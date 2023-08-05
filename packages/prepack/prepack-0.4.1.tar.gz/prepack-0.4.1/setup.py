from setuptools import setup

setup(name='prepack',
      version='0.4.1',
      description='Python excel based data preparation library',
      long_description="Library for preparing data for analysis. "
                       "Allows you to load and easily filter many same structure csv or xls, xlsx files. "
                       "Allows matching tables by incomplete row matching over the shortest Levenshtein "
                       "distance, just like Pandas df.merge()",
      url='http://github.com/legale/prepack',
      author='rumi',
      author_email='legale.legale@gmail.com',
      license='MIT',
      packages=['prepack'],
      zip_safe=False,
      install_requires=['numpy','pandas','python-levenshtein','xlrd'],
      keywords = ['xls', 'excel', 'parser', 'pandas','data preparation'],
      classifiers=[
            'Operating System :: OS Independent',
            'Development Status :: 3 - Alpha',
            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',  # Define that your audience are developers
            'Intended Audience :: End Users/Desktop',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',  # Again, pick a license
            'Programming Language :: Python :: 3',

      ],
      )