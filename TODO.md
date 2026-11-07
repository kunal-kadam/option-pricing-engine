# TODO: model work

## Dividends

- [ ] Add a continuous dividend yield `q` to Black-Scholes (S discounted by e^(-qT) in d₁ and d₂; Greeks updated to match).
- [ ] Add `q` to the binomial tree (risk-neutral probability p = (e^((r−q)Δt) − d) / (u − d)).
- [ ] Add discrete dividends (present value subtracted from the spot, as in Hull's Example 15.9).
- [ ] Update `docs/black-scholes.md` and `docs/binomial-tree.md` to describe dividend support and remove the "no dividends" limitation.

## Binomial pricer generalisation

- [ ] Generalise the binomial pricer to accept any u and d, with the same backward induction. CRR becomes a special case (d = 1/u).
- [ ] Add tests for the generalised tree, including that the case d = 1/u matches CRR exactly.
- [ ] Update `docs/binomial-tree.md` to describe the general tree.

## Step 6: open questions

- [ ] **Problem 1.1 discrepancy.** The solutions set gives 5.0543, but the standard formula gives 5.0574, and rounding the intermediate values doesn't close the gap. Confirm the correct value against Hull's book. If the solutions set is wrong, remove the example and record why.
- [ ] **Implied-volatility tree miss.** The 1,000-step binomial price is 0.00179 from the published 1.875, against a tolerance of 0.0017. The tolerance is my estimate of how much the rounded volatility (0.235) can move the price. Check whether that estimate is right, and whether the tree needs more steps for this case.
- [ ] **Source reliability.** Four of the examples come from an unofficial set of homework solutions, not from Hull. Problems 4.1b and 4.2b are reworked inputs (a dividend absorbed into the spot, and a forward price), so they test a transformed version of the problem, not the original.
- [ ] **Rounding tolerances.** Each tolerance was set by hand from the number of decimals printed in the source. Decide on one consistent rule and record it in the validation file.
- [ ] **Step count.** The validation uses 1,000 steps, but the tree's error oscillates between step counts. Check whether the results hold at a few other step counts, such as 500 and 2,000.
- [ ] **Page references.** The Chapter 15 examples are cited by example number, but the results file doesn't record page numbers. Add them (pages 338 to 339 for Example 15.6, page 341 for Example 15.7 and the implied-volatility example).
- [ ] **Excluded examples.** Hull's Example 15.9 (call price 3.67) uses dividends, and Chapter 13's three examples use an asymmetric tree. Add these once dividend support and the generalised binomial pricer are in place.