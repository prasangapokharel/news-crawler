import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE / "core" / "engine" / "1"))

import read

print("=" * 80)
print("SYSTEM PROMPT VERIFICATION")
print("=" * 80)
print()

system_prompt = read.get_system_prompt()

print(system_prompt)
print()
print("=" * 80)
print(f"Total Length: {len(system_prompt)} characters")
print("=" * 80)
