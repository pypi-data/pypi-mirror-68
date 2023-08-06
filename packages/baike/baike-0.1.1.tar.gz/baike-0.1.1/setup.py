import setuptools

with open("README.md","r",encoding="utf-8") as fh:
    long_description=fh.read()

setuptools.setup(
        name="baike",
        version="0.1.1",
        author="Lightyears",
        author_email="1MLightyears@gmail.com",
        description="BaiduBaike search bot",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/1MLightyears/baike',
        packages=setuptools.find_packages(),
)

