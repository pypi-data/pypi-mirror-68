# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fasjson_client', 'fasjson_client.tests', 'fasjson_client.tests.unit']

package_data = \
{'': ['*'], 'fasjson_client.tests.unit': ['fixtures/*']}

install_requires = \
['bravado>=10.6.0,<11.0.0',
 'gssapi>=1.6.5,<2.0.0',
 'requests-gssapi>=1.2.1,<2.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'fasjson-client',
    'version': '0.0.1',
    'description': 'An OpenAPI client for FASJSON',
    'long_description': "# fasjson-client\n\nA python client library for the FASJSON API\n\nThis client uses the bravado library to build dynamic api methods based on open-api specs (version 2.0): https://github.com/Yelp/bravado\n\n## Usage\n\nInstantiate the client with the FASJSON URL you want to use.\n\n```\n>>> from fasjson_client import Client\n>>> c = Client('http://fasjson.example.com')\n>>> c.me.whoami().response().result\n{'result': {'dn': 'uid=admin,cn=users,cn=accounts,dc=example,dc=test', 'username': 'admin', 'service': None, 'uri': 'http://fasjson.example.test/fasjson/v1/users/admin/'}}\n```\n\n## Authentication\n\nAuthentication is done with Kerberos. If you want to explicitely specify a principal to authenticate as, use the `principal` constructor argument.\n\n```\nc = Client('http://fasjson.example.com', principal='admin@EXAMPLE.TEST')\n```\n\n### Configuring an application for Kerberos authentication\n\nUsers authenticate via `kinit`, applications authenticate via keytabs. It is highly recommended to use [gssproxy](https://github.com/gssapi/gssproxy/]) in order to keep your keytabs secure.\n\n- First, install gssproxy with `dnf install gssproxy`\n- Create the service that you want to authenticate as in IPA: `ipa service-add SERVICE/host-fqdn` (for example `ipa service-add HTTP/server.example.com`)\n- Get the keytab for that service and store it in gssproxy's directory: `ipa-getkeytab -p SERVICE/host-fqdn -k /var/lib/gssproxy/service.keytab` (for example `ipa-getkeytab -p HTTP/server.example.com -k /var/lib/gssproxy/httpd.keytab`)\n- Add a configuration file for your service in gssproxy's configuration directory:\n\n```\n# /etc/gssproxy/50-servicename.conf\n\n[service/servicename]\n  mechs = krb5\n  cred_store = keytab:/var/lib/gssproxy/service.keytab\n  cred_store = client_keytab:/var/lib/gssproxy/service.keytab\n  allow_constrained_delegation = true\n  allow_client_ccache_sync = true\n  cred_usage = both\n  euid = user_the_service_runs_as\n```\n\nFor example:\n\n```\n# /etc/gssproxy/80-httpd.conf\n\n[service/httpd]\n  mechs = krb5\n  cred_store = keytab:/var/lib/gssproxy/httpd.keytab\n  cred_store = client_keytab:/var/lib/gssproxy/httpd.keytab\n  allow_constrained_delegation = true\n  allow_client_ccache_sync = true\n  cred_usage = both\n  euid = apache\n```\n\n- Restart gssproxy with `systemctl restart gssproxy`\n- Configure the service to run with the `GSS_USE_PROXY` environment variable set. Services started by systemd can be configured with a service configuration file, for example with the httpd service:\n\n```\n# /etc/systemd/system/httpd.service.d/gssproxy.conf\n# /usr/lib/systemd/system/httpd.service.d/gssproxy.conf\n\n[Service]\nEnvironment=KRB5CCNAME=/tmp/krb5cc-httpd\nEnvironment=GSS_USE_PROXY=yes\n```\n\nYour service should now be able to authenticate with Kerberos\n\n## Development\n\nInstall dependencies:\n\n```\npoetry install\n```\n\nRun the tests:\n\n```\ntox\n```\n\n## License\n\nLicensed under [lgpl-3.0](./LICENSE)\n",
    'author': 'Fedora Infrastructure',
    'author_email': 'infrastructure@lists.fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/fasjson-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
