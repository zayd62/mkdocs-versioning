import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mkdocs-versioning",
    version="0.1.0",
    author="Zayd Patel",
    author_email="zayd62@gmail.com",
    description="A versioning tool for mkdocs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zayd62/mkdocs-versioning",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Topic :: Documentation",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    entry_points={
        "console_scripts": [
            'mkdocs-versioning = mkversion.__main__:main'
        ],
        'mkdocs.plugins': [
            'mkdocs-versioning = mkversion.entry:Entry',
        ]
    }
)
