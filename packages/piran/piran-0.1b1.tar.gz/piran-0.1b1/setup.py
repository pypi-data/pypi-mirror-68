from os import path
from setuptools import setup, Extension, find_packages

pigen_module = Extension(
    name='pigen',
    sources = ['src/piran/pigen.c']
)

here = path.abspath(path.dirname(__file__))
github = 'https://github.com/Firefnix/PiRan'

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# python3 -m pip install -e git+https://https://github.com/Firefnix/PiRan.git#egg=piran
setup(
    name='piran',
    version='0.1b1',
    description='"Random" numbers based in pi\'s decimals',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=github,
    author='Firefnix',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='math pi random',
    package_dir={'piran': 'src'},
    packages=['piran'],
    python_requires='>=3.5, <4',
    project_urls={
        'Bug Reports': 'https://github.com/Firefnix/PiRan/issues',
        'Source': github
    },
    license='LGPLv3',
    ext_modules=[pigen_module],
    package_data={'piran': ['src/piran/pigen.so']},
)
