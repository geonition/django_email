from setuptools import setup
from setuptools import find_packages

setup(
    name='email_rest',
    version='2.0.1',
    author='Kristoffer Snabb',
    url='https://github.com/geonition/django_email_rest',
    packages=find_packages(),
    include_package_data=True,
    package_data = {
        "email_rest": [
            "templates/*.js",
            "templates/*.html",
            "templates/emailconfirmation/*.txt",
            "templates/emailconfirmation/*.html"
        ],
    },
    zip_safe=False,
    install_requires=['django']
)
