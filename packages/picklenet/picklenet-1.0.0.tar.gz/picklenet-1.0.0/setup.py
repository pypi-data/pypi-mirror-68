import setuptools

# with open('README.md') as fp:
#     long_description = fp.read()
long_description = None

setuptools.setup(
    name = 'picklenet',
    version = '1.0.0',
    url = 'https://github.com/gaming32/picklenet',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'pickle-like interface for .NET serialization',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    install_requires = [
        'pythonnet; implementation_name != "IronPython"',
    ],
    py_modules = [
        'picklenet',
    ],
)