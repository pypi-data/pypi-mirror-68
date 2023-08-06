import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sphinx_target_theme', # Replace with your own username
    version='0.0.4',
    author=u'Klaus Kähler Holst',
    author_email='klaus@holst.it',
    description='Sphinx theme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['sphinx_target_theme'],
    entry_points={'sphinx.html_themes': ['sphinx_target_theme = '
                                         'sphinx_target_theme']},
    url='https://github.com/kkholst/sphinx_target_theme',
    classifiers=[
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Theme',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
    python_requires='>=3.5',
)
