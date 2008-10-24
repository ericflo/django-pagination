import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

version = '1.0'

setup(
    name='pagination',
    version=version,
    description="django-pagination",
    long_description=open("docs/usage.txt").read(),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='pagination,django',
    author='Eric Florenzano',
    author_email='floguy@gmail.com',
    url='http://www.eflorenzano.com/',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
