import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="atmigram",
    version="0.0.1",
    author="fishsouprecipe",
    author_email="fishsouprecipe@gmail.com",
    description="async/await lib ... (atmigram)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fishsouprecipe/atmigram",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.5',
)