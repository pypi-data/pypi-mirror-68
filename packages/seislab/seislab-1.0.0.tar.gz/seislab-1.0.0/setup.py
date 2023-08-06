import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='seislab',
    version='1.0.0',
    packages=setuptools.find_packages(),
    description='A python toolbox for seismic data i/o and analysis',
    author='Cognitive Geo',
    author_email='cognitivegeo.info@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=['Python', 'Seismic'],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)