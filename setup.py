import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="scan",
    version="0.0.2",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),

    install_requires=[
        "moto==1.3.14",
        "pytest==5.4.1",
        "requests==2.24.0",
        "boto3==1.12.37",
        "requests==2.24.0",
        "psycopg2-binary==2.8.5"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
