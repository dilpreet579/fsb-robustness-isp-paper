"""Shared harness for E1-E3: the world (data, estimator, attackers per condition) and result rows."""
import argparse
import csv
import hashlib
import json
import os
import time

import numpy as np
from scipy.special import ndtri

from c3sim import attacker as atk
from c3sim import data, estimators

QS = (1, 10, 100, 1000)
COLS = ["condition", "scheme", "variant", "param", "avg_bucket", "max_bucket", "q", "baseline_success",
        "bucket_success", "loss", "std_over_repeats", "n_targets", "repeats", "pool", "seed", "cfg_hash", "attacker"]
# `attacker` is an added trailing column: 'est' = weights p^ (base paper), 'emp' = weights from counts (plan literal)
MODELS = ("est", "emp")
RESULTS = os.path.join(data.ROOT, "results")
N_CAND = 2_000_000


def args(desc):
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument("--fast", action="store_true", help="2,000 targets, 3 repeats")
    a = ap.parse_args()
    a.n_targets, a.repeats = (2000, 3) if a.fast else (5000, 5)
    return a


def cfg_hash(**kw):
    return hashlib.sha1(json.dumps(kw, sort_keys=True, default=str).encode()).hexdigest()[:10]


XATO = os.path.join(data.DATA, "xato", "xato-net-10-million-passwords-1000.txt")


def load_xato(n=370):
    """First n lines of SecLists Passwords/Common-Credentials/xato-net-10-million-passwords-1000.txt (the top-1000 of the Xato 10M list)."""
    if not os.path.exists(XATO):
        return None
    with open(XATO, "rb") as f:
        return np.array([ln.rstrip(b"\r\n") for ln in f.read().split(b"\n")[:n]], dtype=f"S{data.W}")


def memo(fn):
    """Cache fn on big arrays (the attacker's candidate list is evaluated once per estimator, not once per qbar)."""
    cache = {}

    def g(s):
        if len(s) < 100_000:
            return fn(s)
        k = (id(s), len(s))
        if k not in cache:
            cache[k] = (s, fn(s))  # keep s alive so id(s) cannot be reused
        return cache[k][1]

    return g


class World:
    """Leak S~ = A_train, server estimate, and attackers/target pools for M0-M3."""

    def __init__(self, t=100_000, smoothing="adddelta", n_cand=N_CAND, postproc=None):
        """postproc(world) -> (phat_fn, ph_S) replaces the deployed estimate (Phase 1b calibration)."""
        self.t, self.smoothing, self.n_cand = t, smoothing, n_cand
        self.sp = data.splits()
        self.xato = load_xato()  # Phase 1c banned list (first 370 lines of the Xato top-1000); None if the file is absent
        self.pw, self.cnt = self.sp["A_train"]
        self.N = len(self.pw)
        if n_cand is None:  # Phase 1e: the attacker holds every password of S~ (no generated strings)
            self.n_cand = self.N
        self.bits = int(np.ceil(np.log2(self.N)))
        self.h_S = data.pool_hash(self.pw)
        t0 = time.time()
        self.est = estimators.Estimator(self.pw, self.cnt, t=t, smoothing=smoothing)
        self.ph_S = self.est.phat_ranked(self.pw)
        self._base_fn = memo(self.est.phat)
        if postproc is not None:
            fn, self.ph_S = postproc(self)
            self._base_fn = memo(fn)
        print(f"[world] N={self.N:,} |B|=2^{self.bits} estimator built in {time.time() - t0:.0f}s", flush=True)
        self._att = {}
        self._zs = {}  # noise draws by salt (pw-aligned z_w)

    # ---- conditions -------------------------------------------------------------------------------------------
    def banned(self):  # named list for M2
        return self.pw[:370]

    def policy_mask(self, pw, banned=None, minlen=8):
        """Password policy: length >= minlen and not on the banned list (Phase 1d ablation varies both)."""
        return (data.lengths(pw) >= minlen) & ~np.isin(pw, self.banned() if banned is None else banned)

    def _ablate(self, cond, pw):
        """M2L: length >= 8 only (empty banned list). M2B: Xato blocklist only (no length rule)."""
        if cond == "M2L":
            return self.policy_mask(pw, banned=np.array([], dtype=f"S{data.W}"), minlen=8)
        return self.policy_mask(pw, banned=self.xato, minlen=0)

    def short_keep(self):
        """Phase 1c sanity: drop attacker candidates of length <= 2 that are outside the histogram head (index >= t)."""
        return ~((data.lengths(self.pw) <= 2) & (np.arange(len(self.pw)) >= self.t))

    def condition(self, cond, pool=None, model="est"):
        """(attacker, target pool (pw, cnt), pool name) for M0 / M1 / M2 / M3.
        model 'emp': attacker weights = empirical counts of its training corpus (plan literal).
        model 'est': attacker weights = the public estimate p^ (what the base paper's attacker uses). M1 has no p^
        for the attacker's own corpus, so M1 is always empirical (same object for both models)."""
        # M1b (Phase 1b): server estimate from A_train, targets from B_target, attacker = the M0 attacker (weights p^ or counts)
        # Phase 1c: M1a = M1 (alias), M2x = M2 with the Xato top-370 banned list, M0s / M2s = est-attacker sanity (short candidates removed)
        key = ({"M3": "M0", "M1b": "M0", "M1a": "M1"}.get(cond, cond), model if cond not in ("M1", "M1a") else "emp")  # attackers shared; pools are not
        if key not in self._att:
            w = self.cnt if model == "emp" else self.gt_weights() if model == "gt" else self.ph_S  # weights over S~ (aligned with self.pw)
            if key[0] == "M0":
                self._att[key] = atk.Attacker(self.pw, w, self.n_cand, name=f"A_train/{model}")
            elif key[0] == "M1":
                bp, bc = self.sp["B_attack"]
                self._att[key] = atk.Attacker(bp, bc, self.n_cand, name="B_attack/emp")
            elif key[0] == "M2x":
                self._att[key] = atk.Attacker(self.pw, w, self.n_cand, keep=self.policy_mask(self.pw, self.xato), name=f"A_train|policy_xato/{model}")
            elif key[0] in ("M2L", "M2B"):  # Phase 1d ablation: length >= 8 only / Xato blocklist only
                self._att[key] = atk.Attacker(self.pw, w, self.n_cand, keep=self._ablate(key[0], self.pw), name=f"A_train|{key[0]}/{model}")
            elif key[0] == "M0s":
                self._att[key] = atk.Attacker(self.pw, w, self.n_cand, keep=self.short_keep(), name=f"A_train|noshort/{model}")
            elif key[0] == "M2s":
                self._att[key] = atk.Attacker(self.pw, w, self.n_cand, keep=self.policy_mask(self.pw, self.xato) & self.short_keep(),
                                              name=f"A_train|policy_xato|noshort/{model}")
            else:  # M2
                self._att[key] = atk.Attacker(self.pw, w, self.n_cand, keep=self.policy_mask(self.pw), name=f"A_train|policy/{model}")
        # target pool: pool in (None, 'dev', 'fresh')
        tag = {None: "", "dev": "_dev", "fresh": "_fresh"}[pool]
        if cond in ("M1", "M1a", "M1b"):
            name = "B_dev" if pool == "dev" else "B_fresh" if pool == "fresh" else "B_target"
            return self._att[key], self.sp[name], name
        name = {"": "A_test", "_dev": "A_dev", "_fresh": "A_fresh"}[tag]
        pw, cnt = self.sp[name]
        if cond == "M2":
            m = self.policy_mask(pw)
            return self._att[key], (pw[m], cnt[m]), name + "|policy"
        if cond in ("M2x", "M2s"):
            m = self.policy_mask(pw, self.xato)
            return self._att[key], (pw[m], cnt[m]), name + "|policy_xato"
        if cond in ("M2L", "M2B"):
            m = self._ablate(cond, pw)
            return self._att[key], (pw[m], cnt[m]), name + ("|len8_only" if cond == "M2L" else "|blocklist_only")
        return self._att[key], (pw, cnt), name

    def gt_weights(self, rmax=5):
        """Phase 1g attacker 'gt': leak counts with Good-Turing adjusted values for counts r <= rmax (Turing: r* = (r+1) n_{r+1} / n_r,
        n_r = number of passwords with count r), raw counts above. The leak-holding attacker that does not take a count-1 password at face value."""
        c = self.cnt
        n = np.bincount(c, minlength=rmax + 2)[: rmax + 2].astype(np.float64)
        w = c.astype(np.float64)
        for r in range(1, rmax + 1):
            w[c == r] = (r + 1) * n[r + 1] / n[r]
        return w

    # ---- estimates --------------------------------------------------------------------------------------------
    def noise(self, strings, salt=None):
        """z_w ~ N(0,1) seeded by the password (salted SHA-256 -> uniform -> probit). salt=None is the Phase 1-1c draw."""
        h = data.salted_hash64(strings, salt or data.NOISE_SALT)
        return ndtri(((h >> np.uint64(11)).astype(np.float64) + 0.5) / 2.0 ** 53)

    def noisy_member(self, sigma, salt=None):
        """FSB member with p^ * exp(sigma z_w). salt = another noise draw (Phase 1d); None = the original draw."""
        salt = salt or data.NOISE_SALT
        if salt not in self._zs:
            self._zs[salt] = ndtri(((data.pool_hash(self.pw, salt) >> np.uint64(11)).astype(np.float64) + 0.5) / 2.0 ** 53)
        z = self._zs[salt]
        return memo(lambda s: self._base_fn(s) * np.exp(sigma * self.noise(s, salt))), self.ph_S * np.exp(sigma * z)

    def base_member(self):
        return self._base_fn, self.ph_S

    # ---- E3 variants (plan T7) ---------------------------------------------------------------------------------
    def _cached(self, name, fn):
        key = hashlib.sha1(f"{name}|{self.N}|{int(self.cnt.sum())}|{self.t}|{data.SEED_A}".encode()).hexdigest()[:12]
        p = os.path.join(data.CACHE, f"ph_{name}_{key}.npy")
        if os.path.exists(p):
            return np.load(p)
        x = fn()
        np.save(p, x)
        return x

    def boot_member(self, k):
        """Poisson bootstrap resample of the leak counts (seed 500+k); own histogram and own 3-gram."""
        c2 = np.random.default_rng(500 + k).poisson(self.cnt).astype(np.int64)
        m = c2 > 0
        pw2, c2 = data.sort_corpus(self.pw[m], c2[m])
        est = estimators.Estimator(pw2, c2, t=self.t, smoothing=self.smoothing)
        return memo(est.phat), self._cached(f"boot{k}", lambda: est.phat(self.pw))

    def tempered_member(self, tau):
        return memo(lambda s: self._base_fn(s) ** tau), self.ph_S ** tau

    def smoothed_member(self):
        est = estimators.Estimator(self.pw, self.cnt, t=self.t, smoothing="kn")
        return memo(est.phat), self._cached("kn", lambda: est.phat_ranked(self.pw))

    def members(self, variant):
        if variant == "fsb_base":
            return [self.base_member()]
        if variant == "ens_max":
            return [self.base_member()] + [self.boot_member(k) for k in range(5)] + [self.tempered_member(t) for t in (0.8, 0.6)]
        if variant == "smoothed":
            return [self.smoothed_member()]
        raise ValueError(variant)


def run(world, cond, scheme, name, variant, param, n_targets, repeats, seed, pool=None, tag="", extra_cfg=None, models=MODELS):
    """Both attacker models; returns the concatenated rows."""
    return [r for m in models for r in run1(world, cond, scheme, name, variant, param, n_targets, repeats, seed, pool, tag, extra_cfg, m)]


def run1(world, cond, scheme, name, variant, param, n_targets, repeats, seed, pool, tag, extra_cfg, model):
    """Play both games `repeats` times (targets re-sampled each time, seeded) and return result rows."""
    att, (tp, tc), pool_name = world.condition(cond, pool, model)
    avg, mx = scheme.sizes(world.h_S)
    key = f"{name}|{variant}|{param}|{tag}"
    t0 = time.time()
    res = []
    for r in range(repeats):
        tgt = tp[data.sample_targets(tp, tc, n_targets, seed + r)]
        res.append(atk.play(att, scheme, key, tgt, np.random.default_rng(seed + 1000 + r)))
    att._ix.clear()
    cfg = cfg_hash(cond=cond, scheme=name, variant=variant, param=param, n=n_targets, rep=repeats, seed=seed, pool=pool_name,
                   t=world.t, smoothing=world.smoothing, n_cand=world.n_cand, splits=[data.SEED_A, data.SEED_B, data.SEED_DEV],
                   extra=extra_cfg, attacker=model)
    rows = []
    for q in QS:
        b = np.array([x["bucket"][q] for x in res]) * 100
        a = np.array([x["baseline"][q] for x in res]) * 100
        loss = b - a
        rows.append(dict(condition=cond, scheme=name, variant=variant, param=param, avg_bucket=round(avg, 2), max_bucket=mx, q=q,
                         baseline_success=round(a.mean(), 3), bucket_success=round(b.mean(), 3), loss=round(loss.mean(), 3),
                         std_over_repeats=round(float(loss.std(ddof=1)) if repeats > 1 else 0.0, 3), n_targets=n_targets,
                         repeats=repeats, pool=pool_name, seed=seed, cfg_hash=cfg, attacker=model,
                         t=world.t, cand_per_bucket=round(float(np.mean([x["mean_cand_in_bucket"] for x in res])), 1),  # t, cand_per_bucket: Phase 1b+ CSVs only
                         loss_by_repeat=[round(float(v), 4) for v in loss],  # in-memory only (not CSV columns); Phase 1c/1d intervals and ratios
                         bucket_by_repeat=[round(float(v), 4) for v in b], baseline_by_repeat=[round(float(v), 4) for v in a]))
    L = {r["q"]: r["loss"] for r in rows}
    print(f"[{cond}/{model}] {name:>3} {variant:<10} param={param!s:<6} avg={avg:>9.1f} max={mx:>8} "
          f"loss q1/10/100/1000 = {L[1]:+6.2f} {L[10]:+6.2f} {L[100]:+6.2f} {L[1000]:+6.2f}   "
          f"base@1000={rows[-1]['baseline_success']:.2f} cand/bucket={np.mean([x['mean_cand_in_bucket'] for x in res]):.0f} "
          f"[{time.time() - t0:.0f}s]", flush=True)
    return rows


COLS1B = COLS + ["t", "cand_per_bucket"]  # Phase 1b CSVs


def write_csv(path, rows, cols=COLS):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
