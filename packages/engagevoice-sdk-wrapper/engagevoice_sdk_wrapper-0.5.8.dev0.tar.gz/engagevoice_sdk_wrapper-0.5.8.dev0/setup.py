from setuptools import setup, find_packages
import sys, os

version = '0.5.8'

setup(name='engagevoice_sdk_wrapper',
      version=version,
      description="RingCentral Engage Voice SDK Wrapper for Python",
      long_description="""\
""",
      classifiers=[], 
      keywords='RingCentral, Engage Voice, Contact Center',
      author='Phong Vu',
      author_email='phong.vu@ringcentral.com',
      url='http://engage.ringcentral.com',
      license='',
      packages=find_packages(exclude=[]),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
            'requests'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
