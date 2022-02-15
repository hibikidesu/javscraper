from setuptools import setup

# Requirements
requirements = [
    "requests>=2.26.0",
    "lxml>=4.6.3",
    "cloudscraper>=1.2.58"
]


setup(
    name="javscraper",
    version="1.1.4",
    description="Python library used to help scrape JAV sites.",
    url="https://github.com/hibikidesu/javscraper",
    author="Hibiki",
    license_files=("COPYING",),
    packages=["javscraper"],
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
