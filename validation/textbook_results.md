# Validation against published worked examples

Source: KSU homework solutions (sol_hw_4_actu_468_ctm-bsf1.pdf). Binomial uses 1000 steps.

| Example | Method | Published | Computed | Abs. error | Rel. error | Within rounding |
|---|---|---:|---:|---:|---:|:---:|
| Problem 1.1: call | Black-Scholes | 5.0543 | 5.05739 | 0.00309 | 6.11e-04 | no |
| Problem 1.1: call | Binomial (1000 steps) | 5.0543 | 5.05731 | 0.00301 | 5.96e-04 | no |
| Problem 1.2: put | Black-Scholes | 6.4020 | 6.40141 | 0.00059 | 9.25e-05 | no |
| Problem 1.2: put | Binomial (1000 steps) | 6.4020 | 6.40069 | 0.00131 | 2.05e-04 | no |
| Problem 4.1b: call (dividend absorbed) | Black-Scholes | 14.3920 | 14.38630 | 0.00570 | 3.96e-04 | no |
| Problem 4.1b: call (dividend absorbed) | Binomial (1000 steps) | 14.3920 | 14.38830 | 0.00370 | 2.57e-04 | no |
| Problem 4.2b: call (forward price) | Black-Scholes | 14.3920 | 14.38553 | 0.00647 | 4.49e-04 | no |
| Problem 4.2b: call (forward price) | Binomial (1000 steps) | 14.3920 | 14.38656 | 0.00544 | 3.78e-04 | no |
| Hull Example 15.6: call | Black-Scholes | 4.7600 | 4.75942 | 0.00058 | 1.21e-04 | yes |
| Hull Example 15.6: call | Binomial (1000 steps) | 4.7600 | 4.75982 | 0.00018 | 3.84e-05 | yes |
| Hull Example 15.6: put | Black-Scholes | 0.8100 | 0.80860 | 0.00140 | 1.73e-03 | yes |
| Hull Example 15.6: put | Binomial (1000 steps) | 0.8100 | 0.80899 | 0.00101 | 1.24e-03 | yes |
| Hull Example 15.7: 5-year call | Black-Scholes | 7.0400 | 7.04024 | 0.00024 | 3.40e-05 | yes |
| Hull Example 15.7: 5-year call | Binomial (1000 steps) | 7.0400 | 7.04205 | 0.00205 | 2.91e-04 | yes |
| Hull implied volatility example: call | Black-Scholes | 1.8750 | 1.87661 | 0.00161 | 8.59e-04 | yes |
| Hull implied volatility example: call | Binomial (1000 steps) | 1.8750 | 1.87679 | 0.00179 | 9.55e-04 | no |
