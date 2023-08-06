from setuptools import setup

setup(name='molywood',
      version='0.144',
      description='A script to automate the production of molecular movies in VMD',
      url='https://gitlab.com/KomBioMol/molywood',
      author='Milosz Wieczor',
      author_email='milafternoon@gmail.com',
      license='GNU GPLv3',
      packages=['molywood'],
      entry_points={'console_scripts': ['molywood = molywood.moly:molywood',
                                        'molywood-gen-env = molywood.moly:gen_yml']},
      python_requires='>=3.4',
      #install_requires=['numpy', 'matplotlib', 'seaborn'],
      zip_safe=False)
