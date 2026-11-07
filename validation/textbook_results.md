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
