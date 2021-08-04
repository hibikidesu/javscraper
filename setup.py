from setuptools import setup

# Requirements
with open("requirements.txt", "r") as f:
    requirements = f.read().split("\n")


setup(
    name="javscraper",
    version="1.0.0",
    description="Python library used to help scrape JAV sites.",
    url="https://github.com/hibikidesu/javscraper",
    author="Hibiki",
    license_files=("COPYING",),
    packages=["javscraper"],
    python_requires=">=3.4",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
