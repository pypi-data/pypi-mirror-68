import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="GEMLibrary-linux",
    version="0.2.2",
    include_package_data=True,
    author="Kevin Morgan",
    description="Derivatives Library for Teleios",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
)
