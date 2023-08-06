# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_sso_credential_process']

package_data = \
{'': ['*']}

install_requires = \
['botocore>=1.16.0',
 'docutils>=0.10,<0.16',
 'jmespath>=0.7.1,<1.0.0',
 'python-dateutil>=2.1,<3.0.0',
 'urllib3>=1.20,<1.26']

entry_points = \
{'console_scripts': ['aws-configure-sso-profile = '
                     'aws_sso_credential_process.aws_configure_sso_profile:main',
                     'aws-sso-configure-profile = '
                     'aws_sso_credential_process.aws_configure_sso_profile:main',
                     'aws-sso-credential-process = '
                     'aws_sso_credential_process.aws_sso_credential_process:main']}

setup_kwargs = {
    'name': 'aws-sso-credential-process',
    'version': '0.2.1',
    'description': 'Bring AWS SSO-based credentials to the AWS SDKs until they have proper support',
    'long_description': None,
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
