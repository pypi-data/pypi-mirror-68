import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk8s-debore",
    "version": "0.1.1",
    "description": "Run your apps on Kubernetes cluster without bored YAMLing",
    "license": "Apache-2.0",
    "url": "https://github.com/toricls/cdk8s-debore.git",
    "long_description_content_type": "text/markdown",
    "author": "Tori<yshr@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/toricls/cdk8s-debore.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_debore",
        "cdk8s_debore._jsii"
    ],
    "package_data": {
        "cdk8s_debore._jsii": [
            "cdk8s-debore@0.1.1.jsii.tgz"
        ],
        "cdk8s_debore": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3",
        "cdk8s>=0.20.0, <0.21.0",
        "constructs>=2.0.1, <3.0.0"
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
