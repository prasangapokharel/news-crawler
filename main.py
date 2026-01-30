import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "core" / "engine"))

from run import run

if __name__ == "__main__":
    run()
