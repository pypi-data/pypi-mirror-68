from setuptools import setup, find_packages
from pymumble_py3.constants import PYMUMBLE_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pymumble",
    version=PYMUMBLE_VERSION,
    author='Azlux',
    author_email='github@azlux.fr',
    description="Mumble library used for multiple uses like making mumble bot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/azlux/pymumble',
    license='GPLv3',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Operating System :: OS Independent",
                 ],
    python_requires='>=3.6',
)
