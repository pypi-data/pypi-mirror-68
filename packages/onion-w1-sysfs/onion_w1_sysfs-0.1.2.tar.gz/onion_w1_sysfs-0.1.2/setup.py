import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onion_w1_sysfs",
    version="0.1.2",
    author="Grizmin",
    author_email="grizmin@gmail.com",
    description="w1 lib using the sysfs interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grizmin/w1-gpio-linux",
    package_dir={'': 'OneWire'},
    py_modules=["OneWire"],
    packages=setuptools.find_packages(where='OneWire'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='onion omega IoT w1 onewire 1w',
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
)
