from setuptools import setup, find_packages

setup(
    name='find_home',
    packages=find_packages(),
    version='0.0.4',
    author='Vladimir Starostin',
    author_email='vladimir.starostin@uni-tuebingen.de',
    description='I just wanna find home...',
    license='MIT',
    python_requires='>=3.7.*',
    install_requires=[
        'cryptography',
        'beautifulsoup4',
    ],
    include_package_data=True,
    keywords='parser',
    url='https://pypi.org/project/find_home/',
)
