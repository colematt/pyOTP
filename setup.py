import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyotp-pkg-mcole8",
    version="1.1",
    author="Matthew Cole",
    author_email="mcole8@binghamton.edu",
    description="Python3 implementation of IETF One-Time Password algorithms with QRCode recognition for provisioning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/colematt/pyOTP/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)