import pytest

from c3sim import data, estimators


@pytest.fixture(scope="session")
def corpora():
    """Skip (not error) every corpus-dependent test when the corpora are absent (data/ not fetched, no cache)."""
    if not data.corpora_available():
        pytest.skip("corpora not available: run `make fetch` (or set C3SIM_DATA / C3SIM_CACHE)")


@pytest.fixture(scope="session")
def sp(corpora):
    return data.splits()


@pytest.fixture(scope="session")
def est(sp):
    return estimators.Estimator(*sp["A_train"], t=100_000)
