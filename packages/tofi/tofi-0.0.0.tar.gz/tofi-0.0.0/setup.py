import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="tofi",
    version="0.0.0",
    author="Llandy Riveron Del Risco",
    author_email="llandy3d@gmail.com",
    description="I like tofi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llandy3d/tofi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
