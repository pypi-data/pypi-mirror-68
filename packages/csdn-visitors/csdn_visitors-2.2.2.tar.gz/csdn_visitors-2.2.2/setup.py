import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="csdn_visitors",
    version="2.2.2",
    author="Lux",
    author_email="1223411083@qq.com",
    description="Swipe CSDN visitors in batches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Amiee-well/CSDN",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= [
        'requests','lxml'
    ],
)
