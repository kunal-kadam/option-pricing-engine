# Cox-Ross-Rubinstein Binomial Tree Pricer

This document explains `src/option_pricing/binomial.py`: what the function does, how to call it, the method behind it, and how we checked that it is correct.

## Contents

- Conventions
- Public function
- Method
- Implementation notes
- Correctness checks
- Known limitations

## Conventions

The inputs use the same units as the Black-Scholes code (see `docs/black-scholes.md`):

| Symbol | Meaning | Unit |
|---|---|---|
| `S` | Spot price | currency |
| `K` | Strike price | currency |
| `T` | Time to expiry | years |
| `r` | Continuously compounded risk-free rate | decimal (0.05 = 5%) |
| `sigma` | Volatility | annualised decimal (0.20 = 20%) |
| `n_steps` | Number of time steps in the tree | positive integer |

The pricer values European options only, with no dividends.

## Public function

### `price(S, K, T, r, sigma, n_steps, option_type="call")`

Returns the price of a European call or put as a Python float.

```python
from option_pricing.binomial import price

price(100, 100, 1.0, 0.05, 0.20, 1000, "call")   # 10.4486
price(100, 100, 1.0, 0.05, 0.20, 1000, "put")    # 5.5715
```

Unlike the Black-Scholes functions, this takes one set of scalar inputs per call. To price many options, loop over them or use the Black-Scholes code for European options, which is vectorised.

### Input validation

The function raises `ValueError` when:

- `option_type` is not `"call"` or `"put"`
- `S`, `K`, `T`, or `sigma` is zero or negative
- `n_steps` is not a positive whole number
- the risk-neutral probability falls outside (0, 1), which means the tree cannot represent the market at that step count. The fix is to increase `n_steps`.

`r` can be negative. It is not validated.

## Method

The tree divides the time to expiry `T` into `n` steps of length `dt = T / n`. At each step the asset price moves up by a factor `u` or down by `d`:

$$
u = e^{\sigma\sqrt{dt}}, \qquad d = \frac{1}{u}
$$

The risk-neutral probability of an up move is

$$
p = \frac{e^{r\,dt} - d}{u - d}
$$

Pricing runs in two stages:

1. **Terminal payoffs.** After `n` steps, the tree has `n + 1` nodes. Node `j` has had `j` up moves, so its price is $S\,u^{j}d^{\,n-j} = S\,u^{2j-n}$. The payoff at each node is $\max(S_T - K, 0)$ for a call or $\max(K - S_T, 0)$ for a put.
2. **Backward induction.** Working back from expiry, each node takes the discounted risk-neutral average of its two successors:

$$
V_{i,j} = e^{-r\,dt}\left[p\,V_{i+1,j+1} + (1-p)\,V_{i+1,j}\right]
$$

The value at the first node, `V_{0,0}`, is the option price.

As `n` grows, the tree converges to the Black-Scholes price.

## Implementation notes

- **Vectorised layers.** Each backward step is one NumPy operation on the whole layer of nodes, so the cost per step is small.
- **No explicit price tree.** The code stores only the current layer of values, which is `n + 1` numbers, rather than the full tree of about `n²/2` nodes.
- **Return type.** The result is a plain Python float.

## Correctness checks

1. **Hand calculation.** With one step, the price matches a direct calculation of the discounted risk-neutral payoff.
2. **Naive implementation.** Over 200 random cases (random spot, strike, maturity, rate, volatility, step count from 1 to 60, calls and puts), the vectorised code agrees with a separate, loop-based tree to within 1.3e-13.
3. **Convergence to Black-Scholes.** For the reference case (S=100, K=100, T=1, r=5%, σ=20%), the error against the Black-Scholes call price is shown below. The call and put errors are equal at each step count.

| Steps | Tree price | Absolute error |
|---|---|---|
| 10 | 10.25341 | 0.197 |
| 50 | 10.41069 | 0.040 |
| 100 | 10.43061 | 0.020 |
| 500 | 10.44659 | 0.004 |
| 1000 | 10.44858 | 0.002 |
| 10000 | 10.45038 | 0.0002 |

4. **Random convergence check.** Over 100 random cases with 2,000 steps, the largest difference from Black-Scholes was 2.7e-3.
5. **Put-call parity.** Holds on the tree, since payoffs and discounting are linear. Tested at 200 steps.
6. **Probability check.** A case with a large rate and very low volatility, where the probability falls above 1, raises the expected error.

Conclusion: the tree follows the CRR method, its values match a naive implementation to floating-point precision, and it converges to Black-Scholes as the step count grows.

## Known limitations

- **Slow convergence.** The error falls roughly in proportion to `1/n`, and it oscillates between step counts. Accuracy at a given step count is coarser than Black-Scholes, which is why the tree is used here as a benchmark rather than the main pricer.
- **European options only.** Early exercise, as used for American options, would need an extra check at each node. It is out of scope.
- **No dividends.** The model would need a dividend yield to price options on dividend-paying stocks.
- **Large exponents.** The terminal prices use `u` raised to a power of up to `n`. For very high volatility, very long maturity, or very large `n`, this can overflow. The code does not guard against it.
- **Speed.** A 1,000-step price takes about 2 ms, and 10,000 steps take about 0.15 s. Step 7 will measure these properly.
