import setuptools
with open("README.txt", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='walklog',  
     version='0.1',
     scripts=['walklog'] ,
     author="Priyansh Tiwari",
     author_email="Priyansh.tiwari99@gmail.com",
     description="My own customized Loguru",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )