# Option Pricing Engine

Vectorised pricing and sensitivity analysis for European options, with a Cox-Ross-Rubinstein binomial tree benchmark. Built with Python, NumPy, and pytest.

> Status: in development. Sections on methods, validation, performance, and usage will be filled in as each step is completed.

## Planned contents

- Black-Scholes pricing and Greeks (delta, gamma, vega, theta, rho) for European calls and puts
- Cox-Ross-Rubinstein binomial tree pricer
- Put-call parity and convergence tests
- Validation against published textbook examples, with absolute and relative error
- Runtime measurements for single, batch, and tree pricing

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

```bash
pytest
```

## References

To be added during validation.
