from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

CLASSIFIERS = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Development Status :: 4 - Beta"
]

setup(
    name='aanalytics2',
    version="0.0.1",
    license='GPL',
    description='Adobe Analytics v2 API wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Julien Piccini',
    author_email='piccini.julien@gmail.com',
    url='https://github.com/pitchmuc/adobe_analytics_api_2.0',
    keywords=['adobe', 'analytics', 'API', 'python'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas>=0.25.3',
        'pathlib2>=2.3.5',
        'requests>=2.22.0',
        'PyJWT[crypto]>=1.7.1',
        'PyJWT>=1.7.1'
    ],
    classifiers=CLASSIFIERS,
    python_requires='>=3.6'
)
