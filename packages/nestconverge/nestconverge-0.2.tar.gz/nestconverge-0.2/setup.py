from distutils.core import setup

setup(name='nestconverge',
      version='0.2',
      packages=['nestconverge'],
      license='Creative Commons Attribution-Noncommercial-Share Alike license',
      description='Convergence Criterion for Nested Sampling chains',
      long_description='Convergence Criterion for Nested Sampling chains. For more information, check: https://github.com/Pablo-Lemos/NestConverge',
      entry_points = {'console_scripts': ['nestconverge=nestconverge.command_line:main']},
      author='Pablo Lemos',
      author_email='pablo.lemos.18@ucl.ac.uk',
      url='https://github.com/Pablo-Lemos/NestConverge'
      )

