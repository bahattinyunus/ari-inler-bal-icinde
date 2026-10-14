from setuptools import setup, find_packages

setup(
    name="ari-inler-bal-icinde",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "ari_inler_bal_icinde": ["data/*.json"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ari-inler-bal-icinde=ari_inler_bal_icinde.cli:main",
        ],
    },
    python_requires=">=3.9",
)
