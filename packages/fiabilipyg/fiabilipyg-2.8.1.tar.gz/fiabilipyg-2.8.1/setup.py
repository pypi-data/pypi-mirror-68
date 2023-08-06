import setuptools

setuptools.setup(
    name="fiabilipyg", # Replace with your own username
    version="2.8.1",
    author="chabotsi, crubier, cdrom1",
    author_email="contact@fiabilipy.org",
    description="fiabilipy with .draw",
    long_description="Slight enhancement of fiabilipy for draw(): supports latest versions of networkx. Description of fiabilipy: This package provides some functions to learn engineering reliability at university. One can build components, put them together to build a system and evaluate its reliability, maintainability, availability, the Mean-Time-To-Failure, etc. This package also provides functions to describe a system by a Markov process."
,
    url="http://fiabilipy.org",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
