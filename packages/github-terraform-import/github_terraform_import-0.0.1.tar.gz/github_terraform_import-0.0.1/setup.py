import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="github_terraform_import",
    version="0.0.1",
    packages=[
        'github_terraform_import',
        'github_terraform_import/github_types',
        'github_terraform_import/provider',
    ],
    install_requires=["requests>=2.0"],
    description="Import or sync existing Github infrastructure into terraform",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BraeWebb/github-terraform-import",
    author="Brae Webb",
    author_email="email@braewebb.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)