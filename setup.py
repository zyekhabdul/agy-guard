from setuptools import setup

setup(
    name="agy-guard",
    version="3.0.0",
    description="Deterministic AI Agent Governance, AST Blast-Radius Scanner & Verification Harness",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Zyekh Abdul",
    author_email="zyekhabdulqadirjailani@gmail.com",
    url="https://github.com/zyekhabdul/agy-guard",
    license="MIT",
    scripts=["bin/agy-guard"],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
)
