import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="newpyproj",
    version="0.0.4",
    author="Rafael Leite Paulo",
    author_email="rafael@leite.org",
    description="Automatically creates a new python project folder",
    keywords = ['TEMPLATE', 'AUTOMATION', 'PROJECT', 'STRUCTURE', 'PACKAGE'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafxel/newpyproj/",
    packages=setuptools.find_packages(exclude=("tests", "docs")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["pytest"]
)

