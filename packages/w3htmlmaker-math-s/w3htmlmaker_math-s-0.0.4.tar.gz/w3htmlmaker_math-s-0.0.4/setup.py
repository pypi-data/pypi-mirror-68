import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="w3htmlmaker_math-s",
    version="0.0.4",
    author="Matheus Silva",
    author_email="matheus.andrade1996@gmail.com",
    description="A HTML creator for articles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/math-s/w3htmlmaker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
