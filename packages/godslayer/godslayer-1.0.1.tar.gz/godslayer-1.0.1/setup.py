#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Yukihiko Shinoda",
    author_email="yuk.hik.future@gmail.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Indexing",
        "Typing :: Typed",
    ],
    description="Provides generator to read Kami (god) CSV record as list of string.",
    install_requires=[],
    dependency_links=[],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="God CSV Excel Microsoft 神CSV ネ申CSV 神エクセル ネ申エクセル マイクロソフト",
    name="godslayer",
    packages=find_packages(include=["godslayer", "godslayer.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/yukihiko-shinoda/god-slayer",
    version="1.0.1",
    zip_safe=False,
)
