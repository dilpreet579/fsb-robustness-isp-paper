"""Phase 1c: Xato list loading and the short-candidate filter."""
from types import SimpleNamespace

import numpy as np
import pytest

from c3sim import data
from experiments import common as C


def test_xato_list_is_first_370_lines():
    x = C.load_xato()
    if x is None:
        pytest.skip("data/xato not fetched")
    # line 43 of the SecLists file is blank, so the first 370 lines hold 369 real passwords (a blank cannot match the length >= 8 policy)
    assert len(x) == 370 and x[0] == b"123456" and x[1] == b"password" and (x == b"").sum() == 1


def test_policy_and_short_filter_semantics():
    pw = np.array([b"123456", b"ab", b"abcdefgh", b"password1", b"zz", b"trustno1"], dtype="S30")
    w = SimpleNamespace(pw=pw, t=2)  # head = first 2 rows
    banned = np.array([b"password1"], dtype="S30")
    pol = C.World.policy_mask(w, pw, banned)  # length >= 8 and not banned
    assert pol.tolist() == [False, False, True, False, False, True]
    keep = C.World.short_keep(w)  # drop length <= 2 outside the head (index >= t)
    assert keep.tolist() == [True, True, True, True, False, True]
    assert (data.lengths(pw) == [6, 2, 8, 9, 2, 8]).all()
