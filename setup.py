from distutils.core import setup

name = 'PyGML'
description = "Read and write Graffiti Markup Language (GML)"
author = 'David Keegan'
author_email = 'keegan3d@gmail.com'

setup(name=name,
    version='1.0',
    description=description,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    url='http://bitbucket.org/keegan3d/pygml',
    download_url='http://bitbucket.org/keegan3d/pygml/downloads/',
    license='MIT - See LICENSE file',
    keywords=['gml','api', 'graffiti'],
    platforms=['Independant'],  
    long_description=description,
    packages = [name],
    )