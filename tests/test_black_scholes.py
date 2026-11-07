import numpy as np
import pytest

from option_pricing.black_scholes import greeks, price

# Reference case: S=100, K=100, T=1, r=5%, sigma=20% (standard textbook example).
S0, K0, T0, R0, SIGMA0 = 100.0, 100.0, 1.0, 0.05, 0.20


def test_call_price_matches_reference():
    assert price(S0, K0, T0, R0, SIGMA0, "call") == pytest.approx(10.4506, abs=1e-4)


def test_put_price_matches_reference():
    assert price(S0, K0, T0, R0, SIGMA0, "put") == pytest.approx(5.5735, abs=1e-4)


def test_call_greeks_match_reference():
    g = greeks(S0, K0, T0, R0, SIGMA0, "call")
    assert g["delta"] == pytest.approx(0.6368, abs=1e-4)
    assert g["gamma"] == pytest.approx(0.018762, abs=1e-6)
    assert g["vega"] == pytest.approx(37.524, abs=1e-3)
    assert g["theta"] == pytest.approx(-6.4140, abs=1e-3)
    assert g["rho"] == pytest.approx(53.2325, abs=1e-3)


def test_put_call_parity_scalar():
    call = price(S0, K0, T0, R0, SIGMA0, "call")
    put = price(S0, K0, T0, R0, SIGMA0, "put")
    assert call - put == pytest.approx(S0 - K0 * np.exp(-R0 * T0), abs=1e-10)


def test_put_call_parity_vectorised():
    rng = np.random.default_rng(0)
    S = rng.uniform(50, 150, 1000)
    K = rng.uniform(50, 150, 1000)
    T = rng.uniform(0.01, 3.0, 1000)
    r = rng.uniform(-0.01, 0.10, 1000)
    sigma = rng.uniform(0.05, 0.80, 1000)
    call = price(S, K, T, r, sigma, "call")
    put = price(S, K, T, r, sigma, "put")
    np.testing.assert_allclose(call - put, S - K * np.exp(-r * T), atol=1e-8)


def test_vectorised_matches_scalar():
    S = np.array([90.0, 100.0, 110.0])
    batch = price(S, K0, T0, R0, SIGMA0, "call")
    scalars = [price(s, K0, T0, R0, SIGMA0, "call") for s in S]
    np.testing.assert_allclose(batch, scalars)


def test_prices_are_nonnegative_and_bounded():
    rng = np.random.default_rng(1)
    S = rng.uniform(20, 200, 500)
    K = rng.uniform(20, 200, 500)
    T = rng.uniform(0.01, 5.0, 500)
    sigma = rng.uniform(0.05, 1.0, 500)
    call = price(S, K, T, 0.03, sigma, "call")
    # Deep out-of-the-money prices can come out as -1e-15 from floating-point cancellation.
    assert np.all(call >= -1e-10)
    assert np.all(call <= S + 1e-12)


def test_deep_otm_short_expiry_approaches_intrinsic():
    # Deep in the money at very short expiry: call value is close to S - K discounted.
    value = price(110.0, 100.0, 1e-4, 0.0, 0.2, "call")
    assert value == pytest.approx(10.0, abs=1e-2)


@pytest.mark.parametrize("option_type", ["call", "put"])
@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100.0, 100.0, 1.0, 0.05, 0.20),
    (95.0, 105.0, 0.5, 0.02, 0.35),
    (120.0, 100.0, 2.0, 0.04, 0.15),
])
def test_greeks_match_finite_differences(option_type, S, K, T, r, sigma):
    h = 1e-5
    g = greeks(S, K, T, r, sigma, option_type)

    def v(**kw):
        args = dict(S=S, K=K, T=T, r=r, sigma=sigma)
        args.update(kw)
        return price(args["S"], args["K"], args["T"], args["r"], args["sigma"], option_type)

    delta_fd = (v(S=S + h) - v(S=S - h)) / (2 * h)
    # Second differences need a larger step to avoid rounding noise dominating.
    hs = 1e-2
    gamma_fd = (v(S=S + hs) - 2 * v() + v(S=S - hs)) / (hs * hs)
    vega_fd = (v(sigma=sigma + h) - v(sigma=sigma - h)) / (2 * h)
    theta_fd = -(v(T=T + h) - v(T=T - h)) / (2 * h)
    rho_fd = (v(r=r + h) - v(r=r - h)) / (2 * h)

    assert g["delta"] == pytest.approx(delta_fd, abs=1e-5)
    assert g["gamma"] == pytest.approx(gamma_fd, abs=1e-4)
    assert g["vega"] == pytest.approx(vega_fd, abs=1e-4)
    assert g["theta"] == pytest.approx(theta_fd, abs=1e-4)
    assert g["rho"] == pytest.approx(rho_fd, abs=1e-4)


def test_put_delta_is_call_delta_minus_one():
    call_delta = greeks(S0, K0, T0, R0, SIGMA0, "call")["delta"]
    put_delta = greeks(S0, K0, T0, R0, SIGMA0, "put")["delta"]
    assert put_delta == pytest.approx(call_delta - 1.0, abs=1e-12)


def test_gamma_and_vega_are_same_for_call_and_put():
    call = greeks(S0, K0, T0, R0, SIGMA0, "call")
    put = greeks(S0, K0, T0, R0, SIGMA0, "put")
    assert call["gamma"] == pytest.approx(put["gamma"], abs=1e-12)
    assert call["vega"] == pytest.approx(put["vega"], abs=1e-12)


@pytest.mark.parametrize("kwargs", [
    dict(S=0.0, K=100.0, T=1.0, r=0.05, sigma=0.2),
    dict(S=100.0, K=-1.0, T=1.0, r=0.05, sigma=0.2),
    dict(S=100.0, K=100.0, T=0.0, r=0.05, sigma=0.2),
    dict(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.0),
])
def test_invalid_inputs_raise(kwargs):
    with pytest.raises(ValueError):
        price(option_type="call", **kwargs)


def test_unknown_option_type_raises():
    with pytest.raises(ValueError):
        price(S0, K0, T0, R0, SIGMA0, "straddle")
