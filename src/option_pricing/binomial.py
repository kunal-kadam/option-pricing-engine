"""Cox-Ross-Rubinstein (CRR) binomial tree pricer for European options (no dividends).

Uses the same conventions as ``option_pricing.black_scholes``:
S spot, K strike, T years to expiry, r continuously compounded rate, sigma volatility.
"""

import numpy as np

OPTION_TYPES = ("call", "put")


def price(S, K, T, r, sigma, n_steps, option_type="call"):
    """Price a European call or put on a CRR binomial tree with ``n_steps`` steps."""
    if option_type not in OPTION_TYPES:
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive")
    if T <= 0:
        raise ValueError("T must be positive")
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if int(n_steps) != n_steps or n_steps < 1:
        raise ValueError("n_steps must be a positive integer")
    n = int(n_steps)

    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    discount = np.exp(-r * dt)
    p = (np.exp(r * dt) - d) / (u - d)
    if not 0.0 < p < 1.0:
        raise ValueError(
            f"risk-neutral probability {p:.4f} is outside (0, 1); increase n_steps"
        )

    # Terminal asset prices: node j (0..n) has j up-moves, so S * u^j * d^(n-j) = S * u^(2j-n).
    j = np.arange(n + 1)
    terminal_prices = S * u ** (2 * j - n)
    if option_type == "call":
        values = np.maximum(terminal_prices - K, 0.0)
    else:
        values = np.maximum(K - terminal_prices, 0.0)

    # Backward induction: each step discounts the risk-neutral expectation of the next layer.
    for _ in range(n):
        values = discount * (p * values[1:] + (1.0 - p) * values[:-1])
    return float(values[0])
