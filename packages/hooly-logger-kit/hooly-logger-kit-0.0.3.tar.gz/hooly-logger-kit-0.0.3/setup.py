import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hooly-logger-kit",
    version="0.0.3",
    author="David Erazo",
    author_email="david.erazo@afpcapital.cl",
    description="A small library for logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AFP-Capital/hooly-logger-kit-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
