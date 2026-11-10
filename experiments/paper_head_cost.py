"""Paper item 3: how much data would a client need to hold the histogram head? -> paper/head_cost.csv (used in table T3).

THIS IS AN ESTIMATE OF DATA SIZE, NOT AN IMPLEMENTATION. Nothing is transmitted, compressed on a wire, or stored by the simulator; the numbers say how many bytes
the head would occupy if it were written down in the simplest way, so the paper can state an order of magnitude.

For t in {100k, 300k, 1M, 3M, 10M}: the head = the t most frequent passwords of the leak S~ = A_train (rank by count, ties lexicographic, as in every experiment).
  plain_text_bytes   = sum over the t head strings of (length + 1)   [one newline delimiter per string]
  gzip9_bytes        = gzip -9 of the newline-delimited text (gzip header mtime = 0, so the number is reproducible)
  prob_float32_bytes = 4 * t  (one float32 probability per entry; the head probabilities are count / total)
  *_MB               = bytes / 1e6 (decimal megabytes); plain+prob and gzip+prob add the probability array to the text
The 3-gram table of the estimator is 97 x 97 x 96 numbers (97 context symbols = 95 printable + BOS + unused slot, 96 next symbols = 95 printable + EOS):
  float32 = 4 bytes per number, float64 = 8 bytes per number (the simulator itself stores float64 log-probabilities).
Needs the corpora (reads A_train via c3sim.data.splits())."""
import gzip
import os

import numpy as np
import pandas as pd

from c3sim import data
from experiments.paper_common import PAPER

TS = (100_000, 300_000, 1_000_000, 3_000_000, 10_000_000)
TRIGRAM_ENTRIES = 97 * 97 * 96


def main():
    pw, cnt = data.splits()["A_train"]  # sorted by count desc: the first t rows are the head
    rows = []
    for t in TS:
        head = pw[:t]
        plain = int(data.lengths(head).sum() + t)
        blob = b"\n".join(head.tolist()) + b"\n"
        assert len(blob) == plain
        gz = len(gzip.compress(blob, compresslevel=9, mtime=0))
        prob = 4 * t
        rows.append(dict(t=t, entries=t, head_mass_share=round(float(cnt[:t].sum() / cnt.sum()), 6), plain_text_bytes=plain, gzip9_bytes=gz, prob_float32_bytes=prob,
                         plain_MB=plain / 1e6, gzip9_MB=gz / 1e6, prob_float32_MB=prob / 1e6, plain_plus_prob_MB=(plain + prob) / 1e6, gzip9_plus_prob_MB=(gz + prob) / 1e6,
                         trigram_entries=TRIGRAM_ENTRIES, trigram_float32_MB=TRIGRAM_ENTRIES * 4 / 1e6, trigram_float64_MB=TRIGRAM_ENTRIES * 8 / 1e6,
                         note="estimate of data size, not an implementation; MB = 1e6 bytes"))
        print(f"t={t:>10,}: plain {plain / 1e6:7.2f} MB, gzip -9 {gz / 1e6:7.2f} MB, +float32 probs {prob / 1e6:6.2f} MB", flush=True)
    os.makedirs(PAPER, exist_ok=True)
    pd.DataFrame(rows).round(6).to_csv(os.path.join(PAPER, "head_cost.csv"), index=False)
    print("NOTE: these are estimates of data size, not an implementation.")


if __name__ == "__main__":
    main()
