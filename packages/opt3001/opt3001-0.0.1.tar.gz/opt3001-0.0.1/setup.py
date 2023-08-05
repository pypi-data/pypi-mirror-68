import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opt3001",
    version="0.0.1",
    author="Thomas Pöhlmann",
    author_email="thomaspoehlmann96@googlemail.com",
    description="A demo_car package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perryrh0dan/opt3001",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 