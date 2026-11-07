import numpy as np
import pytest

from option_pricing.binomial import price as binomial_price
from option_pricing.black_scholes import price as bs_price

S0, K0, T0, R0, SIGMA0 = 100.0, 100.0, 1.0, 0.05, 0.20


def test_one_step_matches_hand_calculation():
    # One step: value = e^{-rT} * (p * payoff_up + (1 - p) * payoff_down), computed directly.
    dt = T0
    u = np.exp(SIGMA0 * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(R0 * dt) - d) / (u - d)
    expected = np.exp(-R0 * dt) * p * max(S0 * u - K0, 0.0)
    assert binomial_price(S0, K0, T0, R0, SIGMA0, 1, "call") == pytest.approx(expected, abs=1e-12)


# Observed errors at the reference case are about 0.20, 0.040, 0.020, 0.004, 0.002;
# tolerances sit above these with room for floating-point variation.
CONVERGENCE_TOLERANCE = {10: 0.25, 50: 0.05, 100: 0.03, 500: 0.01, 1000: 0.005}


@pytest.mark.parametrize("n", sorted(CONVERGENCE_TOLERANCE))
def test_converges_to_black_scholes_call(n):
    bs = bs_price(S0, K0, T0, R0, SIGMA0, "call")
    tree = binomial_price(S0, K0, T0, R0, SIGMA0, n, "call")
    assert abs(tree - bs) < CONVERGENCE_TOLERANCE[n]


def test_converges_to_black_scholes_put_at_1000_steps():
    bs = bs_price(S0, K0, T0, R0, SIGMA0, "put")
    tree = binomial_price(S0, K0, T0, R0, SIGMA0, 1000, "put")
    assert tree == pytest.approx(bs, abs=5e-3)


def test_error_shrinks_with_more_steps():
    bs = bs_price(S0, K0, T0, R0, SIGMA0, "call")
    err_10 = abs(binomial_price(S0, K0, T0, R0, SIGMA0, 10, "call") - bs)
    err_1000 = abs(binomial_price(S0, K0, T0, R0, SIGMA0, 1000, "call") - bs)
    assert err_1000 < err_10


def test_put_call_parity_holds_on_tree():
    call = binomial_price(S0, K0, T0, R0, SIGMA0, 200, "call")
    put = binomial_price(S0, K0, T0, R0, SIGMA0, 200, "put")
    assert call - put == pytest.approx(S0 - K0 * np.exp(-R0 * T0), abs=1e-9)


def test_prices_are_nonnegative():
    assert binomial_price(50.0, 100.0, 1.0, 0.02, 0.3, 100, "call") >= 0
    assert binomial_price(150.0, 100.0, 1.0, 0.02, 0.3, 100, "put") >= 0


@pytest.mark.parametrize("kwargs", [
    dict(S=0.0, K=100.0, T=1.0, r=0.05, sigma=0.2, n_steps=10),
    dict(S=100.0, K=100.0, T=0.0, r=0.05, sigma=0.2, n_steps=10),
    dict(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.0, n_steps=10),
    dict(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2, n_steps=0),
    dict(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2, n_steps=2.5),
])
def test_invalid_inputs_raise(kwargs):
    with pytest.raises(ValueError):
        binomial_price(option_type="call", **kwargs)


def test_unknown_option_type_raises():
    with pytest.raises(ValueError):
        binomial_price(S0, K0, T0, R0, SIGMA0, 10, "straddle")


def test_probability_out_of_range_raises():
    # Large rate with very low volatility and one step makes p > 1, which is not a valid tree.
    with pytest.raises(ValueError):
        binomial_price(100.0, 100.0, 1.0, 0.5, 0.01, 1, "call")
