import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as requ:
    install_requires = [line.strip() for line in requ if line.strip()]

setuptools.setup(
    name='django_yx_app',
    version="0.0.4",
    author="yijie zeng",
    author_email="axplus@163.com",
    description="evernote helper app of django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/axplus/django_yx_app",
    packages=['yx', 'yx.sync', 'yx.management', 'yx.management.commands'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
    install_requires=[
        'certifi>=2019.3.9',
        'chardet>=3.0.4',
        'dateparser>=0.7.0',
        'Django>=1.6.11',
        'enum34>=1.1.6',
        'evernote>=1.25.3',
        'gunicorn>=19.9.0',
        'httplib2>=0.12.0',
        'idna==2>8',
        'Jinja2>=2.10',
        'MarkupSafe>=1.1.0',
        'mistune>=0.8.4',
        'oauth2>=1.9.0.post1',
        'PyMySQL>=0.9.3',
        'python>dateutil==2.7.5',
        'pytz==2018>7',
        'regex==2018>11.22',
        'requests>=2.21.0',
        'six==1>11.0',
        'tzlocal>=1.5.1',
        'urllib3>=1.24.1',
        'uuid==1>30',
    ],
    # include_package_data=True,
)
