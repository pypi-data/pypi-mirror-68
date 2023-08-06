from setuptools import setup, find_packages


requirements = []

setup(
      name="ecli",
      version = "0.0.23", #@version@#
      description="handle,.in progressing..,APIs",
      author="ihgazni2",
      url="https://github.com/ihgazni2/ecli",
      author_email='', 
      license="MIT",
      long_description = "refer to .md files in https://github.com/ihgazni2/ecli",
      classifiers=[
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          ],
      packages= find_packages(),
      entry_points={
          'console_scripts': [
              'ecli_srch=ecli.bin.srch:main',
              'ecli_pobj=ecli.bin.pobj:main',
              'ecli_jsonq=ecli.bin.jsonq:main',
              'ecli_html_tagq=ecli.bin.htmlq:main_tagq',
              'ecli_html_attrq=ecli.bin.htmlq:main_attrq',
              'ecli_html_txtq=ecli.bin.htmlq:main_txtq',
              'ecli_lcp=ecli.bin.lcp:main',
              'ecli_ldd=ecli.bin.ldd:main',
              'ecli_lcut=ecli.bin.lcut:main',
              'ecli_abbr=ecli.bin.abbr:main'
          ]
      },
      package_data={
          'resources':['RESOURCES/*']
      },
      include_package_data=True,
      install_requires=requirements,
      py_modules=['ecli'], 
)


# python3 setup.py bdist --formats=tar
# python3 setup.py sdist


















