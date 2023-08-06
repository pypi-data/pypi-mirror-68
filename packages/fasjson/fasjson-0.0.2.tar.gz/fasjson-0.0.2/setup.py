# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fasjson',
 'fasjson.lib',
 'fasjson.lib.ldap',
 'fasjson.tests',
 'fasjson.tests.unit',
 'fasjson.web',
 'fasjson.web.apis',
 'fasjson.web.extensions',
 'fasjson.web.resources',
 'fasjson.web.utils']

package_data = \
{'': ['*'], 'fasjson.tests': ['fixtures/*']}

install_requires = \
['Flask>=1.1.1,<2.0.0',
 'dnspython>=1.16.0,<2.0.0',
 'flask-healthz>=0.0.1,<0.0.2',
 'flask-restx>=0.2.0,<0.3.0',
 'gssapi>=1.6.2,<2.0.0',
 'python-freeipa>=1.0.5,<2.0.0',
 'python-ldap>=3.2.0,<4.0.0',
 'requests-kerberos>=0.12.0,<0.13.0',
 'typing>=3.7.4.1,<4.0.0.0']

setup_kwargs = {
    'name': 'fasjson',
    'version': '0.0.2',
    'description': 'fasjson makes it possible for applications to talk to the fedora account system.',
    'long_description': '# Fedora Account System / IPA JSON gateway\n\n## Installation\n\nInstall dependencies\n\n```\ndnf install ipa-client httpd mod_auth_gssapi mod_session python3-mod_wsgi python3-poetry\n```\n\nInstall WSGI app\n\n```\npoetry config virtualenvs.create false\npoetry install\ncp ansible/roles/fasjson/files/fasjson.wsgi /srv/\n```\n\nEnroll the system as an IPA client\n\n```\n$ ipa-client-install\n```\n\nGet service keytab for HTTPd\n\n```\nipa service-add HTTP/$(hostname)\nipa servicedelegationrule-add-member --principals=HTTP/$(hostname) fasjson-delegation\nipa-getkeytab -p HTTP/$(hostname) -k /var/lib/gssproxy/httpd.keytab\nchown root:root /var/lib/gssproxy/httpd.keytab\nchmod 640 /var/lib/gssproxy/httpd.keytab\n```\n\nConfigure GSSProxy for Apache\n\n```\ncp ansible/roles/fasjson/files/config/gssproxy-fasjson.conf /etc/gssproxy/99-fasjson.conf\nsystemctl enable gssproxy.service\nsystemctl restart gssproxy.service\n```\n\nConfigure temporary files\n\n```\ncp ansible/roles/fasjson/files/config/tmpfiles-fasjson.conf /etc/tmpfiles.d/fasjson.conf\nsystemd-tmpfiles --create\n```\n\nTune SELinux Policy\n\n```\nsetsebool -P httpd_can_connect_ldap=on\n```\n\nConfigure Apache\n\n```\nmkdir mkdir -p /etc/systemd/system/httpd.service.d\ncp ansible/roles/fasjson/files/config/systemd-httpd-service-fasjson.conf /etc/systemd/system/httpd.service.d/fasjson.conf\ncp ansible/roles/fasjson/files/config/httpd-fasjson.conf /etc/httpd/conf.d/fasjson.conf\nsystemctl daemon-reload\nsystemctl enable httpd.service\nsystemctl restart httpd.service\n```\n\n## Usage\n\n```\n$ kinit\n$ curl --negotiate -u : http://$(hostname)/fasjson/v1/groups/\n{"result": [{"name": "test-group", "uri": "http://$(hostname)/fasjson/v1/groups/test-group/"}]}\n$ curl --negotiate -u : http://$(hostname)/fasjson/v1/groups/admins/\n{"result": {"name": "test-group", "uri": "http://fasjson.example.test/fasjson/v1/groups/test-group/"}}\n$ curl --negotiate -u : http://$(hostname)/fasjson/v1/users/admin/\n{"result": {"username": "admin", "surname": "Administrator", "givenname": "", "emails": ["admin@$(domain)"], "ircnicks": null, "locale": "fr_FR", "timezone": null, "gpgkeyids": null, "creation": "2020-04-23T10:16:35", "locked": false, "uri": "http://$(hostname)/fasjson/v1/users/admin/"}}\n$ curl --negotiate -u : http://$(hostname)/fasjson/v1/me/\n{"result": {"dn": "uid=admin,cn=users,cn=accounts,dc=$(domain)", "username": "admin", "uri": "http://$(hostname)/fasjson/v1/users/admin/"}}\n```\n\n## TODO\n\n- documentation\n- HTTPS\n',
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/fasjson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
