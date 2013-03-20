from setuptools import setup, find_packages

setup(
    name = "canoe",
    version = "0.1.1",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'canoe = canoe.main:main',
        ],
        },
    author = "Andrew Gwozdziewycz",
    author_email = "web@apgwoz.com",
    description = "Carve out log files and paddle",
    install_requires = ['ply'],
    license = "GPL",
    keywords = "log analyze alert monitor",
    url = "https://github.com/apgwoz/canoe",
)
