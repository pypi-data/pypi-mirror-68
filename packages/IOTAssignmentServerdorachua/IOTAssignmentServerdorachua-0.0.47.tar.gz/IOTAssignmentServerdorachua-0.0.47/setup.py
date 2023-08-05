import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IOTAssignmentServerdorachua", # Replace dorachua with your own username (no space)
    version="0.0.47",
    author="Dora Chua",
    author_email="msdorachua@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=['numpy','mysql-connector-python','IOTAssignmentUtilitiesdorachua'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
    python_requires='>=3.6',
)
