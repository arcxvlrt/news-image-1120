"""Copy the prebuilt entry.png to /output/entry.png. No network; output is byte-identical every run."""
import os
import shutil
from pathlib import Path

# OUTPUT_DIR is only for local testing; the bounty runner uses the default /output.
out = Path(os.environ.get("OUTPUT_DIR", "/output"))
out.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(__file__).resolve().parent / "entry.png", out / "entry.png")
