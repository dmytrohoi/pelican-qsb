import setuptools

import qsb

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pelican-qsb",
    version=qsb.__version__,
    packages=setuptools.find_packages(),
    url="https://github.com/dmytrohoi/pelican-qsb",
    license="MIT License",
    author=qsb.__author__,
    author_email=qsb.__email__,
    description="Simple helper for automation Pelican-based site building",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=["pelican", "ghp-import"],
    entry_points={"console_scripts": ["pelican-qsb = qsb.make_site:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pelican",
        "Framework :: Pelican :: Plugins",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools"
    ],
)
