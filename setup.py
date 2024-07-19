import setuptools

setuptools.setup(
    name='luxtools',
    version='0.1.0',
    description='Tools to make my life a bit easier',
    packages=setuptools.find_packages(),
    install_requires=[
        "torch",
        'typeguard'
    ],
)
