"""Step 7: runtime of the pricers.

Run from the project root:

    python benchmarks/runtime.py

Each case is repeated REPEATS times and the median is reported. Writes
benchmarks/runtime_results.csv and benchmarks/runtime_results.md.
"""

import csv
import pathlib
import platform
import statistics
import sys
import time

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from option_pricing.binomial import price as tree_price  # noqa: E402
from option_pricing.black_scholes import price as bs_price  # noqa: E402

REPEATS = 7
BATCH_SIZE = 10_000
TREE_STEPS = [10, 50, 100, 500, 1000, 10_000]
BATCH_TREE_STEPS = 100  # binomial batch uses a moderate step count; see README

RNG = np.random.default_rng(12345)
S_BATCH = RNG.uniform(50, 150, BATCH_SIZE)
K_BATCH = RNG.uniform(50, 150, BATCH_SIZE)
T_BATCH = RNG.uniform(0.05, 3.0, BATCH_SIZE)
R_BATCH = RNG.uniform(0.0, 0.08, BATCH_SIZE)
SIGMA_BATCH = RNG.uniform(0.05, 0.6, BATCH_SIZE)


def time_median(fn, repeats=REPEATS):
    """Median wall-clock seconds over repeats, after one untimed warm-up call."""
    fn()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return statistics.median(samples), min(samples), max(samples)


def cases():
    yield ("Black-Scholes, single price", 1,
           lambda: bs_price(100.0, 100.0, 1.0, 0.05, 0.20, "call"))
    yield ("Black-Scholes, batch of 10,000 (vectorised)", BATCH_SIZE,
           lambda: bs_price(S_BATCH, K_BATCH, T_BATCH, R_BATCH, SIGMA_BATCH, "call"))
    for n in TREE_STEPS:
        yield (f"Binomial tree, single price, {n} steps", 1,
               lambda n=n: tree_price(100.0, 100.0, 1.0, 0.05, 0.20, n, "call"))

    def tree_batch():
        for i in range(BATCH_SIZE):
            tree_price(S_BATCH[i], K_BATCH[i], T_BATCH[i], R_BATCH[i], SIGMA_BATCH[i],
                       BATCH_TREE_STEPS, "call")

    yield (f"Binomial tree, batch of 10,000 ({BATCH_TREE_STEPS} steps each, looped)",
           BATCH_SIZE, tree_batch)


def run():
    rows = []
    for name, n_options, fn in cases():
        median, fastest, slowest = time_median(fn)
        rows.append({
            "case": name,
            "options": n_options,
            "median_seconds": median,
            "min_seconds": fastest,
            "max_seconds": slowest,
            "microseconds_per_option": median / n_options * 1e6,
        })
        print(f"{name:72s} median={median:.6f}s  per option={median / n_options * 1e6:.2f} us")
    return rows


def write_outputs(rows):
    out_dir = ROOT / "benchmarks"
    fields = ["case", "options", "median_seconds", "min_seconds", "max_seconds",
              "microseconds_per_option"]
    with open(out_dir / "runtime_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Runtime results",
        "",
        f"Median of {REPEATS} runs after one warm-up. Python {platform.python_version()}, "
        f"NumPy {np.__version__}, {platform.system()} {platform.machine()}.",
        "",
        "| Case | Options | Median (s) | Min (s) | Max (s) | µs per option |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['case']} | {r['options']:,} | {r['median_seconds']:.6f} | "
            f"{r['min_seconds']:.6f} | {r['max_seconds']:.6f} | "
            f"{r['microseconds_per_option']:.2f} |"
        )
    (out_dir / "runtime_results.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    write_outputs(run())
