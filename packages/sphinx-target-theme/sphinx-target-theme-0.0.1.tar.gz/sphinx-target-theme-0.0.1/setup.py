import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx-target-theme", # Replace with your own username
    version="0.0.1",
    author=u"Klaus Kähler Holst",
    author_email="klaus@holst.it",
    description="Sphinx theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/kkholst/sphinx_target_theme",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
