"""Download NASA's C-MAPSS benchmark archive into the ignored data/raw folder."""
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
destination = ROOT / "data" / "raw" / "CMAPSSData.zip"
destination.parent.mkdir(parents=True, exist_ok=True)
url = "https://zenodo.org/records/15346912/files/CMAPSSData.zip?download=1"
if not destination.exists():
    print(f"Downloading NASA C-MAPSS data to {destination}")
    urlretrieve(url, destination)
else:
    print(f"Dataset archive already exists: {destination}")

