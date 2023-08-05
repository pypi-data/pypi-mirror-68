from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="paymentcheckout",
    version="1.0.5",
    description="Payment verification for QIWI, Yandex Money, Payeer and QIWI Virtual Bank Card.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Blazzerrr",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["paymentcheckout"],
    include_package_data=True,
    install_requires=["requests"]
)

 
