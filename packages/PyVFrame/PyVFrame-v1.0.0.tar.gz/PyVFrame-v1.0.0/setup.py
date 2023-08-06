from distutils.core import setup

setup(
  name = 'PyVFrame',
  packages = ['PyVFrame'],
  version = 'v1.0.0',
  license = 'MIT',
  description = 'Framework built in python for easy vanilla web development',
  author = 'Drew Adams',
  author_email = 'drew@drewtadams.com',
  url = 'https://github.com/drewtadams',
  download_url = 'https://github.com/drewtadams/PyVFrame/archive/v1.0.0.tar.gz',
  keywords = ['framework', 'html', 'scss', 'css', 'js'],
  install_requires = [
    'importlib',
    'jsmin',
    'json',
    'shutil',
  ],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)