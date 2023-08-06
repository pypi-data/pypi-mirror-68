import setuptools

from version import get_git_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ni-core-server", # Replace with your own username
    version=get_git_version(),
    author="Primael Bruant",
    author_email="primael.bruant@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pika==1.1.0",
        "tornado==6.0.4",
        "click==7.1.2",
        "ni-logging-utils==0.0.3",
        "coloredlogs==14.0",
        "pillow==7.1.2"
    ],
    entry_points='''
       [console_scripts]
       core_server=core.cm:cm
    ''',
    python_requires='>=3.6'
)
