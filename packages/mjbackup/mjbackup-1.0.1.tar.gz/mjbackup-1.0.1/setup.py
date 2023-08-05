import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mjbackup", # Replace with your own username
    version="1.0.1",
    author="morningjoe",
    author_email="morningjoe@morningjoesoftware.com",
    description="Morning Joe Software Linux Server Backup System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.morningjoesoftware.com",
    download_url="https://github.com/morningjoesoftware/mjbackup/archive/v1.0.1.tar.gz",
    packages=setuptools.find_packages(),
    data_files=[('configs', ['conf/backup1.xml', 'conf/backup2.xml', 'conf/backup3.xml', 'conf/mjbackupConfig.xml', 'conf/mjbackupMysql.conf', 'conf/mjbackupPgsql.conf', 'conf/mjsync.conf']),
            ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Archiving :: Compression',
    ],
    platforms=['posix'],
    python_requires='>=3.6',
)