from setuptools import setup

requires = ["requests>=2.14.2"]

setup(
    name='my_new_package',
    version='0.1',
    description='Awesome library',
    url='https://github.com/whatever/whatever',
    author='yourname',
    author_email='your@address.com',
    license='MIT',
    keywords='sample setuptools development',
    packages=[
        "my_new_package",
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
