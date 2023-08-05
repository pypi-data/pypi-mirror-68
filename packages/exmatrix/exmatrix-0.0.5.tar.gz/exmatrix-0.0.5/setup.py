from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='exmatrix',
    version='0.0.5',
    description='A Python package to ExMatrix method, supporting Random Forest models interpretability.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/blindreview/??',
    author='Blind Review',
    author_email='blindreview@gmail.com',
    license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International',
    classifiers=[
        'License :: Free for non-commercial use',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    packages=['src'],
    include_package_data=True,
    install_requires=['numpy'],    
)