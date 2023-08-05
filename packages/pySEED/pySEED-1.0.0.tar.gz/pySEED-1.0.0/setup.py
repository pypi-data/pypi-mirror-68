import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySEED",
    version="1.0.0",
    author="Valentin Calzada Ledesma, Juan de Anda Suarez",
    author_email="m.c.juandeanda@gmail.com",
    description="pySEED is a python inplementation of the SEED optimization algorithm that was published in IEEE Accsses, with DOI: 10.1109/ACCESS.2019.2948199",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/juandeanda/pySEED.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2',
    install_requires=[
   'numpy>=1.18.2',
   'joblib>=0.14.1'
   ]
)
