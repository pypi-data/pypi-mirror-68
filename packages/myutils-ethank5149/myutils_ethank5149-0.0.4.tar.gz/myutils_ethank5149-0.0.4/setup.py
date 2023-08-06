from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="myutils_ethank5149",
    version="0.0.4",
    author="Ethan Knox",
    author_email="ethank5149@gmail.com.com",
    description="Frequently used function and math utilities",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ethank5149/myutils_ethank5149",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.6',
    tests_require=[],
)
