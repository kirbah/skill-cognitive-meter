from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills"
TARGETS = [
    ROOT / ".claude" / "skills",
    ROOT / ".agent" / "skills",
]

for target in TARGETS:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    for skill_dir in SRC.iterdir():
        if skill_dir.is_dir():
            shutil.copytree(skill_dir, target / skill_dir.name)