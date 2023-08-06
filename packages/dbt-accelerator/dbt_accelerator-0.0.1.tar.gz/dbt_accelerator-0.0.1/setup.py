import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbt_accelerator", 
    version="0.0.1",
    author="Ramgopalan V",
    author_email="ram.gopalan@live.com",
    description="Package which generates schema.yml and columns.md from Excel Sheet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramgopalan/dbt_accelerator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas','xlrd','mdutils'],
    required_by= "create.py",
    python_requires='>=3.6',
)