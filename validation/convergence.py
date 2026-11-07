"""Step 5: convergence of the Cox-Ross-Rubinstein tree to Black-Scholes.

Run from the project root:

    python validation/convergence.py

Writes validation/convergence_results.csv and validation/convergence_results.md.
"""

import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from option_pricing.binomial import price as tree_price  # noqa: E402
from option_pricing.black_scholes import price as bs_price  # noqa: E402

STEP_COUNTS = [10, 50, 100, 500, 1000]

CASES = {
    "At the money": dict(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.20),
    "In the money (K=90)": dict(S=100.0, K=90.0, T=1.0, r=0.05, sigma=0.20),
    "Out of the money (K=110)": dict(S=100.0, K=110.0, T=1.0, r=0.05, sigma=0.20),
}
OPTION_TYPES = ("call", "put")


def run():
    rows = []
    for case_name, params in CASES.items():
        for option_type in OPTION_TYPES:
            reference = bs_price(option_type=option_type, **params)
            for n in STEP_COUNTS:
                tree = tree_price(n_steps=n, option_type=option_type, **params)
                abs_err = abs(tree - reference)
                rows.append({
                    "case": case_name,
                    "option": option_type,
                    "steps": n,
                    "black_scholes": reference,
                    "tree": tree,
                    "abs_error": abs_err,
                    "rel_error": abs_err / reference,
                })
    return rows


def write_outputs(rows):
    out_dir = ROOT / "validation"
    fields = ["case", "option", "steps", "black_scholes", "tree", "abs_error", "rel_error"]

    with open(out_dir / "convergence_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Convergence to Black-Scholes",
        "",
        "Parameters apart from strike: S=100, T=1, r=5%, sigma=20%.",
        "",
        "| Case | Option | Steps | Black-Scholes | Tree | Abs. error | Rel. error |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['case']} | {r['option']} | {r['steps']} | {r['black_scholes']:.5f} | "
            f"{r['tree']:.5f} | {r['abs_error']:.5f} | {r['rel_error']:.2e} |"
        )
    (out_dir / "convergence_results.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    results = run()
    write_outputs(results)
    for r in results:
        print(f"{r['case']:28s} {r['option']:4s} n={r['steps']:5d} "
              f"tree={r['tree']:.5f} bs={r['black_scholes']:.5f} "
              f"abs={r['abs_error']:.5f} rel={r['rel_error']:.2e}")
