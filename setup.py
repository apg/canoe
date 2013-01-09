from setuptools import setup, find_packages

setup(
    name = "canoe",
    version = __version__,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'canoe = canoe.main:main',
        ],
        },
    author = "Andrew Gwozdziewycz",
    author_email = "apg@okcupid.com",
    description = "Carve out log files and paddle",
    license = "GPL",
    keywords = "log analyze alert monitor",
    url = "https://github.com/apgwoz/canoe",
)
