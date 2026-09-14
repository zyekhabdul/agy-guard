from setuptools import setup, find_packages

setup(
    name="agy-guard",
    version="3.0.1",
    description="Deterministic AI Agent Governance, AST Blast-Radius Scanner & Verification Harness",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Zyekh Abdul",
    author_email="zyekhabdulqadirjailani@gmail.com",
    url="https://github.com/zyekhabdul/agy-guard",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "agy-guard=agy_guard.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
)
