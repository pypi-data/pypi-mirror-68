from distutils.core import setup
setup(
  name = 'pyzer',         
  packages = ['pyzer'],   
  scripts=['scripts/pyzer'],
  version = '0.3',      
  license='MIT',        
  description = 'Simple analyzer for some standard files, creating visual graphs from them',
  author = 'Ualter Azambuja Junior',                   
  author_email = 'ualter.junior@gmail.com',      
  url = 'https://github.com/ualter/py-analyzer',   
  download_url = 'https://github.com/ualter/py-analyzer/archive/v0_3.tar.gz',    
  keywords = ['ANALYSIS', 'GRAPH', 'DRAWIO', 'CSV'],   
  install_requires=[            
          'PyYAML'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)