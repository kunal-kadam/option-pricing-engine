"""Black-Scholes pricing and Greeks for European options (no dividends).

Conventions
-----------
- S: spot price, K: strike, T: time to expiry in years,
  r: continuously compounded risk-free rate, sigma: volatility (annualised).
- Theta is per year (time decay of value as calendar time passes).
- Vega is per unit of volatility (divide by 100 for per volatility point).
- Rho is per unit of the interest rate (divide by 100 for per rate point).

All functions accept scalars or NumPy arrays and broadcast them together.
"""

import math

import numpy as np

_erf = np.frompyfunc(math.erf, 1, 1)
_SQRT_2 = math.sqrt(2.0)
_SQRT_2PI = math.sqrt(2.0 * math.pi)

OPTION_TYPES = ("call", "put")


def _norm_cdf(x):
    """Standard normal CDF, vectorised."""
    erf_values = np.asarray(_erf(np.asarray(x, dtype=float) / _SQRT_2), dtype=float)
    return 0.5 * (1.0 + erf_values)


def _norm_pdf(x):
    """Standard normal PDF, vectorised."""
    x = np.asarray(x, dtype=float)
    return np.exp(-0.5 * x * x) / _SQRT_2PI


def _validate(S, K, T, sigma, option_type):
    if option_type not in OPTION_TYPES:
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")
    S, K, T, sigma = (np.asarray(v, dtype=float) for v in (S, K, T, sigma))
    if np.any(S <= 0) or np.any(K <= 0):
        raise ValueError("S and K must be positive")
    if np.any(T <= 0):
        raise ValueError("T must be positive")
    if np.any(sigma <= 0):
        raise ValueError("sigma must be positive")
    return S, K, T, sigma


def _d1_d2(S, K, T, r, sigma):
    sqrt_T = np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T
    return d1, d2


def price(S, K, T, r, sigma, option_type="call"):
    """Black-Scholes price of a European call or put."""
    S, K, T, sigma = _validate(S, K, T, sigma, option_type)
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    discount = np.exp(-r * T)
    if option_type == "call":
        return S * _norm_cdf(d1) - K * discount * _norm_cdf(d2)
    return K * discount * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def greeks(S, K, T, r, sigma, option_type="call"):
    """Delta, gamma, vega, theta, and rho of a European call or put.

    Returns a dict of NumPy arrays (or floats for scalar inputs).
    """
    S, K, T, sigma = _validate(S, K, T, sigma, option_type)
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    sqrt_T = np.sqrt(T)
    discount = np.exp(-r * T)
    pdf_d1 = _norm_pdf(d1)

    gamma = pdf_d1 / (S * sigma * sqrt_T)
    vega = S * pdf_d1 * sqrt_T
    common_theta = -S * pdf_d1 * sigma / (2.0 * sqrt_T)

    if option_type == "call":
        delta = _norm_cdf(d1)
        theta = common_theta - r * K * discount * _norm_cdf(d2)
        rho = K * T * discount * _norm_cdf(d2)
    else:
        delta = _norm_cdf(d1) - 1.0
        theta = common_theta + r * K * discount * _norm_cdf(-d2)
        rho = -K * T * discount * _norm_cdf(-d2)

    result = {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }
    return {name: value[()] if np.ndim(value) == 0 else value for name, value in result.items()}
