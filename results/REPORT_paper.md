# Paper PDF build report

## What was built
- `paper/preamble.tex` (document class article 10pt two-column, 0.75in margins, natbib author-year, booktabs; page layout lives only here; the author block is in `main.tex`), `paper/main.tex` (md text converted), `paper/refs.bib` (only fields given in the md reference list; `hunt` has `year={n.d.}`, `miessler` has no year, so BibTeX prints "empty year in miessler").
- `make paper-pdf` builds `paper/main.pdf` from scratch with tectonic (it runs BibTeX itself).
- `paper/check_text_numbers.py` (number audit, writes `paper/text_numbers_audit.tsv`).
- Tooling deviation: no pdflatex/latexmk/bibtex/biber/tlmgr/apt were available and basictex needs sudo, so `tectonic 0.17.0` and `poppler` were installed with Homebrew.

## Build status
- 8 pages. Body (Sections 1-7, Ethics, AI use, Availability) **and the reference list** fit inside pages 1-7 (no text was cut; the reference list is set in `\footnotesize` with `\bibsep` 0, the duplicate DOI URL of the Pal 2019 entry was dropped, and the Hunt note was shortened); Appendices A-C are on page 8 (single-column after `\onecolumn`).
- Pages per section (first page to last): 1: p1-2; 2: p2; 3: p2-3; 4: p3-5 (4.1 p3, 4.2 p3, 4.3 p3-4, 4.4 p4, 4.5 p5); 5: p5-6; 6: p6-7; 7: p7.
- Undefined references/citations: 0. Overfull boxes: 2, both about 1 pt (Conditions table). Underfull: 14 (narrow p-columns, appendix/bibliography lines). No overfull above 5 pt.
- Float placement (final build; first citation page / float page): Fig 1 3/3, Table 1 4/4, Fig 2 3/4, Fig 3 5/5, Fig 4 5/6. Every float is within 1 page of its first citation. An earlier build drifted 2-3 pages; the float sources were moved to the start of the citing subsection (D34). Page count and body length did not change (9 pages, body ends p7).
- Page images were inspected for all pages in the earlier builds and for pages 4 and 6 in the final build; figure fonts are readable, tables fit their columns.

## Non-mechanical edits to the md text (all other changes are LaTeX escaping and citation commands)
1. Date line "Nov 15, 2026 · @Dilpreet Singh" is dropped (`\date{}`, no date printed); the author block lists Dilpreet Singh, Ishita Gupta, Madhav Raj with "National Institute of Technology Delhi" in small font under each name.
2. Hard-coded "Section N", "Figure N", "Table 1", "Appendix A" became `\ref`s.
3. Table 1 uses `T1_headline.tex`, which has two extra columns (success ratio at q=1, FSB and HPB emp). The caption was extended with one sentence defining them (bucket success / baseline success, mean ± sd over 5 repeats). The md text quotes the ratios only for M2x q̄=100 (85 ± 25, 86 ± 21), which equal the table.
4. Captions were condensed from `paper/captions.md` (file names/seed/palette dropped; all numbers kept).
5. Appendix A caption is the md intro sentence; the md closing sentence is kept and duplicates the footnote row inside `T7_m3_crossings.tex`.
6. Added (new text): Appendix B "Head storage" (Table `T3_tsweep_head_storage.tex` + `T3_note.tex`, caption written by me) and Appendix C "Fixes at equal bucket size" (Fig 5, caption condensed). Neither is cited in the body, since the md never mentions them.
7. References 7 (Kneser–Ney) and 8 (SecLists) are never cited in the md; kept via `\nocite`.
8. The md "Conditions" table has no caption in the md and none was added (non-floating tabular).
9. Related Work, "Position": "To our knowledge, no earlier study measures ... but our literature search was not exhaustive and we would welcome pointers to such work." became "We are not aware of an earlier study that measures ... ; our literature search was not exhaustive." The claim itself still needs the authors' literature check.
10. Generative-AI paragraph shortened and made generic (no tool named): "Generative AI tools were used to help write the code and drafts of this paper. The authors reviewed the code and results and take responsibility for the content; all numbers are generated from the result files by scripts in the repository."
11. Layout-only changes: A_train/A_test are math subscripts; headings are ragged-right with no hyphenation; the title is bold; the reference list is in `\small` with tighter spacing; `refs.bib` booktitles no longer repeat the year (printed once from the year field).

### Still open after the review pass
- References: Hunt now carries the date the authors read off the page (30 June 2022; printed "Hunt, 2022"). `docs/paper.md` now says the same. Pasquini is printed as "IEEE S&P, 2024 ... ePrint 2023/1848" (venue plus the ePrint link/ID the md gives).
- Length (resolved without cutting text, see Build status): references now end on p7. The earlier cut candidates were not needed; they were that touch none of C1-C5: the "Storage figures" and "Small second corpus" limitation bullets, the last sentence of the "The estimate" paragraph in Section 2 ("We also evaluate a Kneser-Ney 3-gram ... Section 4 what each variation shows"). Not cut: that changes the md text, so the authors decide.
- Fig. 4 is column width; the single open square (M2x est at t=1M, the only measurement) is explained in the caption. Making it larger means `figure*` with `fig4_wide.pdf` (about +0.1 page); removing the square means changing `experiments/paper_figs.py`, which this task may not touch.

## Number audit (`.venv/bin/python -I paper/check_text_numbers.py`)
Current run: 713 tokens: 543 numbers.csv, 18 head_cost.csv, 8 data_report, 1 e1d_ablation, 6 derived, 60 stated constants, 50 table-provenance (tables byte-identical to a regeneration by `paper_tables.py`), 24 weak (integers below 100 matched only by numbers.csv; coincidence-prone), 1 year excluded, **2 unmatched** (below). The first run had 4 unmatched; the two others were fixed as follows:
- `14.2` (M2L emp loss at q=q̄=100): `e1e_headline.csv` gives 14.148, i.e. 14.1; the md rounded twice (via T1's 14.15). **Fixed in `main.tex`: now 14.1.** T1 still prints 14.15 (two decimals, same value).
- `3.4` (blocklist-only M2B emp, q̄=10) is correct (3.428 in `e1d_ablation.csv`); numbers.csv simply has no M2B rows (D28). Not a text error: the audit now also reads the M2B emp rows of `e1d_ablation.csv` as a documented source. (3.9 and 3.3 in the same sentence are 3.928 and 3.312 in that file.)
- `main.tex:203` `1.5%` (Thomas et al. 2019) and `main.tex:202` `16%` (Pal et al. 2019): external claims, not in the repo; not checked (no network). "12x" and "4 billion" are present in the base paper PDF (`docs/1905.13737v3.pdf`).
- Derived checks: exp(5.86)=351.4 ("about 350"); 0.693/0.308=2.25 and 0.658/0.308=2.13 ("about 2 to 1"); 10M/1M head storage 76.9/7.46 = 10.3 ("ten times"); HPB larger by 1.4%, 24.9%, 13.1% (text 1/25/13%); M2x q=1 removed 0.81% ("under 1%"); FSB est M0 q̄=100 q=1000 loss 11.252 pp (above 10 holds).
- `paper/check_numbers.py`: OK, all 364 numbers match.
- Not audited: numbers written as words ("six baseline successes per repeat", 0.12% × 5,000 = 6, consistent).

## md inconsistencies: fixed in `main.tex`, and `docs/paper.md` was then synced to the PDF text at the authors' request (author line, 98.6%, Section 1/Section 5 pointers, 14.1, Position sentence, generic AI disclosure, Hunt 2022, Appendices B and C added; the md stays untracked and is not to be committed)
- Intro contribution 4 said 98.7% while Section 4.4 says 98.6% (data: M0 FSB q=1 98.64%, q=100 98.67%). Now "98.6% of the targets gained at q = 1" in the intro.
- Section 3 said M1a "is left to the appendix", but the appendix has no M1a content and Limitations says "omitted". Now "is omitted (Section 5)".
- Section 2 said "Section 3 explains why we vary the estimate and the attacker"; Section 3 does not, the Introduction does. Now points to Section 1.
- Also fixed: "14.2" to "14.1" (above). Not fixed, only noted: M2x at q̄=1000, q=1: FSB removes −41.7% of HPB's loss (FSB worse); the md does not mention it.

## Logs and tests
D34 (DISCREPANCIES.md), Q37 (QUESTIONS.md) and the `paper/README.md` section "Paper PDF" were added. `make test`: 39 passed; its rewrite of `results/tests_all.txt` was reverted with `git checkout` to leave `results/` unchanged. Nothing from this task is committed.

## Open items for the human
Author block is filled (Dilpreet Singh, Ishita Gupta, Madhav Raj; institute under each name; no emails or departments). Gen-AI disclosure wording; undated Hunt reference; whether `paper/main.pdf` should be committed (build files are currently untracked and not ignored).
