# Convergence to Black-Scholes

Parameters apart from strike: S=100, T=1, r=5%, sigma=20%.

| Case | Option | Steps | Black-Scholes | Tree | Abs. error | Rel. error |
|---|---|---:|---:|---:|---:|---:|
| At the money | call | 10 | 10.45058 | 10.25341 | 0.19717 | 1.89e-02 |
| At the money | call | 50 | 10.45058 | 10.41069 | 0.03989 | 3.82e-03 |
| At the money | call | 100 | 10.45058 | 10.43061 | 0.01997 | 1.91e-03 |
| At the money | call | 500 | 10.45058 | 10.44659 | 0.00400 | 3.83e-04 |
| At the money | call | 1000 | 10.45058 | 10.44858 | 0.00200 | 1.91e-04 |
| At the money | put | 10 | 5.57353 | 5.37635 | 0.19717 | 3.54e-02 |
| At the money | put | 50 | 5.57353 | 5.53363 | 0.03989 | 7.16e-03 |
| At the money | put | 100 | 5.57353 | 5.55355 | 0.01997 | 3.58e-03 |
| At the money | put | 500 | 5.57353 | 5.56953 | 0.00400 | 7.17e-04 |
| At the money | put | 1000 | 5.57353 | 5.57153 | 0.00200 | 3.59e-04 |
| In the money (K=90) | call | 10 | 16.69945 | 16.72216 | 0.02271 | 1.36e-03 |
| In the money (K=90) | call | 50 | 16.69945 | 16.69753 | 0.00191 | 1.15e-04 |
| In the money (K=90) | call | 100 | 16.69945 | 16.71048 | 0.01103 | 6.61e-04 |
| In the money (K=90) | call | 500 | 16.69945 | 16.69871 | 0.00074 | 4.42e-05 |
| In the money (K=90) | call | 1000 | 16.69945 | 16.70038 | 0.00093 | 5.59e-05 |
| In the money (K=90) | put | 10 | 2.31010 | 2.33281 | 0.02271 | 9.83e-03 |
| In the money (K=90) | put | 50 | 2.31010 | 2.30818 | 0.00191 | 8.29e-04 |
| In the money (K=90) | put | 100 | 2.31010 | 2.32113 | 0.01103 | 4.78e-03 |
| In the money (K=90) | put | 500 | 2.31010 | 2.30936 | 0.00074 | 3.20e-04 |
| In the money (K=90) | put | 1000 | 2.31010 | 2.31103 | 0.00093 | 4.04e-04 |
| Out of the money (K=110) | call | 10 | 6.04009 | 6.09918 | 0.05910 | 9.78e-03 |
| Out of the money (K=110) | call | 50 | 6.04009 | 6.06070 | 0.02061 | 3.41e-03 |
| Out of the money (K=110) | call | 100 | 6.04009 | 6.05322 | 0.01314 | 2.17e-03 |
| Out of the money (K=110) | call | 500 | 6.04009 | 6.04222 | 0.00213 | 3.53e-04 |
| Out of the money (K=110) | call | 1000 | 6.04009 | 6.04161 | 0.00152 | 2.52e-04 |
| Out of the money (K=110) | put | 10 | 10.67532 | 10.73442 | 0.05910 | 5.54e-03 |
| Out of the money (K=110) | put | 50 | 10.67532 | 10.69593 | 0.02061 | 1.93e-03 |
| Out of the money (K=110) | put | 100 | 10.67532 | 10.68846 | 0.01314 | 1.23e-03 |
| Out of the money (K=110) | put | 500 | 10.67532 | 10.67746 | 0.00213 | 2.00e-04 |
| Out of the money (K=110) | put | 1000 | 10.67532 | 10.67685 | 0.00152 | 1.43e-04 |
