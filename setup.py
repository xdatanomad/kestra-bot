import sys
import asyncio
from pathlib import Path
import shutil


DATA_DIR = Path(__file__).parent / "data"


def check_python_version():
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8 or higher is required.")

def create_dirs():
    data_dir = DATA_DIR
    tmp_dir = data_dir / "tmp"
    kestra_wd_dir = data_dir / "kestra-wd"
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    kestra_wd_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created dirs")


def cleanup_dirs():
    tmp_dir = DATA_DIR / "tmp"
    kestra_wd_dir = DATA_DIR / "kestra-wd"
    # Cleanup temporary directory
    if tmp_dir.exists():
        for item in tmp_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        print(f"Cleaned up tmp dir: {tmp_dir}")
    # Cleanup kestra working directory
    if kestra_wd_dir.exists():
        for item in kestra_wd_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        print(f"Cleaned up kestra-wd dir: {kestra_wd_dir}")


def setup():
    # check Python version
    check_python_version()
    # setup
    create_dirs()
    cleanup_dirs()
    print("Setup complete.")


if __name__ == "__main__":
    setup()
    