import setuptools
with open("README.txt", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='MyPipModule',  
     version='0.1',
     scripts=['MyPipModule'] ,
     author="Priyansh Tiwari",
     author_email="Priyansh.tiwari99@gmail.com",
     description="My own Pip module",
     long_description=long_description,
     long_description_content_type="text/markdown",
     #url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )