import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='chibp',  
    version='1.2.0',
    author="Christopher Dunne",
    author_email="contact@chrisdunne.net",
    description="A package for utilising the Haveibeenpwned API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisdunne/hibp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires  = ["requests"],
 )