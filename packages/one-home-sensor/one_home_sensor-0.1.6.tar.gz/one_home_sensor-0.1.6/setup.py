import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="one_home_sensor",
    version='0.1.6',
    author="LeadTheSalt",
    author_email="leadthesalt.soc@gmail.com",
    description="My home tempearture sensor for my RaspberryPi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leadthesalt/one_home_sensor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'smbus2',
        'i2cdevice',
        'pymongo[srv,tls]'
    ],
    python_requires='>=3.5',
)