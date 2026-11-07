"""Step 6: validate both pricers against published worked examples.

Run from the project root:

    python validation/textbook_validation.py

Writes validation/textbook_results.csv and validation/textbook_results.md.

Sources: problems and reference prices from a published set of solutions to
Black-Scholes homework (fac.ksu.edu.sa, sol_hw_4_actu_468_ctm-bsf1.pdf).
Only examples with no dividend yield, no foreign rate and no discrete dividend
are used, because the pricer does not model those.
"""

import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from option_pricing.binomial import price as tree_price  # noqa: E402
from option_pricing.black_scholes import price as bs_price  # noqa: E402

BINOMIAL_STEPS = 1000
SOURCE = "KSU homework solutions (sol_hw_4_actu_468_ctm-bsf1.pdf)"
HULL_CH15 = "Hull, Options, Futures and Other Derivatives, 9th ed., Chapter 15"

# Each entry: name, inputs, option type, published price, and the published value's rounding.
EXAMPLES = [
    {
        "name": "Problem 1.1: call",
        "S": 52.0, "K": 50.0, "T": 0.25, "r": 0.12, "sigma": 0.30,
        "option": "call", "published": 5.0543, "rounding": 0.00005,
    },
    {
        "name": "Problem 1.2: put",
        "S": 69.0, "K": 70.0, "T": 0.5, "r": 0.05, "sigma": 0.35,
        "option": "put", "published": 6.4020, "rounding": 0.00005,
    },
    {
        # Problem 4.1b restates the 4.1a case with the dividend yield absorbed into
        # the spot and strike (r=0, no dividend). Price stated as 14.392.
        "name": "Problem 4.1b: call (dividend absorbed)",
        "S": 100.0 * 2.718281828459045 ** (-0.0225),
        "K": 95.0 * 2.718281828459045 ** (-0.06),
        "T": 0.75, "r": 0.0, "sigma": 0.30,
        "option": "call", "published": 14.392, "rounding": 0.0005,
    },
    {
        # Problem 4.2b: the forward price F0 = 103.82 is used as the spot,
        # expressed as S = F0 * e^(-rT) so the standard formula reproduces it.
        "name": "Problem 4.2b: call (forward price)",
        "S": 103.82 * 2.718281828459045 ** (-0.08 * 0.75),
        "K": 95.0, "T": 0.75, "r": 0.08, "sigma": 0.30,
        "option": "call", "published": 14.392, "rounding": 0.0005,
    },
    # Hull, Options, Futures and Other Derivatives (9th ed.), Chapter 15, Example 15.6.
    {
        "name": "Hull Example 15.6: call",
        "S": 42.0, "K": 40.0, "T": 0.5, "r": 0.10, "sigma": 0.20,
        "option": "call", "published": 4.76, "rounding": 0.005,
        "source": HULL_CH15,
    },
    {
        "name": "Hull Example 15.6: put",
        "S": 42.0, "K": 40.0, "T": 0.5, "r": 0.10, "sigma": 0.20,
        "option": "put", "published": 0.81, "rounding": 0.005,
        "source": HULL_CH15,
    },
    # Hull Chapter 15, Example 15.7 (the value of a five-year European call used in a warrant example).
    {
        "name": "Hull Example 15.7: 5-year call",
        "S": 40.0, "K": 60.0, "T": 5.0, "r": 0.03, "sigma": 0.30,
        "option": "call", "published": 7.04, "rounding": 0.005,
        "source": HULL_CH15,
    },
    # Hull Chapter 15, implied volatility section: a call priced at 1.875 has implied volatility 0.235.
    # The volatility is published to 3 decimals; vega * 0.0005 is the price uncertainty from that rounding.
    {
        "name": "Hull implied volatility example: call",
        "S": 21.0, "K": 20.0, "T": 0.25, "r": 0.10, "sigma": 0.235,
        "option": "call", "published": 1.875, "rounding": 0.0017,
        "source": HULL_CH15,
    },
]


def run():
    rows = []
    for ex in EXAMPLES:
        args = dict(S=ex["S"], K=ex["K"], T=ex["T"], r=ex["r"], sigma=ex["sigma"])
        bs = bs_price(option_type=ex["option"], **args)
        tree = tree_price(n_steps=BINOMIAL_STEPS, option_type=ex["option"], **args)
        published = ex["published"]
        for method, value in (("Black-Scholes", bs), (f"Binomial ({BINOMIAL_STEPS} steps)", tree)):
            abs_err = abs(value - published)
            rows.append({
                "example": ex["name"],
                "method": method,
                "published": published,
                "computed": value,
                "abs_error": abs_err,
                "rel_error": abs_err / published,
                "rounding_tolerance": ex["rounding"],
                "within_rounding": abs_err <= ex["rounding"] + 1e-9,
                "source": ex.get("source", SOURCE),
            })
    return rows


def write_outputs(rows):
    out_dir = ROOT / "validation"
    fields = ["example", "method", "published", "computed", "abs_error", "rel_error",
              "rounding_tolerance", "within_rounding", "source"]
    with open(out_dir / "textbook_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Validation against published worked examples",
        "",
        f"Source: {SOURCE}. Binomial uses {BINOMIAL_STEPS} steps.",
        "",
        "| Example | Method | Published | Computed | Abs. error | Rel. error | Within rounding |",
        "|---|---|---:|---:|---:|---:|:---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['example']} | {r['method']} | {r['published']:.4f} | {r['computed']:.5f} | "
            f"{r['abs_error']:.5f} | {r['rel_error']:.2e} | {'yes' if r['within_rounding'] else 'no'} |"
        )
    (out_dir / "textbook_results.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    results = run()
    write_outputs(results)
    for r in results:
        print(f"{r['example']:40s} {r['method']:26s} pub={r['published']:.4f} "
              f"comp={r['computed']:.5f} abs={r['abs_error']:.5f} rel={r['rel_error']:.2e} "
              f"within_rounding={r['within_rounding']}")
