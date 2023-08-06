import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ems-compliance-checks-pkg-MarkoDS",
    version="0.0.2",
    author="Marko Kauzlarić",
    author_email="marko@discoveryspecialists.com",
    description="Package that hold logic for compliance checks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acdcorp/clarity_ems_compliance_checks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
