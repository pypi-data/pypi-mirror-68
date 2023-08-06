from distutils.core import setup
setup(
  name = 'smallbrowser',
  packages = ['smallbrowser'],
  version = '0.1',
  license='gpl-3.0',
  description = "A small HTTP browser library in Python based on the 'requests' library",
  author = 'Ivan Dustin B. Bilon',
  author_email = 'ivan22.dust@gmail.com',
  url = 'https://github.com/ivandustin/smallbrowser',
  keywords = ['http', 'browser', 'client', 'requests', 'web', 'scraping', 'small', 'simple', 'easy', 'beginners'],
  install_requires=[
          'requests',
          'pyquery',
      ]
)
