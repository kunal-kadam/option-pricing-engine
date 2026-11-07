# Option Pricing Engine

Pricing and sensitivity analysis for European options, built with Python, NumPy, and pytest. It includes:

- Black-Scholes-Merton pricing and the Greeks (delta, gamma, vega, theta, rho) for European calls and puts, vectorised with NumPy
- A Cox-Ross-Rubinstein (CRR) binomial tree pricer, used as an independent benchmark
- Tests for put-call parity, arbitrage bounds, finite-difference Greeks, and convergence
- Validation against published worked examples, with absolute and relative errors
- Runtime measurements for single prices, batches, and the tree at several step counts

Dividends are not yet supported. See [TODO.md](TODO.md).

## Methods

### Black-Scholes-Merton

With d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T) and d₂ = d₁ − σ√T:

- Call: C = S·N(d₁) − K·e^(−rT)·N(d₂)
- Put: P = K·e^(−rT)·N(−d₂) − S·N(−d₁)

Greeks are closed-form (see [docs/black-scholes.md](docs/black-scholes.md)). Vega is per unit of volatility, and theta is per year.

### Cox-Ross-Rubinstein binomial tree

The tree uses u = e^(σ√Δt), d = 1/u, and risk-neutral probability p = (e^(rΔt) − d) / (u − d). Prices are found by backward induction from the terminal payoffs (see [docs/binomial-tree.md](docs/binomial-tree.md)).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Requires Python 3.10 or newer.

## Usage

```python
from option_pricing.black_scholes import price, greeks
from option_pricing.binomial import price as tree_price

price(100, 100, 1.0, 0.05, 0.20, "call")        # 10.4506
greeks(100, 100, 1.0, 0.05, 0.20, "call")       # dict with delta, gamma, vega, theta, rho
tree_price(100, 100, 1.0, 0.05, 0.20, 1000, "call")  # 10.4486
```

Black-Scholes accepts NumPy arrays for batch pricing. The tree prices one option per call.

## Running the tests

```bash
pytest
```

All 65 tests should pass.

## Validation

### Published worked examples

Both methods were checked against eight published European option prices. Four come from a published set of homework solutions, and four come from Hull's *Options, Futures, and Other Derivatives* (9th edition), Chapter 15. The binomial tree uses 1,000 steps.

| Example | Method | Published | Computed | Abs. error | Rel. error |
|---|---|---:|---:|---:|---:|
| Hull 15.6: call | Black-Scholes | 4.7600 | 4.75942 | 0.00058 | 1.21e-04 |
| Hull 15.6: call | Binomial | 4.7600 | 4.75982 | 0.00018 | 3.84e-05 |
| Hull 15.6: put | Black-Scholes | 0.8100 | 0.80860 | 0.00140 | 1.73e-03 |
| Hull 15.6: put | Binomial | 0.8100 | 0.80899 | 0.00101 | 1.24e-03 |
| Hull 15.7: 5-year call | Black-Scholes | 7.0400 | 7.04024 | 0.00024 | 3.40e-05 |
| Hull 15.7: 5-year call | Binomial | 7.0400 | 7.04205 | 0.00205 | 2.91e-04 |
| Hull implied volatility example: call | Black-Scholes | 1.8750 | 1.87661 | 0.00161 | 8.59e-04 |
| Hull implied volatility example: call | Binomial | 1.8750 | 1.87679 | 0.00179 | 9.55e-04 |

The four solution-set examples (Problems 1.1, 1.2, 4.1b, and 4.2b) are in [validation/textbook_results.md](validation/textbook_results.md). Their errors are between 0.001 and 0.006, and they fall outside the printed rounding. Problem 1.1 is still being checked, since the solutions set's value differs from the standard formula.

The full table, with rounding tolerances and a within-rounding flag for each row, is in [validation/textbook_results.md](validation/textbook_results.md). Run `python validation/textbook_validation.py` to regenerate it.

### Convergence of the tree

The tree converges to Black-Scholes as the step count increases. At the money, the error falls roughly in proportion to 1/n:

| Steps | Abs. error (call, at the money) |
|---:|---:|
| 10 | 0.19717 |
| 50 | 0.03989 |
| 100 | 0.01997 |
| 500 | 0.00400 |
| 1,000 | 0.00200 |

For in-the-money and out-of-the-money strikes, the error falls overall but not at every step count. The tree's error oscillates when the strike does not sit on the tree's price grid. Results for all three cases are in [validation/convergence_results.md](validation/convergence_results.md). Run `python validation/convergence.py` to regenerate them.

## Performance

Median of seven runs after a warm-up, on Linux with Python 3.13 and NumPy 2.5. Results are in [benchmarks/runtime_results.md](benchmarks/runtime_results.md).

| Case | Median time |
|---|---:|
| Black-Scholes, single price | 21 µs |
| Black-Scholes, batch of 10,000 (vectorised) | 1.7 ms (0.17 µs per option) |
| Binomial tree, single price, 100 steps | 0.22 ms |
| Binomial tree, single price, 1,000 steps | 2.6 ms |
| Binomial tree, single price, 10,000 steps | 0.20 s |
| Binomial tree, batch of 10,000 (100 steps each) | 2.1 s |

Black-Scholes is much faster for batches because it is vectorised across the array. The tree prices one option per loop, so its batch time grows with the number of options. Timings depend on the machine. Run `python benchmarks/runtime.py` to measure your own.

## Limitations

- **European options only.** The tree does not handle early exercise.
- **No dividends.** Both pricers assume the underlying pays no dividends. Dividend support is planned (see [TODO.md](TODO.md)).
- **Tiny negative prices.** Deep out-of-the-money options can return values such as −3e−15 through floating-point cancellation. Treat values below zero as zero when displaying prices.

## Project layout

```
src/option_pricing/     pricing code (black_scholes.py, binomial.py)
tests/                  pytest suite
validation/             published-example checks and convergence study
benchmarks/             runtime measurements
docs/                   method notes and correctness checks
```

## References

- J. C. Hull, *Options, Futures, and Other Derivatives*, 9th edition (Global Edition). Chapter 13 (binomial trees), Chapter 15 (the Black-Scholes-Merton model), including Examples 15.6 and 15.7 and the implied-volatility example.
- J. C. Cox, S. A. Ross, and M. Rubinstein, "Option Pricing: A Simplified Approach," *Journal of Financial Economics*, 1979. Source of the CRR tree construction.
- F. Black and M. Scholes, "The Pricing of Options and Corporate Liabilities," *Journal of Political Economy*, 1973.
- R. C. Merton, "Theory of Rational Option Pricing," *Bell Journal of Economics and Management Science*, 1973.
- Published solutions to Black-Scholes homework problems (fac.ksu.edu.sa, sol_hw_4_actu_468_ctm-bsf1.pdf), used for four of the validation examples.

## License

To be added before publication.
