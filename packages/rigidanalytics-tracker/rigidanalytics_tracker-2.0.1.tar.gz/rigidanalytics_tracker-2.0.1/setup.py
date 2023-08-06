import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rigidanalytics_tracker",
    version="2.0.1",
    author="Shane Reustle",
    author_email="shane@reustle.co",
    description="Server-side analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reustleco/rigidanalytics-tracker/",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "blinker",
        "urllib3",
    ]
)
