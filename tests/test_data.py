import numpy as np

from c3sim import data


def test_same_seed_same_split():
    cnt = np.random.default_rng(0).integers(1, 1000, 5000)
    a, _ = data.binom_split(cnt, 0.9, 7)
    b, _ = data.binom_split(cnt, 0.9, 7)
    c, _ = data.binom_split(cnt, 0.9, 8)
    assert (a == b).all() and not (a == c).all()


def test_split_conserves_mass_and_is_account_level():
    cnt = np.array([1, 1, 5, 100, 10**6])
    tr, te = data.binom_split(cnt, 0.5, 1)
    assert (tr + te == cnt).all() and (tr >= 0).all() and (te >= 0).all()


def test_clean_aggregates_and_filters():
    pw, c = data.clean([b"a", b"a", b"", b"caf\xc3\xa9", b"x" * 31, b"b c"], np.array([1, 2, 5, 5, 5, 4]))
    assert dict(zip(pw.tolist(), c.tolist())) == {b"a": 3, b"b c": 4}


def test_real_splits_deterministic_and_pools_consistent(corpora):
    s1, s2 = data.splits(), data.splits()
    for k in s1:
        assert (s1[k][0] == s2[k][0]).all() and (s1[k][1] == s2[k][1]).all()
    a = data.load_corpus("rockyou")
    assert int(s1["A_train"][1].sum() + s1["A_test"][1].sum()) == int(a["cnt"].sum())
    assert int(s1["A_dev"][1].sum() + s1["A_fresh"][1].sum()) == int(s1["A_test"][1].sum())
