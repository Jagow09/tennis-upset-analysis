import subprocess
import sys

scripts = [
    "src/01_scrape.py",
    "src/02_clean.py",
    "src/03_analysis.py",
    "src/04_figures.py"
]

print("Running full tennis upsets pipeline...\n")

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error in {script}:")
        print(result.stderr)
        break
    else:
        print(f"{script} completed successfully\n")

print("Pipeline complete!")
