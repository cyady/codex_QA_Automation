import subprocess
from datetime import datetime


def run(cmd: str) -> None:
    completed = subprocess.run(cmd, shell=True, check=True)


def test_smoke_home() -> None:
    run("npx vibium navigate https://example.com")
    # Example explicit wait checkpoint (adjust selector for real page):
    # run('npx vibium wait "[data-testid=ready]" --state visible --timeout 10000')
    run("npx vibium text")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run(f"npx vibium screenshot -o shot-{stamp}.png")


if __name__ == "__main__":
    test_smoke_home()
