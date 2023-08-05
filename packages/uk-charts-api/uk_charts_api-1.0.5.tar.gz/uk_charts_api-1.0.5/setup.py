import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uk_charts_api",
    version="1.0.5",
    author="Connor McLaughlin",
    description="Python package to get deezer info for UK Top 40 charts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmclaughlin/UK-Charts-API",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.6",
    install_requires=[
        "beautifulsoup4==4.9.0",
        "certifi==2020.4.5.1",
        "cffi==1.14.0",
        "chardet==3.0.4",
        "cryptography==2.9.2",
        "idna==2.9",
        "pycparser==2.20",
        "requests==2.23.0",
        "six==1.14.0",
        "soupsieve==2.0",
        "urllib3 == 1.25.9",
    ],
)
