=======
History
=======

0.0.11 (2020-05-15)
-------------------

- Added the 'max_rate' arg to `up()` function.


0.0.10 (2020-04-20)
-------------------

- All MarathonApp args must be strings.


0.0.9 (2020-04-20)
------------------

- Session memory argument `mem` must be string for marathon strange enough.


0.0.8 (2020-04-16)
------------------

- Added the `pause_timeout` arg to the `up()` function.


0.0.7 (2020-02-19)
------------------

- Strip the 'simulation-' prefix when querying for the docker container_list to
  ensure uniformity between all carriers.


0.0.6 (2020-01-27)
------------------

- Use a generic `envs` arg that will set the container env variables.

- Added args `sim_uid, sim_ref_datetime, end_time, duration and start_mode` to
  container CMD.


0.0.5 (2020-01-17)
------------------

- Use generic marathon constraints settings.


0.0.4 (2019-12-19)
------------------

- Added support for host and ip lookups.


0.0.3 (2019-12-19)
------------------

- Catch also `ImportErrors` for simple settings.


0.0.2 (2019-12-19)
------------------

- Rename env var only_initialize to scheduler_action.


0.0.1 (2019-12-19)
------------------

* First release on PyPI.
