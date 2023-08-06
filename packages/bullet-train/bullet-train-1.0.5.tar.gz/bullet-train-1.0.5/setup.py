from setuptools import setup

with open("Readme.md", "r") as readme:
    long_description = readme.read()

setup(
    name="bullet-train",
    version="1.0.5",
    packages=["bullet_train"],
    description="Bullet Train Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Solid State Group",
    author_email="bullettrain@solidstategroup.com",
    license="BSD3",
    url="https://github.com/solidstategroup/bullet-train-python-client",
    keywords=["feature", "flag", "bullet", "train", "remote", "config"],
    install_requires=[
        'requests>=2.19.1',
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)