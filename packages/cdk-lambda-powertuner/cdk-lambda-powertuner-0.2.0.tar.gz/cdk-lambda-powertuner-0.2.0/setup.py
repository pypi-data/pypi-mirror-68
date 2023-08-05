import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-lambda-powertuner",
    "version": "0.2.0",
    "description": "cdk-lambda-powertuner",
    "license": "Apache-2.0",
    "url": "https://github.com/nideveloper/cdk-lambda-powertuner.git",
    "long_description_content_type": "text/markdown",
    "author": "hello@cdkpatterns.com",
    "project_urls": {
        "Source": "https://github.com/nideveloper/cdk-lambda-powertuner.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "lambda_powertuner",
        "lambda_powertuner._jsii"
    ],
    "package_data": {
        "lambda_powertuner._jsii": [
            "cdk-lambda-powertuner@0.2.0.jsii.tgz"
        ],
        "lambda_powertuner": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-iam>=1.37.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.37.0, <2.0.0",
        "aws-cdk.aws-stepfunctions>=1.37.0, <2.0.0",
        "aws-cdk.aws-stepfunctions-tasks>=1.37.0, <2.0.0",
        "aws-cdk.core>=1.37.0, <2.0.0",
        "constructs>=0.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
