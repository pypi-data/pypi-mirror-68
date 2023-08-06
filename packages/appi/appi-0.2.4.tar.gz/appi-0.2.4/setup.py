import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appi",
    version="0.2.4",
    author="Daniel Robbins, Antoine Pinsard",
    author_email="drobbins@funtoo.org",
    description="This is a python module created by Antoine Pinsard that powers ego query commands.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://code.funtoo.org/bitbucket/projects/CORE/repos/appi/browse",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',
    packages=setuptools.find_packages()
)
