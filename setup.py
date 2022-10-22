import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dlresultserm",
    version="0.0.1",
    author="Open Politica",
    author_email="openpoliticaperu@gmail.com",
    description="Script to obtain results from ERM 2022",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openpolitica/results-elections-2022",
    project_urls={
        "Bug Tracker": "https://github.com/openpolitica/results-elections-2022/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License ",
        "Operating System :: POSIX :: Linux ",
    ],
    packages=setuptools.find_packages(
        include=[
            'dlresultserm',
            'dlresultserm.*']),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'colorlog',
        'requests',
        'python-dotenv'],
    entry_points={
        'console_scripts': [
            'dlresultserm=dlresultserm.cli:main',
        ],
    },
)
