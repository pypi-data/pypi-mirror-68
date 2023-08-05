import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="python-hydra",
    version="1.3.1",
    description="Python API for interfacing with Hydra Execution Environment",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lukecavabarrett/python-hydra",
    author="Luca Cavalleri",
    author_email="luca.cavallery@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["hydra"],
    include_package_data=True,
    install_requires=[],
    entry_points={
    },
)

# rm dist/*
# python3 setup.py sdist bdist_wheel
# twine upload dist/*