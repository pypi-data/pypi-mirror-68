Multi backend for Taxi
======================

This is a special "multi" backend for [Taxi](https://github.com/sephii/taxi).
It allows pushing entries to multiple backends.

Installation
------------

```shell
taxi plugin install multi
```

Usage
-----

In your `.taxirc` file, use the `multi` protocol for your backend. The backends
parameter is a comma-separated list of the backends you want to push to.

```ini
[backends]
multi_backend = multi://?backends=my_tempo_backend,my_tipee_backend
```

Then define the backends a separate section:

```ini
[multi]
my_tempo_backend = tempo://jira_user_account_id:tempo_api_token@api.tempo.io/core/3/
my_tipee_backend = tipee://app_name:app_private_key@instance.tipee.net/api/?person=person_id
```
