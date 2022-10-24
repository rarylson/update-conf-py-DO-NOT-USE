update-conf.py
==============

[![Test Status](https://github.com/rarylson/update-conf.py/actions/workflows/tests.yml/badge.svg?branch=master&event=push)](https://github.com/rarylson/update-conf.py/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/rarylson/update-conf.py/badge.svg?branch=master)](https://coveralls.io/github/rarylson/update-conf.py?branch=master)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/update-conf.py.svg)](https://pypi.python.org/pypi/update-conf.py/)
[![PyPI - Version](https://img.shields.io/pypi/v/update-conf.py.svg)](https://pypi.python.org/pypi/update-conf.py/)
[![License](https://img.shields.io/pypi/l/update-conf.py.svg)](LICENSE)

Generate config files from `conf.d` like directories.

Split your config file into smaller files, called snippets, in a `conf.d` like directory. The generated config file will be the concatenation of all snippets, with snippets ordered by the lexical order of their names.

Files ending with `.bak`, `.old` and other similar terminations will be ignored.

This project was based on the [update-conf.d project](https://github.com/Atha/update-conf.d).

Install
-------

This project works in Python 3 (3.7 or newer).

To install:

```bash
pip install update-conf.py
```

It's possible to clone the project in Github and install it via `setuptools`:

```bash
git clone git@github.com:rarylson/update-conf.py.git
cd update-conf.py
python setup.py install
```

Usage
-----

To generate a config file, you can run something like this:

```bash
update-conf.py -f /etc/snmp/snmpd.conf
```

The example above will merge the snippets in the directory `/etc/snmp/snmpd.conf.d` into the file `/etc/snmp/snmpd.conf`.

If the directory containing the snippets uses a diferent name pattern, you can pass its name as an argument:

```bash
update-conf.py -f /etc/snmp/snmpd.conf -d /etc/snmp/snmpd.d
```

It's also possible to define frequently used options in a config file. For example, in `/etc/update-conf.py.conf`:

```ini
[snmpd]
file = /etc/snmp/snmpd.conf
dir = /etc/snmp/snmpd.d
```

Now, you can run:

```bash
update-conf.py -n snmpd
```

To get help:

```bash
update-conf.py --help
```

### Config files

`update-conf.py` will use the global config file (`/etc/update-conf.py.conf`) or the user-home config file (`~/.update-conf.py.conf`) if they exist.

You can use the the sample config file (provided within the distributed package) as a start point:

```bash
cp ${prefix}/share/update-conf.py/update-conf.py.conf /etc/update-conf.py.conf
```

It's also possible to pass a custom config file via command line args:

```bash
update-conf.py -c my_custom_config.conf -n snmpd
```

License
-------

This software is released under the [Revised BSD License](LICENSE).

Changelog
---------

Check the [CHANGELOG](CHANGELOG.md) page.

Contributing
------------

If you want to contribute with this project, check the [CONTRIBUTING](CONTRIBUTING.md) page.

TODO
----

- Publish this software in a Ubuntu PPA.
