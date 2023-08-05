import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CoralPay",# Replace with your own username
    version="0.0.1",
    author="Adegoke Ayanfe",
    author_email="adegokeayanfe@gmail.com",
    description="CoralPay python libary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beloved23/coralpay",
    packages=setuptools.find_packages(),
    classifiers=[
           'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
    install_requires=[          
          'pretty_bad_protocol'
      ]
)



