import glob
import setuptools
import sys
import unittest

# if version of setuptools is 20.8.1 or below, it doesn't support env specs
if int(setuptools.__version__.split(".")[0]) < 21:
    if sys.version_info[:3] < (3, 5, 0):
        typing_dep = ["typing"]
    else:
        typing_dep = []
else:
    typing_dep = ["typing ; python_version<'3.5.0'"]


def gtirb_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


if __name__ == "__main__":
    setuptools.setup(
        name="gtirb",
        version=(
            "1"
            ".6"
            ".0"
        ),
        author="abhaskar",
        author_email="abhaskar@grammatech.com",
        description="The gtirb package",
        packages=setuptools.find_packages(),
        test_suite="setup.gtirb_test_suite",
        install_requires=["protobuf"] + typing_dep,
        classifiers=["Programming Language :: Python :: 3"],
    )
