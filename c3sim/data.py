"""T1: load SecLists *-withcount files, clean, and make seeded binomial account splits.

A corpus is (pw, cnt): pw is a numpy 'S30' array (zero padded, no NULs inside), cnt an int64 array,
sorted by count desc then password asc (so index == rank, ties broken lexicographically).
"""
import hashlib
import os
import tarfile

import numpy as np

W = 30  # max password length
SALT = b"c3sim-salt-v1"
NOISE_SALT = b"c3sim-noise-v1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(ROOT, "cache")
PATHS = {
    "rockyou": os.path.join(DATA, "rockyou", "rockyou-withcount.txt"),
    "phpbb": os.path.join(DATA, "phpbb", "phpbb-withcount.txt"),
}


def extract_rockyou():
    """Extract the tarball into its own directory (data/rockyou/); only the one expected member."""
    d = os.path.dirname(PATHS["rockyou"])
    if os.path.exists(PATHS["rockyou"]):
        return
    with tarfile.open(os.path.join(d, "rockyou-withcount.txt.tar.gz")) as t:
        m = [x for x in t.getmembers() if os.path.basename(x.name) == "rockyou-withcount.txt" and x.isfile()]
        assert len(m) == 1, [x.name for x in t.getmembers()]
        with t.extractfile(m[0]) as src, open(PATHS["rockyou"], "wb") as dst:
            while chunk := src.read(1 << 24):
                dst.write(chunk)


def read_raw(path):
    """Parse `count password` lines (uniq -c style). Returns (list of bytes pw, int64 counts, n_bad_lines)."""
    pws, cnts, bad = [], [], 0
    with open(path, "rb") as f:
        for line in f:
            line = line.rstrip(b"\r\n").lstrip(b" ")
            head, sep, pw = line.partition(b" ")
            if not sep or not head.isdigit():
                bad += 1
                continue
            pws.append(pw)
            cnts.append(int(head))
    return pws, np.array(cnts, dtype=np.int64), bad


def clean(pws, cnts):
    """Printable ASCII (0x20-0x7e) only, length 1..30, case kept, duplicate counts aggregated."""
    keep = np.fromiter(
        (1 <= len(p) <= W and p.isascii() and all(32 <= c < 127 for c in p) for p in pws),
        dtype=bool, count=len(pws))
    arr = np.array([p for p, k in zip(pws, keep) if k], dtype=f"S{W}")
    c = cnts[keep]
    uniq, inv = np.unique(arr, return_inverse=True)
    tot = np.bincount(inv, weights=c, minlength=len(uniq)).astype(np.int64)
    return sort_corpus(uniq, tot)


def sort_corpus(pw, cnt):
    """Count desc, password asc (np.lexsort: last key is primary)."""
    o = np.lexsort((pw, -cnt))
    return pw[o], cnt[o]


def load_corpus(name):
    """Cleaned corpus, cached as .npz. Returns dict(pw, cnt, raw_unique, raw_total, n_bad, ...)."""
    os.makedirs(CACHE, exist_ok=True)
    cp = os.path.join(CACHE, f"{name}_clean.npz")
    if os.path.exists(cp):
        z = np.load(cp)
        return {k: z[k] for k in z.files}
    if name == "rockyou":
        extract_rockyou()
    pws, cnts, bad = read_raw(PATHS[name])
    raw = dict(raw_unique=len(pws), raw_total=int(cnts.sum()), n_bad=bad,
               raw_distinct=len(set(pws)))
    pw, cnt = clean(pws, cnts)
    out = dict(pw=pw, cnt=cnt, **{k: np.int64(v) for k, v in raw.items()})
    np.savez(cp, **out)
    return out


def binom_split(cnt, p, seed):
    """Account-level split: c_train ~ Binomial(c, p), c_test = c - c_train. Deterministic in seed."""
    tr = np.random.default_rng(seed).binomial(cnt, p).astype(np.int64)
    return tr, cnt - tr


def sub_corpus(pw, cnt):
    """Drop zero-count rows, return a sorted corpus."""
    m = cnt > 0
    return sort_corpus(pw[m], cnt[m])


SEED_A, SEED_B, SEED_DEV = 101, 102, 103  # split seeds (never re-rolled)


def splits(seed_a=SEED_A, seed_b=SEED_B, seed_dev=SEED_DEV):
    """All pools as {name: (pw, cnt)}.
    A_train (p=0.9) = leak S~; A_test = matched target pool; A_dev/A_fresh = 50/50 account split of A_test
    (E3: tune on dev, report on fresh); B_attack (p=0.5) trains the M1 attacker; B_target = M1 target pool;
    B_dev/B_fresh = 50/50 account split of B_target (E3 M1 pools)."""
    a, b = load_corpus("rockyou"), load_corpus("phpbb")
    tr, te = binom_split(a["cnt"], 0.9, seed_a)
    dv, fr = binom_split(te, 0.5, seed_dev)
    bt, bg = binom_split(b["cnt"], 0.5, seed_b)
    bdv, bfr = binom_split(bg, 0.5, seed_dev + 1)
    ap, bp = a["pw"], b["pw"]
    return {"A_train": sub_corpus(ap, tr), "A_test": sub_corpus(ap, te),
            "A_dev": sub_corpus(ap, dv), "A_fresh": sub_corpus(ap, fr),
            "B_attack": sub_corpus(bp, bt), "B_target": sub_corpus(bp, bg),
            "B_dev": sub_corpus(bp, bdv), "B_fresh": sub_corpus(bp, bfr)}


def lengths(pw):
    return (pw.view(np.uint8).reshape(len(pw), W) != 0).sum(1)


def salted_hash64(pw, salt=SALT):
    """Top 64 bits of SHA-256(salt || w) as uint64; f(w) = h >> (64 - log2|B|)."""
    sha = hashlib.sha256
    b = b"".join(sha(salt + w).digest()[:8] for w in pw.tolist())
    return np.frombuffer(b, dtype=">u8").astype(np.uint64)


def pool_hash(pw, salt=SALT):
    """salted_hash64 cached on disk, keyed by the exact contents of pw (safe if the split changes)."""
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(np.ascontiguousarray(pw).tobytes() + salt).hexdigest()[:16]
    p = os.path.join(CACHE, f"h64_{key}.npy")
    if os.path.exists(p):
        return np.load(p)
    h = salted_hash64(pw, salt)
    np.save(p, h)
    return h


def sample_targets(pw, cnt, n, seed):
    """n accounts drawn frequency-weighted (with replacement; pool >> n). Returns row indices into pw."""
    return np.random.default_rng(seed).choice(len(pw), size=n, p=cnt / cnt.sum())
