# appel-crises-web

## for developers

On first time,

- Install `python3.7` if needed
- Install `pre-commit` if needed (`pip install --user pre-commit`)
- Install a python virtualenv manager if needed (`pip install --user vex`, `pip install --user pew`, ...)
- Create a virtualenv (`vex --make appel-crises`, `pew new appel-crises`)
- Install project dependencies: `make bootsrap` (or `pip install -e .[dev]` if make isn't available)
- `cp local_settings.ini.template local_settings.ini` and edit `local_settings.ini`
  if you need
- if you chose postgresql DB, create user and database if needed
- run `make build` to build static files
- run `./manage.py migrate` to create DB tables
- run `./manage.py createsuperuser` to create a local user

## Dependencies management

Dependencies are stored in `setup.cfg`:

- Runtime dependencies are listed under `install_requires` in the `[options]` section;
- Additional development dependencies are listed under `dev=` in the `[options.extras_require]`,
  and installed alongside required dependencies by specifying the `[dev]` extra marker -
  as seen in `pip install -e .[dev]`.


## Building

The project is not composed only of pure Python code (it contains templates, images, ...).
Some of those files must go through some processing before running in production:
- Static files should be consolidated into a single tree, with hashed names and a manifest;
- Message catalogs might need to be compiled to their final `.mo` form;
- Some static data might be converted to some other formats for faster / easier loading.

Those steps are controlled through the project wide `Makefile`, and should be called
through the `make build` (or simply `make`) command.

That step is also executed when building a release.


## Releasing

A release consists of a built project archive, under the `wheel` format; that package MUST include the result of a full compilation.
