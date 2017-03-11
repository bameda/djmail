from setuptools import find_packages, setup

description = """
Simple, powerful and non-obstructive django email middleware.
"""

setup(
    name='djmail',
    url='https://github.com/bameda/djmail',
    author='Andrey Antukh',
    author_email='niwi@niwi.nz',
    maintainer='David Barragán Merino',
    maintainer_email='bameda@dbarraagan.com',
    license='BSD',
    version='1.0.1',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    description=description.strip(),
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ]
)
