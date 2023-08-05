from setuptools import setup, find_namespace_packages

setup(
    name="nmcipher.cli",
    version="0.0.5",
    author="Neil Marshall",
    author_email="neil.marshall@dunelm.org.uk",
    description="A command line parser package for use with basic encryption algorithms",
    packages=find_namespace_packages(include=["nmcipher.*"], exclude=["nmcipher.tests"]),
    install_requires=["nmcipher.affine", "nmcipher.caesar", "nmcipher.transposition"],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "affine = nmcipher.cli:affine",
            "caesar = nmcipher.cli:caesar",
            "transposition=nmcipher.cli:transposition"
        ]
    }
)
