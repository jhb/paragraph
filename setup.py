from setuptools import setup

setup(name='paragraph',
      version='0.0.1',
      description='UI to graph databases',
      url='',
      author='GraphUI devs',
      author_email='devs@graphui.org',
      license='GPLV3',
      packages=['paragraph'],
      install_requires=[
        'Flask',
        'neo4j',
        'pytest',
        'flask_wtf',
        'wtforms',
        'python-dotenv'
    ],
      zip_safe=False)