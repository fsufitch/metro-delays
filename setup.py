from setuptools import setup, find_packages

setup(name='metrodelay',
      version='0.1',
      description='metrodelayed.me, for those who want to know what the Metro is really doing',
      author='Filip Sufitchi',
      author_email='fsufitchi@gmail.com',
      packages=find_packages('src'),
      package_dir={'':'src'},
      include_package_data=True,
      install_requires=[''],
      entry_points = {"console_scripts": [
            'dump_network=metrodelay.common.scripts.metronetwork:main'
            ]},
  )
