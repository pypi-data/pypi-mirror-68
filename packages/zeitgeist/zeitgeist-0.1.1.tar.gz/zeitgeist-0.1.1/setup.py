from setuptools import setup, find_packages

package_name = "zeitgeist"

author = "Mukund Varma, Noah Spies"

setup(
    author=author,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
    name=package_name,
    description="Gene Expression Program discovery in scRNAseq data",
    url="http://github.com/celsiustx/zeitgeist/",
    include_package_data=True,
    packages=[],
    version="0.1.1",
)
