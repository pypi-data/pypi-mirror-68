import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chat-pkg-esteban9706", # Replace with your own username
    version="0.0.1",
    author="Francisco Segovia",
    author_email="corlo.esteban@gmail.com",
    description="A small chat package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Segovfrank/chatify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)