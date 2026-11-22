"""FIST-2027 version (paper/fist): anonymity of the review copy and the 6-page limit. Static checks always run; PDF checks skip when the PDFs or poppler are absent."""
import os
import re
import shutil
import subprocess

import pytest

FIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "paper", "fist")
IDENTIFYING = ["Dilpreet", "Ishita", "Madhav", "Sandhya", "Pundhir", "National Institute of Technology", "dilpreet579", "NIT Delhi"]


def _body():
    return open(os.path.join(FIST, "fist_body.tex"), encoding="utf8").read()


def test_review_copy_source_has_no_identifying_strings():
    """With \\blindtrue, only the branch before \\else of every \\ifblind ... \\else ... \\fi survives; it must not name the authors, the institute or the repository."""
    blind = re.sub(r"\\ifblind(.*?)\\else.*?\\fi", r"\1", _body(), flags=re.S)
    leaks = [s for s in IDENTIFYING if s in blind]
    assert not leaks, leaks
    assert "\\blindtrue" in open(os.path.join(FIST, "fist_blind.tex")).read()
    assert "\\blindfalse" in open(os.path.join(FIST, "fist_named.tex")).read()


def test_named_copy_does_carry_the_authors():
    assert all(s in _body() for s in ("Dilpreet Singh", "Ishita Gupta", "Madhav Raj", "Dr.\\ Sandhya Pundhir", "National Institute of Technology Delhi", "dilpreet579"))


def _pdf(name):
    p = os.path.join(FIST, name)
    if not os.path.exists(p) or not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        pytest.skip("PDF or poppler not available: run `make paper-fist`")
    return p


@pytest.mark.parametrize("name", ["fist_blind.pdf", "fist_named.pdf"])
def test_pdf_is_a4_and_at_most_six_pages(name):
    info = subprocess.run(["pdfinfo", _pdf(name)], capture_output=True, text=True).stdout
    assert int(re.search(r"Pages:\s+(\d+)", info).group(1)) <= 6
    assert "A4" in info


def test_review_pdf_text_and_metadata_have_no_identifying_strings():
    p = _pdf("fist_blind.pdf")
    text = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
    meta = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout
    assert not [s for s in IDENTIFYING if s in text or s in meta]
    assert "Author:" not in meta
