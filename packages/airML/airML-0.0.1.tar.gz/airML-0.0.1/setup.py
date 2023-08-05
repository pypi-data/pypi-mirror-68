from setuptools import setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="airML", # Replace with your own username
    version="0.0.1",
    author="Edgard Marx",
    description="application will allow users to " +
                "share and dereference ML models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    py_modules= ['airML'],
    packages = [""],
    package_dir = {'':'src'},
    include_package_data=True,
)