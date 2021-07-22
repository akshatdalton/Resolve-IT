from setuptools import find_packages, setup

VERSION = "1.0.0"

with open("requirements/common.in") as f:
    REQUIREMENTS = list(
        filter(
            lambda req: not req.startswith("#") and not req.startswith("http") and req,
            f.read().splitlines(),
        )
    )

with open("README.md", encoding="utf8") as f:
    README = f.read()


setup(
    name="Resolve-IT",
    version=VERSION,
    author="Akshat",
    description="A CLI tool that fetches Stack Overflow results when an exception is thrown.",
    long_description=README,
    long_description_content_type="text/markdown",
    author_email="akshat.dak@students.iiit.ac.in",
    python_requires=">=3.5",
    url="https://github.com/akshatdalton/Resolve-IT",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={"console_scripts": ["resolveit = resolveit.app:main"]},
    install_requires=REQUIREMENTS,
    license="MIT License",
)
