from distutils.core import setup
setup(
    name='pygdal',
    version='0.0.1dev',
    description='Pythonic and full control GDAL.',
    long_description=open("README.md").read(),
    author='Fabian Schindler',
    author_email='fabian.schindler@eox.at',
    url='https://github.com/constantinius/pygdal',
    packages=['pygdal'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: GIS"
    ]

)