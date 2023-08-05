import setuptools
import folder_organizer

setuptools.setup(
    name = 'folder-organizer',
    packages = [
        'folder_organizer',
        'folder_organizer.utils',
        'folder_organizer.interfaces'
    ],
    version = '1.2',
    description = 'A simple folder organizer',
    author = 'Unai Hernández',
    author_email = 'unihernandez22@yahoo.com',
    url = 'https://github.com/unihernandez22/folder-organizer/',
    download_url = 'https://github.com/unihernandez22/folder-organizer/tarball/0.1',
    keywords = ['folder', 'organizer', 'organization'],
    data_files = [('folder-organizer-resources', [
        'folder_organizer/resources/folder',
        'folder_organizer/resources/data.json'
    ])],
    install_requires=[
        'pyqt5',
        'setuptools'
    ],
    entry_points = {
        'console_scripts': [
            'folder-organizer=open:main'
        ]
    }
)
