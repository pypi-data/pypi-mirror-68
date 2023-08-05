from distutils.core import setup
setup(
  name = 'WSI_handling',         
  packages = ['WSI_handling'],   
  version = '0.11',      
  license='MIT',        
  description = 'Convienent handling of annotated whole slide images',   
  author = 'Patrick Leo',                   
  author_email = 'pjl54@case.edu',      
  url = 'https://github.com/pjl54/WSI_handling/tree/pip_ready',   
  download_url = 'https://github.com/pjl54/WSI_handling/archive/v0.3.tar.gz',
  keywords = ['whole slide image', 'digital pathology', 'annotations'],
  install_requires=[
          'numpy',
		  'matplotlib',
		  'Pillow',
		  'opencv-python',
		  'shapely',
		  'openslide-python'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',    
    'License :: OSI Approved :: MIT License',    
    'Programming Language :: Python :: 3.6',
  ],
)
