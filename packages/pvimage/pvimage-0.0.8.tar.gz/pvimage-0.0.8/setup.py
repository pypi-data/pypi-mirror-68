from setuptools import setup

with open("PVimageDescription.txt", "r") as fh:
    long_description = fh.read()

setup(name='pvimage',
      version='0.0.8',
      description='package for pv image analysis and machine learning modeling',
      long_description=long_description,
      url='http://engineering.case.edu/centers/sdle/',
      author='Ahmad Maroof Karimi, Benjamin G. Pierce, Justin S. Fada, Nicholas A. Parrilla, Roger H. French, Jennifer L. Braid',
      author_email='axk962@case.edu, jlbraid@sandia.gov',
      license='Apache License v2',
      packages=['pvimage'],
      package_dir={'pvimage': './pvimage'},
      package_data={'pvimage': ['files/data/Minimodules/*','files/data/FullSizeModules/*','files/tutorials/*','files/data/out','README.rst']},
      python_requires='>=3.6.5',
      install_requires=['markdown', 'pyhull','opencv-python','scipy','scikit-image','glob2'],
      include_package_data=True,
      project_urls={"Documentation":"https://pvimage-doc.readthedocs.io/en/latest/index.html","Bugtracker": "https://bitbucket.org/cwrusdle/pvimage-doc/issues?status=new&status=open"},
      zip_safe=False)
