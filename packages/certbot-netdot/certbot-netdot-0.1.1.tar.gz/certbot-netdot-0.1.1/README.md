# Netdot DNS Authenticator for Certbot

This allows automatic completion of `Certbot's <https://github.com/certbot/certbot>`_
DNS01 challange for domains managed via `Netdot <https://github.com/cvicente/Netdot/>`_ DNS.

## Installing

```
$ sudo pip install certbot-netdot
```

Note that you should normally install this as ``root``, unless you know what
you are doing.

## Usage

The plugin requires a user with the edit, view and delete permissions for the DNS zone you
are creating a certificate in.

To use the plugin you need to provide a credentials file

`--certbot-netdot:credentials` *(required)*
  INI file with ``username`` and ``password`` for your Netdot user as well as the endpoint
  URL for your netdot instance. You can also provide the `verify` flag to disable certificate
  verification of the netdot server. This should of course only be used when you want to generate
  the certificate for your netdot server itself :)

The credentials file must have the following format:

```
certbot_netdot:auth_username = admin
certbot_netdot:auth_password = password
certbot_netdot:auth_endpoint = https://netdot.example.com/netdot
certbot_netdot:auth_verify = True
```

For safety reasons the file must not be world readable. You can solve this by
running:

```
$ chmod 600 credentials.ini
```

Then you can run `certbot` using:

```
$ sudo certbot certonly \
    --authenticator certbot-netdot:auth \
    --certbot-netdot:auth-credentials credentials.ini \
    -d domain.com
```

## Attribution


This plugin is based on https://github.com/runfalk/certbot-loopia by Andreas Runfalk

## Changelog

### Version 0.1.1

Released 2020-05-15

* Default cert verification to True
* Fixed generating wildcard certs or other multiple certs for a single domain name

### Version 0.1.0

Released 2020-05-11

* Initial Release
