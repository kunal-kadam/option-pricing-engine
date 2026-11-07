"""Step 5 checks: the binomial tree converges to Black-Scholes across step counts.

The full study is in validation/convergence.py. Its error oscillates from one
step count to the next (the CRR tree is not monotone), so the tests check the
overall trend and the accuracy at 1000 steps rather than strict decrease.
"""

import pytest

from option_pricing.binomial import price as tree_price
from option_pricing.black_scholes import price as bs_price

CASES = {
    "at_the_money": dict(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.20),
    "in_the_money": dict(S=100.0, K=90.0, T=1.0, r=0.05, sigma=0.20),
    "out_of_the_money": dict(S=100.0, K=110.0, T=1.0, r=0.05, sigma=0.20),
}


@pytest.mark.parametrize("option_type", ["call", "put"])
@pytest.mark.parametrize("case", sorted(CASES))
def test_error_at_1000_steps_is_small(case, option_type):
    params = CASES[case]
    error = abs(tree_price(n_steps=1000, option_type=option_type, **params)
                - bs_price(option_type=option_type, **params))
    assert error < 0.005


@pytest.mark.parametrize("option_type", ["call", "put"])
@pytest.mark.parametrize("case", sorted(CASES))
def test_error_trend_falls_from_10_to_1000_steps(case, option_type):
    params = CASES[case]
    reference = bs_price(option_type=option_type, **params)
    coarse = abs(tree_price(n_steps=10, option_type=option_type, **params) - reference)
    fine = abs(tree_price(n_steps=1000, option_type=option_type, **params) - reference)
    assert fine < coarse


@pytest.mark.parametrize("case", sorted(CASES))
def test_call_and_put_errors_match(case):
    # Put-call parity holds on the tree, so the call and put errors are equal.
    params = CASES[case]
    for n in (10, 100, 1000):
        call_err = tree_price(n_steps=n, option_type="call", **params) - bs_price(option_type="call", **params)
        put_err = tree_price(n_steps=n, option_type="put", **params) - bs_price(option_type="put", **params)
        assert call_err == pytest.approx(put_err, abs=1e-9)
