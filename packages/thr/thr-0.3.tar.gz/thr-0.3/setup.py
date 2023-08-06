from setuptools import setup, find_packages
setup(
    name="thr",
    version="0.3",
    description="Minimal Threema Gateway library",
    url="http://github.com/coffeemakr/python-thr",
    author="coffeemakr",
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    license='Unlicense',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
