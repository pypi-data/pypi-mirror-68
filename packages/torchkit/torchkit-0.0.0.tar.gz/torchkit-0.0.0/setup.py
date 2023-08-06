from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open('requirements.txt', 'r') as infile:
    requirements = [line.strip() for line in infile.readlines()]

setup(name='torchkit',
      version='0.0.0',
      description='',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Jeremy Wohlwend',
      author_email='jeremy@asapp.com',
      packages=find_packages(exclude=('test*',)),
      install_requires=requirements,
      include_package_data=True)
