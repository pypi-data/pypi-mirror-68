import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agv-fact",
    version="0.0.2.24",
    author="Andres Alvarado Vazquez",
    author_email="andres@agavesoft.com.mx",
    description="Libreria para generar xml y realizar el timbrado",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/fact",
    packages=setuptools.find_packages(),
    package_data={'fact.generator': '*'},
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)