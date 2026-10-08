import pytest

from c3sim import data, estimators


@pytest.fixture(scope="session")
def sp():
    return data.splits()


@pytest.fixture(scope="session")
def est(sp):
    return estimators.Estimator(*sp["A_train"], t=100_000)
