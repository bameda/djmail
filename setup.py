from setuptools import find_packages, setup

description = """
Simple, powerful and non-obstructive django email middleware.
"""

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='djmail',
    url='https://github.com/bameda/djmail',
    author='Andrey Antukh',
    author_email='niwi@niwi.nz',
    maintainer='David Barragán Merino',
    maintainer_email='bameda@dbarraagan.com',
    license='BSD',
    version='2.0.0',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    description=description.strip(),
    long_description=long_description,
    long_description_content_type='text/x-rst',
    zip_safe=False,
    include_package_data=True,
    package_data={
        '': ['*.html'],
    },
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ]
)
