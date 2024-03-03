from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    name='askdoc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'askdoc=src.chat:main',
        ],
    },
    # Metadata
    author='Romit',
    author_email='romit.73@gmail.com',
    description='Ask a personal doctor for your medical queries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/romitjain/askdoc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
