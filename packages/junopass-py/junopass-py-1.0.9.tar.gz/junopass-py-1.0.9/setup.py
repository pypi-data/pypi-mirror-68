import setuptools
long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="junopass-py",
    version="1.0.9",
    author="Felix Cheruiyot",
    author_email="felix@junopass.com",
    description="JunoPass support for Python.JunoPass provides a secure 2FA and Passwordless authentication.",
    long_description=long_description,
    url="https://github.com/junopass/junopass-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=[
        'PyNaCl==1.3.0',
        'requests==2.23.0'
    ]
)
