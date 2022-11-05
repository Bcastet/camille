from setuptools import setup

setup(
    name="kayle",
    version="0.3.0",
    description="Riot Games API Match wrapper for async requests",
    url="https://github.com/Bcastet/camille",
    author='Benjamin Castet',
    author_email='benjamin.castet@gmail.com',
    license='BSD 2-clause',
    packages=['kayle'],
    install_requires=["munch==2.5.0",
                      "pantheon==2.0.0",
                      "Pillow==9.3.0",
                      "pytest==7.2.0",
                      "requests==2.28.1",
                      "setuptools==65.5.0"],
)
