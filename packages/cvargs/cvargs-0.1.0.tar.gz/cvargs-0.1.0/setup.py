from setuptools import find_packages, setup

with open("README.rst") as f:
    description = f.read()


setup_kwargs = {
    "name": "cvargs",
    "version": "0.1.0",
    "description": "Function argument conversion",
    "long_description": description,
    "long_description_content_type": "text/x-rst",
    "author": "Oliver Berger",
    "author_email": "diefans@gmail.com",
    "url": "https://gitlab.com/diefans/cvargs",
    "package_dir": {"": "src"},
    "packages": find_packages("src"),
    "include_package_data": True,
    # "package_data": {"": ["*"]},
    "install_requires": [],
    "extras_require": {
        "tests": [
            "pytest>=4.6",
            "pytest-cov>=^2.7,<3.0",
            "pytest-watch>=4.2<5.0",
            "pytest-randomly>=3.1<4.0",
            "pdbpp",
        ]
    },
    "entry_points": {},
    "python_requires": ">=3.7,<4.0",
    "classifiers": [
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: MIT License",
    ],
}
setup(**setup_kwargs)
