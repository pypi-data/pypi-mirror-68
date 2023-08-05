import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudpyio",
    version="0.0.19",
    author="cloudpy.io",
    author_email="author@example.com",
    description="cloudpy.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ortutay/cloudpy",
    packages=setuptools.find_packages(
        include=['npc_internal', 'cloudpy'],
        exclude=['npc_internal.server']
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    # TODO: review these dependencies, see which can be removed
    install_requires=[
        'numpy<=1.15.4',  # cap at 1.15.4 until workaround/fix for https://github.com/numpy/numpy/issues/14012
        'pandas>=1.0.0',
        'cloudpickle>=0.6.1',
        'humanize>=2.2.0',
        'requests>=2.20.0',
        'requests-toolbelt>=0.8.0',
        'psutil>=5.4.8',
    ],
)
