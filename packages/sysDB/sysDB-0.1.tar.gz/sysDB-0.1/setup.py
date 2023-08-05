import setuptools

with open("README.md", "r") as readmeHandle:
    long_description = readmeHandle.read()

setuptools.setup(
    name='sysDB',
    version='0.1',
    scripts=['sysDB/__init__.py'],
    author="nnewram",
    author_email="marwenn02@gmail.com",
    description="A x86 and x64 syscall database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marwenn02/syscallDB",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
