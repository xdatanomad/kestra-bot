import sys
import asyncio
from pathlib import Path
import shutil
from setuptools import setup, find_packages


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


# PyPI package configuration
setup(
    name="kestra-bot-demo",
    version="0.1.0",
    description="A Textual terminal application for building Kestra ETL Flows using OpenAI agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Parham Parvizi",
    author_email="parham.parvizi@gmail.com",
    packages=find_packages(),
    install_requires=[
        "textual>=0.40.0",
    ],
    entry_points={
        "console_scripts": [
            "kestra-bot=kestra_demo.app:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: System :: System Shells",
    ],
)


if __name__ == "__main__":
    setup()
