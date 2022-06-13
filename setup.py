from setuptools import setup, find_packages

setup(
    name='src',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    setup_requires=['setuptools-git-version'],
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='',
    author='serbeh, terrorsl',
    author_email='',
    description='Simple Report Creator. For latex reports, etc.',
    requires=['PyPDF2']
)

# Собирать командой python setup.py bdist_wheel
