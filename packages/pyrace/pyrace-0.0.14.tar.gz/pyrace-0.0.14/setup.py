import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrace",
    version="0.0.14",
    author="Cedric Jouan",
    author_email="cedric.jouan@ibm.com",
    description="This package provides an environment to practice different types of reingorcement learning models.",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CedricJouan/pyrace",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib', 'pprint', 'pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)