import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matrix_transpose", # Replace with your own username
    version="1.5",
    author="Noushad Khan",
    author_email="noushadkhan1994@gmail.com",
    description="matrix transpose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noushadkhan01/matrix_transpose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
