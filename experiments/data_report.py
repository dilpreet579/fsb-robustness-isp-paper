"""Write results/data_report.md (T1)."""
import os

import numpy as np

from c3sim import data


def top10(pw, cnt):
    return "\n".join(f"| {i + 1} | `{pw[i].decode()}` | {int(cnt[i]):,} | {cnt[i] / cnt.sum():.4%} |" for i in range(10))


def stats(name, pw, cnt):
    s = int((cnt == 1).sum())
    return (f"| {name} | {len(pw):,} | {int(cnt.sum()):,} | {cnt.sum() / len(pw):.2f} | {s / len(pw):.1%} | "
            f"{cnt[:1000].sum() / cnt.sum():.2%} |")


def main():
    out = ["# Data report (T1)", "",
           "Source: SecLists `Passwords/Leaked-Databases/` withcount files, downloaded from "
           "raw.githubusercontent.com/danielmiessler/SecLists/master (never committed; `data/` is in `.gitignore`).",
           "Corpus A = RockYou (`rockyou-withcount.txt.tar.gz`), Corpus B = phpbb (`phpbb-withcount.txt`). "
           "honeynet, RockYou2021 and RockYou2024 are not used (plan section 3).", "",
           "## Raw vs plan (checked in `results/T1_corpus_check.txt`)", "",
           "| corpus | raw unique lines | raw total | plan unique | plan total | match |", "|---|---|---|---|---|---|"]
    for n, U, T in [("rockyou", 14344391, 32603388), ("phpbb", 184388, 255420)]:
        c = data.load_corpus(n)
        out.append(f"| {n} | {int(c['raw_unique']):,} | {int(c['raw_total']):,} | {U:,} | {T:,} | "
                   f"{int(c['raw_unique']) == U and int(c['raw_total']) == T} |")
    out += ["", "Parser notes: phpbb has 1 unparsable line (count 1, empty password; dropped by the length filter) and 4 "
            "passwords that occur on two lines (`666`, `monalisa`, `b`, `ola`; counts aggregated).", "",
            "## After cleaning (printable ASCII 0x20-0x7e, length 1-30, case kept, duplicates aggregated)", "",
            "| pool | unique | total mass | mass/unique | singleton share of unique | top-1000 mass share |",
            "|---|---|---|---|---|---|"]
    for n in ["rockyou", "phpbb"]:
        c = data.load_corpus(n)
        out.append(stats(n, c["pw"], c["cnt"]))
    out += ["", "Dropped by cleaning: rockyou "
            f"{int(data.load_corpus('rockyou')['raw_unique']) - len(data.load_corpus('rockyou')['pw']):,} unique rows; phpbb "
            f"{int(data.load_corpus('phpbb')['raw_unique']) - len(data.load_corpus('phpbb')['pw']):,} unique rows.", ""]
    for n in ["rockyou", "phpbb"]:
        c = data.load_corpus(n)
        out += [f"### Top 10, {n} (cleaned)", "", "| rank | password | count | share |", "|---|---|---|---|", top10(c["pw"], c["cnt"]), ""]

    sp = data.splits()
    out += [f"## Splits (seeds A={data.SEED_A}, B={data.SEED_B}, dev/fresh={data.SEED_DEV}; per-password c_train ~ Binomial(c, p))", "",
            "| pool | role | unique | total mass | top-1000 mass share |", "|---|---|---|---|---|"]
    role = {"A_train": "leak S~ (server), p=0.9", "A_test": "matched target pool (M0, M2, M3)",
            "A_dev": "E3 tuning pool (50% of A_test accounts)", "A_fresh": "E3 reporting pool (other 50% of A_test)",
            "B_attack": "M1 attacker training, p=0.5", "B_target": "M1 cross-corpus target pool",
            "B_dev": "E3 M1 tuning pool (50% of B_target accounts)", "B_fresh": "E3 M1 reporting pool (other 50%)"}
    for k, (pw, cnt) in sp.items():
        out.append(f"| {k} | {role[k]} | {len(pw):,} | {int(cnt.sum()):,} | {cnt[:1000].sum() / cnt.sum():.2%} |")
    N = len(sp["A_train"][0])
    lg = int(np.ceil(np.log2(N)))
    out += ["", f"S~ = A_train: N = {N:,} unique passwords, |B| = 2^{lg} = {2 ** lg:,}.", ""]
    trs = set(sp["A_train"][0].tolist())
    te = sp["A_test"]
    inn = np.fromiter((p in trs for p in te[0].tolist()), bool, len(te[0]))
    out += [f"A_test accounts whose password is in A_train: {te[1][inn].sum() / te[1].sum():.1%} "
            f"(of test mass); unique-test-rows in A_train: {inn.mean():.1%}.", "",
            "Disjointness: splits are by account (the count of each password is divided between the two sides), so "
            "the *pools* share passwords but never accounts. A_train / A_test and B_attack / B_target are disjoint at the "
            "account level by construction (`c_train + c_test == c`, checked in `tests/test_data.py`). "
            "Cross-corpus: B_target accounts are never in A_train (different corpus), but passwords overlap.", ""]
    bt = sp["B_target"]
    ai = set(sp["A_train"][0].tolist())
    inb = np.fromiter((p in ai for p in bt[0].tolist()), bool, len(bt[0]))
    out += [f"B_target mass whose password is in A_train: {bt[1][inb].sum() / bt[1].sum():.1%}.", "",
            "## Limitations (phpbb)", "",
            "phpbb is small and mostly singletons (total/unique about 1.4). After the 50/50 split B_target holds "
            f"{int(bt[1].sum()):,} accounts, enough for 5,000 targets, but its tail carries no information beyond the top few "
            "thousand passwords. The M1 attacker (B_attack) only knows the passwords it has seen "
            f"({len(sp['B_attack'][0]):,} unique), so its candidate list is that vocabulary, not 2,000,000 entries. "
            "Cross-corpus results mix a distribution shift (RockYou 2009 social-site users vs phpbb forum users) with attacker-vocabulary "
            "size; the two effects cannot be separated here.", ""]
    with open(os.path.join(data.ROOT, "results", "data_report.md"), "w") as f:
        f.write("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
