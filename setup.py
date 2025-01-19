from setuptools import find_packages, setup

setup(
    name="big-data-engineer",
    version="0.1.0",
    description="Big Data Engineer reference repository for Synapse, Spark, ADLS, Fabric, and Kusto workloads.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pyspark>=3.5.0",
        "azure-storage-file-datalake>=12.15.0",
        "azure-cosmos>=4.8.0",
        "pandas>=2.2.0",
    ],
)
