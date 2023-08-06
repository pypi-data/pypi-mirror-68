from pathlib import Path

from setuptools import find_packages, setup

version = "0.0.1"

# Read the contents of readme file
source_root = Path(".")
with (source_root / "readme.md").open(encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements
# with (source_root / "requirements.txt").open(encoding="utf8") as f:
#     requirements = f.readlines()
requirements = []

setup(
    name="task-graph",
    version=version,
    author='loopyme',
    author_email='peter@mail.loopy.tech',
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/loopyme/Task-Graph",
    license="MIT",
    description="Make computer lazy and build a dynamic task graph for your project!",
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="task-graph task-manager lazy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={},
    options={},
)
