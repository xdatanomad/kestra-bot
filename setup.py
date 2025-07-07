import sys
import asyncio
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"


def check_python_version():
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8 or higher is required.")

async def create_dirs():
    data_dir = DATA_DIR
    tmp_dir = data_dir / "tmp"
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created dirs")


def setup():
    # check Python version
    check_python_version()
    # setup
    asyncio.run(create_dirs())
    print("Setup complete.")


if __name__ == "__main__":
    setup()
    