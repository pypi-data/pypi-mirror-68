import setuptools

with open("README.md", "r") as _:
    long_description = _.read()

setuptools.setup(
    name="img-renamer",
    version="2.5.1",
    author="Miika Launiainen",
    author_email="miika.launiainen@gmail.com",
    description="Script to rename images in numberic order",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/miicat/img-renamer",
    scripts=["img_renamer/img_renamer"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.0",
    install_requires=[
        "click",
    ]
)
