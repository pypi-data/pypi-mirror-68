import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alink",
    version="0.0.6",
    author="andyxialm",
    author_email="andyxialm@gmail.com",
    description="Bring users directly to specific content in your Android app.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://refactor.cn/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click>=7.1.2',
    ],
    zip_safe=False,
    platforms='any',
    # py_modules=['alink'],
    entry_points={
        'console_scripts': ['alink = hugo.hugo:cli']
    },
    python_requires='>=3.3',
)
