"""T4: worked examples for the human to replay by hand -> results/worked_examples.txt.

Setting: M0, attacker model 'est' (weights p^), FSB qbar=100 (5 examples) and HPB l=11 (2 examples).
Each example is also recomputed with a naive scan over the whole candidate list (no lookup structure).
"""
import hashlib
import os

import numpy as np

from c3sim import attacker as atk
from c3sim import data
from experiments import common as C


def main():
    w = C.World()
    att, (tp, tc), _ = w.condition("M0", model="est")
    pool = tp[data.sample_targets(tp, tc, 4000, 7000)]
    # classify targets by their count in the leak
    srt = np.argsort(w.pw)
    spw = w.pw[srt]
    pos = np.searchsorted(spw, pool)
    pos[pos == len(srt)] = 0
    in_leak = spw[pos] == pool
    leak_idx = np.where(in_leak, srt[pos], -1)
    c = np.where(leak_idx >= 0, w.cnt[np.maximum(leak_idx, 0)], 0)
    picks = [np.flatnonzero(c >= 1000)[0], np.flatnonzero((c >= 21) & (c < 1000))[0], np.flatnonzero((c >= 2) & (c < 21))[0],
             np.flatnonzero(c == 1)[0], np.flatnonzero(c == 0)[0]]
    cats = ["head (leak count >= 1000)", "histogram (21..999)", "tail (2..20)", "tail singleton", "not in the leak S~"]
    fsb = atk.FSB([w.base_member()], 100, w.bits)
    hpb = atk.HPB(11)
    B = fsb.B
    p_q = fsb.members[0][1]
    L = ["WORKED EXAMPLES (T4). Condition M0, attacker model 'est' (weights = public estimate p^), candidate list = top 2,000,000 of S~ by p^.",
         "",
         "How to replay by hand",
         f"  * hash:  d = SHA-256(b'{data.SALT.decode()}' + password);  h = first 8 bytes of d as a big-endian integer;  f(w) = h >> (64 - bits).",
         "    python3 -c \"import hashlib;d=hashlib.sha256(b'c3sim-salt-v1'+b'123456').digest();print(int.from_bytes(d[:8],'big')>>40)\"   (bits=24)",
         f"  * FSB: |B| = 2^{w.bits} = {B:,};  gamma(w) = min(|B|, ceil(|B| * p^(w) / p^(w_qbar))),  p^(w_qbar) = {p_q:.10e}  (qbar = 100).",
         "    The client picks offset u uniformly in [0, gamma(w)-1]; its bucket is b = (f(w) + u) mod |B|.",
         "    A candidate c is in bucket b iff (b - f(c)) mod |B| < gamma(c).  Score = weight(c) / gamma(c), larger first; ties by weight, then lexicographic.",
         "  * p^(w) for a password in the histogram head (top 100,000 of S~) is count / total, total = %d (sum of A_train counts); otherwise 3-gram probability * scale (scale = %.6f)."
         % (int(w.cnt.sum()), w.est.scale),
         "  * 'weight' below is p^ (attacker model est); p_att = weight / (sum of weights over S~'s candidate set) is shown for reference.",
         ""]
    for scheme, sname, idxs, cl in ((fsb, "FSB qbar=100", picks, cats), (hpb, "HPB l=11", [picks[0], picks[2]], [cats[0], cats[2]])):
        tg = pool[idxs]
        r = atk.play(att, scheme, "we" + sname, tg, np.random.default_rng(11))
        for k, t in enumerate(tg):
            d = hashlib.sha256(data.SALT + t.item()).digest()
            f = int.from_bytes(d[:8], "big") >> (64 - scheme.bits)
            assert f == r["f"][k]
            g = int(r["gamma"][k])
            b = int(r["b"][k])
            ph = w.est.phat(np.array([t], dtype="S30"))[0]
            L += [f"--- {sname}, example {k + 1}: target = {t.decode()!r}  [{cl[k]}; leak count {int(c[idxs[k]])}]",
                  f"    sha256 prefix = {d[:8].hex()}  f(w) = {f}",
                  (f"    p^(w) = {ph:.6e};  |B|*p^(w)/p^(w_qbar) = {B * ph / p_q:.4f}  ->  gamma(w) = {g:,}" if scheme.kind == "fsb"
                   else f"    gamma(w) = 1 (HPB: bucket = first 11 bits of the hash)"),
                  f"    client offset u = {(b - f) % scheme.B:,};  bucket b = {b:,}",
                  f"    candidates in bucket b (fast lookup): {int(r['n_cand_in_bucket'][k]):,}"]
            # naive recomputation over the whole candidate list
            gam = scheme.gamma(att.pw)
            fc = (att.h >> np.uint64(64 - scheme.bits)).astype(np.int64)
            inb = np.flatnonzero(((b - fc) % scheme.B) < gam)
            sc = att.cnt[inb] / gam[inb]
            o = np.lexsort((inb, -sc))[:5]
            naive = inb[o]
            fast = r["top"][k][:5]
            L.append(f"    naive scan over all {len(att.pw):,} candidates: {len(inb):,} in bucket; top-5 identical to fast lookup: {bool((naive == fast).all())}")
            assert (naive == fast).all() and len(inb) == int(r["n_cand_in_bucket"][k])
            L.append("    top-5 guesses:   rank  password             weight p^(c)    p_att(c)       gamma(c)   f(c)       score=weight/gamma")
            for j, ci in enumerate(fast):
                L.append(f"                     {j + 1:>4}  {att.pw[ci].decode():<20} {att.cnt[ci]:.4e}   {att.p_att(ci):.4e}   {int(gam[ci]):>9,}  {int(fc[ci]):>9,}  {att.cnt[ci] / gam[ci]:.6e}")
            tr = int(r["tr"][k])
            hit = [int(j) + 1 for j in np.flatnonzero(r["top"][k] == tr)]
            L.append(f"    target is candidate #{tr if tr >= 0 else 'n/a (not in list)'}; position in the bucket guess list: {hit[0] if hit else 'not in top 1000'}; "
                     f"position without bucket (baseline): {tr + 1 if 0 <= tr < 1000 else 'not in top 1000'}")
            L.append("")
    txt = "\n".join(L)
    open(os.path.join(C.RESULTS, "worked_examples.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
