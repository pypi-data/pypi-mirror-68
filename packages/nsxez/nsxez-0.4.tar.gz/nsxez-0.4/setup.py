import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='nsxez',  
     version='0.4',
     author="Francois Prowse",
     author_email="nsxez@prowsehouse.com",
     description="A API abstraction package for NSX-T 3.0 and greater",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/farsonic/nsxez",
     packages=setuptools.find_packages(),
     install_requires=[            # I get to this in a second
          'requests',
          'json',
          'uuid',
      ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
