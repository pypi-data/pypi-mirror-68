from distutils.core import setup
import setuptools

def readme():
    with open(r'README.txt') as f:
        README = f.read()
    return README

setup(
    name = 'imgdownloader',
    packages = setuptools.find_packages(),
    version = '1.2',
    license='MIT',
    description = 'Use this library to download any image from a given URL.',
    author = 'Ankit Raj Mahapatra',
    author_email = 'ankitrajjitendra816@gmail.com',
    url = 'https://github.com/Ankit404butfound/pydownimg',
    download_url = 'https://github.com/Ankit404butfound/pydownimg',
    keywords = ['download'],
    install_requires=[
          'opencv-python',
          'numpy',
      ],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type="text/markdown",
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
