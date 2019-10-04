import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mkdocs-versioning",
    version="0.1.0",
    author="Zayd Patel",
    author_email="zayd62@gmail.com",
    description="A tool that allows for versioning sites built with mkdocs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zayd62/mkdocs-versioning",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Topic :: Documentation",
        'Topic :: Text Processing',
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={
        "console_scripts": [
            'mkdocs-versioning = mkversion.__main__:main'
        ],
        'mkdocs.plugins': [
            'mkdocs-versioning = mkversion.entry:Entry',
        ]
    },
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    project_urls={
        'Documentation': 'https://zayd62.github.io/mkdocs-versioning/'
    },
    install_requires = [
        'PyYAML >= 5.1.2',
        'mkdocs >= 1.0.4'
    ]
)
