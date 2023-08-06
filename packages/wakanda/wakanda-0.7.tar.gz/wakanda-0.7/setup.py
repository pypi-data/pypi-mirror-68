import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'wakanda',         # How you named your package folder (MyLib)
  packages = ['wakanda'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library enable to extract data from various african website into a pandas DataFrame ',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Bakayoko vaflaly',                   # Type in your name
  author_email = 'bvbouba@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/bvbouba/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/bvbouba/wakanda/archive/0.7.tar.gz',    # I explain this later on
  keywords = ['africa','stock','index','price','exchange'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'fake_useragent',
          'bs4',
          'pandas',
          'numpy',
      ],
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
)
