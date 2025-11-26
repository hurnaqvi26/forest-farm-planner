from setuptools import setup, find_packages

setup(
    name="cropcalc-hurnaqvi",  
    version="0.1.0",
    author="Hur Naqvi",
    author_email="hurnaqvi26@gmail.com",
    description="Crop yield calculator library for farm planner app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
)
