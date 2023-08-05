from distutils.core import setup
from setuptools import find_packages


files = ["Commercial/*","Payment/*","Util/*","Commercial/ECRM/*","Payment/Transfermovil/*","Util/APIDevice/*"]

setup(
  name = 'etecsa-sdk',
  packages = ['EtecsaSDK'],
  package_data = {'EtecsaSDK' : files },
   
  version = '1.3',     
  license='MIT',       
  description = 'Etecsa SDK',  
  author = 'sebastian',
  author_email = 'sebastian.rodriguez@etecsa.cu',      
  url = 'https://github.com/sebastiancuba/etecsa-sdk',  
  download_url = 'https://github.com/sebastiancuba/etecsa-sdk/archive/v1.3.tar.gz',    
  keywords = ['sdk'], 
  install_requires=[
      'requests',
      'validators',
      'pendulum',
      'pyyaml',
      'parser',
      'user-agents'
          ],
  classifiers=[
    'Programming Language :: Python :: 3.8',
  ],
)