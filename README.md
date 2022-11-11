update-conf-py-DO-NOT-USE
=========================

> **IMPORTANT:** This is a fork of `update-conf.py` with the goal to test AWS CodePipeline as well as the whole AWS Code\* stack. This project should **NOT** be used in production.
>
> Also, the code will be stored into 2 repos: CodeCommit, to better test the full AWS Code\* stack; GitHub, as Coveralls free plan only supports it.

[![Test Status](https://img.shields.io/endpoint?label=tests&logo=amazonaws&url=https%3A%2F%2Fof958z8mzd.execute-api.us-east-1.amazonaws.com%2Fprod%2Fbuild-status%3Fuuid%3DeyJlbmNyeXB0ZWREYXRhIjoiOWZsM0ZQeXEwTWtXd3dIc3cyVFZBcFducUE3NVgrODduT21lMTRrUzMzRXJuQTFrS1oxd1pNcmZhalZscDFWSS9KNHFMQjNDSGdaUWJ1WDA5Vm44VzFnPSIsIml2UGFyYW1ldGVyU3BlYyI6Img0VkhSNlVkOG1HZUIrMGEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%253D%26branch%3Dmaster)](https://us-east-1.console.aws.amazon.com/codesuite/codebuild/projects/update-conf-py-DO-NOT-USE-tests/)
[![Coverage Status](https://img.shields.io/coveralls/github/rarylson/update-conf-py-DO-NOT-USE/master?logo=coveralls)](https://coveralls.io/github/rarylson/update-conf-py-DO-NOT-USE)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/update-conf-py-DO-NOT-USE?logo=python&logoColor=white)](https://pypi.python.org/pypi/update-conf-py-DO-NOT-USE/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/update-conf-py-DO-NOT-USE.svg)](https://pypi.python.org/pypi/update-conf-py-DO-NOT-USE/)
[![PyPI - Version](https://img.shields.io/pypi/v/update-conf-py-DO-NOT-USE.svg)](https://pypi.python.org/pypi/update-conf-py-DO-NOT-USE/)
[![License](https://img.shields.io/pypi/l/update-conf-py-DO-NOT-USE.svg)](LICENSE)

> Default CodeBuild badge: [![Test Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiOWZsM0ZQeXEwTWtXd3dIc3cyVFZBcFducUE3NVgrODduT21lMTRrUzMzRXJuQTFrS1oxd1pNcmZhalZscDFWSS9KNHFMQjNDSGdaUWJ1WDA5Vm44VzFnPSIsIml2UGFyYW1ldGVyU3BlYyI6Img0VkhSNlVkOG1HZUIrMGEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)](https://us-east-1.console.aws.amazon.com/codesuite/codebuild/projects/update-conf-py-DO-NOT-USE-tests/)
>
> Badge via custom API based on eventbridge CodeBuild events: [![Test Status](https://img.shields.io/endpoint?label=tests&logo=amazonaws&url=https%3A%2F%2Fizhet1gjri.execute-api.us-east-1.amazonaws.com%2Fprod%2Fbuild-status%3Fbuild-project%3Dupdate-conf-py-DO-NOT-USE-tests)](https://us-east-1.console.aws.amazon.com/codesuite/codebuild/projects/update-conf-py-DO-NOT-USE-tests/)
>
> Badge via custom API based on proxying the default CodeBuild badge: [![Test Status](https://img.shields.io/endpoint?label=tests&logo=amazonaws&url=https%3A%2F%2Fof958z8mzd.execute-api.us-east-1.amazonaws.com%2Fprod%2Fbuild-status%3Fuuid%3DeyJlbmNyeXB0ZWREYXRhIjoiOWZsM0ZQeXEwTWtXd3dIc3cyVFZBcFducUE3NVgrODduT21lMTRrUzMzRXJuQTFrS1oxd1pNcmZhalZscDFWSS9KNHFMQjNDSGdaUWJ1WDA5Vm44VzFnPSIsIml2UGFyYW1ldGVyU3BlYyI6Img0VkhSNlVkOG1HZUIrMGEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%253D%26branch%3Dmaster)](https://us-east-1.console.aws.amazon.com/codesuite/codebuild/projects/update-conf-py-DO-NOT-USE-tests/)

Generate config files from `conf.d` like directories.

Split your config file into smaller files, called snippets, in a `conf.d` like directory. The generated config file will be the concatenation of all snippets, with snippets ordered by the lexical order of their names.

Files ending with `.bak`, `.old` and other similar terminations will be ignored.

This project was based on the [update-conf.d project](https://github.com/Atha/update-conf.d).

Install
-------

This project works in Python 3 (3.7 or newer).

To install:

```bash
pip install update-conf-py-do-not-use
```

To install via AWS CodeArtifact:

```bash
CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
        --domain test --query authorizationToken --output text)
AWS_ACCOUNT=$(aws sts get-caller-identity --query "Account" --output text)
pip install update-conf-py-do-not-use \
        -i https://aws:${CODEARTIFACT_AUTH_TOKEN}@test-${AWS_ACCOUNT}.d.codeartifact.us-east-1.amazonaws.com/pypi/pypi/simple/
```

It's possible to clone the project in AWS CodeCommit and install it via `setuptools`:

```bash
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/update-conf-py-DO-NOT-USE
cd update-conf-py-DO-NOT-USE
python setup.py install
```

Usage
-----

To generate a config file, you can run something like this:

```bash
update-conf-py-do-not-use -f /etc/snmp/snmpd.conf
```

The example above will merge the snippets in the directory `/etc/snmp/snmpd.conf.d` into the file `/etc/snmp/snmpd.conf`.

If the directory containing the snippets uses a diferent name pattern, you can pass its name as an argument:

```bash
update-conf-py-do-not-use -f /etc/snmp/snmpd.conf -d /etc/snmp/snmpd.d
```

It's also possible to define frequently used options in a config file. For example, in `/etc/update-conf-py-do-not-use.conf`:

```ini
[snmpd]
file = /etc/snmp/snmpd.conf
dir = /etc/snmp/snmpd.d
```

Now, you can run:

```bash
update-conf-py-do-not-use -n snmpd
```

To get help:

```bash
update-conf-py-do-not-use --help
```

### Config files

`update-conf-py-do-not-use` will use the global config file (`/etc/update-conf-py-do-not-use.conf`) or the user-home config file (`~/.update-conf-py-do-not-use.conf`) if they exist.

You can use the the sample config file (provided within the distributed package) as a start point:

```bash
cp ${prefix}/share/update-conf-py-do-not-use/update-conf-py-do-not-use.conf /etc/update-conf-py-do-not-use.conf
```

It's also possible to pass a custom config file via command line args:

```bash
update-conf-py-do-not-use -c my_custom_config.conf -n snmpd
```

### More examples

Suppose you have 2 snippets. One is `/etc/snmp/snmpd.conf.d/00-main`:

```ini
syslocation Unknown
syscontact Root <root@localhost>
```

And the other is `/etc/snmp/snmpd.conf.d/01-permissions`:

```ini
rocommunity public 192.168.0.0/24
```

After running `update-conf-py-do-not-use -f /etc/snmp/snmpd.conf`, the generated config file will be:

```ini
# Auto-generated by update-conf-py-do-not-use
# Do NOT edit this file by hand. Your changes will be overwritten.

syslocation Unknown
syscontact Root <root@localhost>

rocommunity public 192.168.0.0/24
```

There are cases when it's useful to change the prefix used in the auto-generated comment. After running `update-conf-py-do-not-use -f /etc/php.ini -p ';'`, the generated config will start with:

```ini
; Auto-generated by update-conf-py-do-not-use
; Do NOT edit this file by hand. Your changes will be overwritten.
```

It's also possible to set the prefix used in the auto-generated comment via config file. For instance, in `/etc/update-conf-py-do-not-use.conf`:

```ini
[php]
file = /etc/php.ini
dir = /etc/php.d
prefix_comment = ;
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
