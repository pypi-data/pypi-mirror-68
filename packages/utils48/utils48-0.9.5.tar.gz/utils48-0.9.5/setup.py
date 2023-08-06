from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
  name = 'utils48',         # How you named your package folder (MyLib)
  packages = ['utils48'],   # Chose the same as "name"
  version = '0.9.5',      # Start with a small number and increase it with every change you make
  description = 'some utilities',   # Give a short description about your library
  author = '48panda',                   # Type in your name
  url = 'https://github.com/48panda48/48util',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/48panda48/48util/archive/0.9.tar.gz',    # I explain this later on
  )
print(long_description)
