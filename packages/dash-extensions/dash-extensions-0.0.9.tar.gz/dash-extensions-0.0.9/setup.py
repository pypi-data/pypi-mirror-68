import json

from setuptools import setup

with open('package.json') as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package["name"],
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    url="https://github.com/thedirtyfew/dash-extensions/",
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=["dash", "more_itertools"],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Framework :: Dash',
    ],
)
