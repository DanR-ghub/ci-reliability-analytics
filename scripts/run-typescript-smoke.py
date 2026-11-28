import argparse
import os
import platform
import subprocess
import time
from pathlib import Path


TYPESCRIPT_SHA = "399a95c9715b0cdf77aa8a23cf9cf557d8585b41"
COMPILER_CHECK = ("./built/local/tsc", "-p", "./tsc/testdata/fixtures/compiler", "--noEmit")
STEPS = (
    ("Install locked dependencies", ("npm", "ci")),
    ("Build the compiler with race detection", ("./node_modules/.bin/hereby", "build", "--race")),
    ("Compile the fixture in single-threaded mode", (*COMPILER_CHECK, "--singleThreaded")),
    ("Compile the fixture with the default settings", COMPILER_CHECK),
)


def run_baseline(checkout):
    revision = subprocess.check_output(
        ("git", "rev-parse", "--verify", "HEAD"), cwd=checkout, text=True
    ).strip()
    if revision != TYPESCRIPT_SHA:
        raise SystemExit(f"Expected TypeScript {TYPESCRIPT_SHA}, got {revision}")

    status = subprocess.check_output(("git", "status", "--porcelain"), cwd=checkout, text=True)
    if status.strip():
        raise SystemExit("Use a clean TypeScript checkout for the baseline.")

    print(f"TypeScript revision: {revision}", flush=True)
    image = os.environ.get("ImageOS", "local")
    image_version = os.environ.get("ImageVersion", "unknown")
    print(f"Runner image: {image} {image_version} | {platform.system()} {platform.machine()}", flush=True)
    for label, command, expected in (
        ("Node", ("node", "--version"), "v24.22.1"),
        ("npm", ("npm", "--version"), "11.21.1"),
        ("Go", ("go", "env", "GOVERSION"), "go1.27.2"),
    ):
        actual = subprocess.check_output(command, cwd=checkout, text=True).strip()
        if actual != expected:
            raise SystemExit(f"Expected {label} {expected}, got {actual}")
        print(f"{label}: {actual}", flush=True)

    for label, command in STEPS:
        print(f"\n{label}", flush=True)
        started = time.perf_counter()
        try:
            subprocess.run(command, cwd=checkout, check=True)
        finally:
            print(f"Wall time: {time.perf_counter() - started:.3f} seconds", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the pinned TypeScript smoke baseline.")
    parser.add_argument("checkout", type=Path, help="Root of a clean TypeScript checkout")
    run_baseline(parser.parse_args().checkout.resolve())
