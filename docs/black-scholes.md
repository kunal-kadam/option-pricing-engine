# Black-Scholes Pricing and Greeks

This document explains `src/option_pricing/black_scholes.py`: what each function does, how to call it, the formulas behind it, and how we checked that it is correct.

## Contents

- Conventions and units
- Public functions
- Formulas
- Implementation notes
- Correctness checks
- Known limitations

## Conventions and units

| Symbol | Meaning | Unit |
|---|---|---|
| `S` | Spot price of the underlying | currency |
| `K` | Strike price | currency |
| `T` | Time to expiry | years |
| `r` | Continuously compounded risk-free rate | decimal (0.05 = 5%) |
| `sigma` | Volatility of the underlying | annualised decimal (0.20 = 20%) |

Units of the Greeks:

- **Delta**: change in option price per 1 unit change in `S`.
- **Gamma**: change in delta per 1 unit change in `S`.
- **Vega**: change in option price per 1.0 change in `sigma`. Divide by 100 for the change per volatility point (1%).
- **Theta**: change in option price per year of calendar time. Divide by 365 for the change per day.
- **Rho**: change in option price per 1.0 change in `r`. Divide by 100 for the change per rate point (1%).

The model assumes European exercise and no dividends.

## Public functions

### `price(S, K, T, r, sigma, option_type="call")`

Returns the Black-Scholes price of a European call or put.

```python
from option_pricing.black_scholes import price

price(100, 100, 1.0, 0.05, 0.20, "call")   # 10.4506
price(100, 100, 1.0, 0.05, 0.20, "put")    # 5.5735
```

### `greeks(S, K, T, r, sigma, option_type="call")`

Returns a dictionary with the keys `delta`, `gamma`, `vega`, `theta`, and `rho`.

```python
from option_pricing.black_scholes import greeks

g = greeks(100, 100, 1.0, 0.05, 0.20, "call")
g["delta"]   # 0.6368
g["gamma"]   # 0.018762
g["vega"]    # 37.524
g["theta"]   # -6.4140 (per year)
g["rho"]     # 53.2325
```

### Vectorised use

All inputs can be NumPy arrays. They are broadcast together, so a batch of options is priced in one call:

```python
import numpy as np
from option_pricing.black_scholes import price

S = np.array([90.0, 100.0, 110.0])
price(S, 100.0, 1.0, 0.05, 0.20, "call")   # three prices, one per spot
```

`option_type` is a single string for the whole call. To price a mix of calls and puts, call the function once for each type and combine the results.

### Input validation

The functions raise `ValueError` when:

- `S`, `K`, `T`, or `sigma` is zero or negative
- `option_type` is not `"call"` or `"put"`

`r` can be negative. It is not validated.

## Formulas

With

$$
d_1 = \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \qquad
d_2 = d_1 - \sigma\sqrt{T}
$$

let $N(\cdot)$ be the standard normal CDF and $n(\cdot)$ its PDF.

**Prices**

$$
C = S\,N(d_1) - K e^{-rT} N(d_2), \qquad
P = K e^{-rT} N(-d_2) - S\,N(-d_1)
$$

**Greeks**

| Greek | Call | Put |
|---|---|---|
| Delta | $N(d_1)$ | $N(d_1) - 1$ |
| Gamma | $\dfrac{n(d_1)}{S\sigma\sqrt{T}}$ | same as call |
| Vega | $S\,n(d_1)\sqrt{T}$ | same as call |
| Theta | $-\dfrac{S\,n(d_1)\,\sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)$ | $-\dfrac{S\,n(d_1)\,\sigma}{2\sqrt{T}} + rKe^{-rT}N(-d_2)$ |
| Rho | $KTe^{-rT}N(d_2)$ | $-KTe^{-rT}N(-d_2)$ |

Put-call parity holds for the prices: $C - P = S - Ke^{-rT}$.

## Implementation notes

- **Normal CDF.** NumPy has no error function, so the code applies Python's `math.erf` element by element with `np.frompyfunc`. This keeps the package dependent only on NumPy.
- **Scalar output.** When every input is a scalar, `greeks` returns plain NumPy floats rather than 0-dimensional arrays.
- **Shared intermediates.** `d1`, `d2`, and the discount factor are computed once per call and reused across all Greeks.

## Correctness checks

1. **Textbook values.** For S=100, K=100, T=1, r=5%, σ=20%, the code gives the call price 10.4506, put price 5.5735, and the call Greeks listed above. These match the standard reference values, and the unit tests assert them to 4 decimal places.
2. **Put-call parity.** Tested for single values and for 1,000 random option sets.
3. **Finite differences.** Each Greek is compared with a numerical derivative of the price (central differences on `S`, `sigma`, `T`, and `r`). This is tested for calls and puts at three parameter sets.
4. **Independent implementation.** Over 10,000 random options, the prices and Greeks were compared with a separate implementation built on SciPy's normal distribution. The largest difference was 2.3e-13, which is floating-point rounding.
5. **Symmetry relations.** Put delta equals call delta minus 1, and gamma and vega are identical for calls and puts. Both are tested.

Conclusion: the formulas, signs, and units are correct, and the implementation agrees with the reference to floating-point precision.

## Known limitations

- **Tiny negative prices.** Deep out-of-the-money options can return values such as -3e-15. This is floating-point cancellation, not a modelling error. Treat any value below zero as zero when displaying prices.
- **No dividends.** The model would need a dividend yield `q` to price options on dividend-paying stocks. This is out of scope for the project.
- **No expiry handling.** `T` must be positive. Options at expiry should be valued as their intrinsic value by the caller.
- **Speed.** The erf step runs one Python call per element. The batch of 20,000 options in the check above took 0.003 seconds, which is fast enough for this project. Step 7 will measure it properly.
