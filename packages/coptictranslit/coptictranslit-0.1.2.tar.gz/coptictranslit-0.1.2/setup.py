from setuptools import setup 
  
# reading long description from file 
with open('README.md') as file: 
    long_description = file.read() 
  
  
# specify requirements of your package here 
REQUIREMENTS = ['pynini'] 
  
# some more details 
CLASSIFIERS = [ 
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.3', 
    'Programming Language :: Python :: 3.4', 
    'Programming Language :: Python :: 3.5', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ] 
  
# calling the setup function  
setup(name='coptictranslit', 
      version='0.1.2', 
      description='An inital release of a Coptic Transliterator', 
      long_description='The vision of this project is to provide an easy, bulk transliteration service between Coptic and Latin script. The primary use case (Coptic --> Latin script) is to allow English speakers who do not read Coptic to follow along with church services by offering transliterated text with accurate and transparent pronunciations. For more information visit out Github page at https://github.com/shehatamichael/coptic-transliteration', 
      url='https://github.com/shehatamichael/coptic-transliteration', 
      author='Michael Shehata', 
      author_email='shehatamichael4@gmail.com', 
      packages=['translit'], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords='Coptic'
      ) 