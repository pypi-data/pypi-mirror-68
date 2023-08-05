import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "whatsapp-converter",
    version="0.3.4",
    author="Martin Sand",
    author_email="marti.sand.dev@gmail.com",
    description="Use whatsapp-converter to convert your exported WhatsApp chat to a CSV or ODS file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandsturm/whatsapp-converter",
    license='LICENSE.txt',
    packages=setuptools.find_packages(),
    # packages=["reader"],
    install_requires=[
        'tqdm>=4.46.0',
        'xlwt>=1.3.0'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
    ],
    python_requires='>=3.7',
    project_urls={  # Optional
        'Source': 'https://github.com/sandsturm/whatsapp-converter/',
    },
    entry_points={
        "console_scripts": [
            "whatsapp-converter=whatsapp_converter.__main__:main",
        ]
    },
)
