import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utils4ymc",
    version="0.1.2",
    author="Yummy Chen",
    author_email="chenymcan@gmail.com",
    description="Making our programing more efficient.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/interesting6/utils4ymc",
    packages=setuptools.find_packages(),
    install_requires=['numpy>=1.15', ],
    entry_points={
        # 'console_scripts': [
        #     'utils=utils:main'
        # ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.6',
)