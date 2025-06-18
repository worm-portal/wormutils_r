import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wormutils_r",
    version="0.1.0",
    author="Grayson Boyer",
    author_email="gmboyer@asu.edu",
    description="A package for common functions containing R/rpy2 used in other WORM codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={},
    packages=['wormutils_r'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=['rpy2', 'dill', 'pandas', 'numpy'],
    include_package_data=True,
    package_data={},
    zip_safe=False
)

