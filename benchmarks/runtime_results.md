# Runtime results

Median of 7 runs after one warm-up. Python 3.10.10, NumPy 2.2.6, Windows AMD64.

| Case | Options | Median (s) | Min (s) | Max (s) | µs per option |
|---|---:|---:|---:|---:|---:|
| Black-Scholes, single price | 1 | 0.000035 | 0.000033 | 0.000042 | 34.60 |
| Black-Scholes, batch of 10,000 (vectorised) | 10,000 | 0.001820 | 0.001774 | 0.004080 | 0.18 |
| Binomial tree, single price, 10 steps | 1 | 0.000037 | 0.000035 | 0.000057 | 37.20 |
| Binomial tree, single price, 50 steps | 1 | 0.000142 | 0.000141 | 0.000174 | 142.10 |
| Binomial tree, single price, 100 steps | 1 | 0.000268 | 0.000268 | 0.000295 | 268.30 |
| Binomial tree, single price, 500 steps | 1 | 0.001692 | 0.001650 | 0.002948 | 1691.50 |
| Binomial tree, single price, 1000 steps | 1 | 0.004426 | 0.003750 | 0.007696 | 4425.70 |
| Binomial tree, single price, 10000 steps | 1 | 0.150989 | 0.148246 | 0.157152 | 150989.10 |
| Binomial tree, batch of 10,000 (100 steps each, looped) | 10,000 | 2.785758 | 2.718355 | 2.876868 | 278.58 |
