# Flask feature flag

Tool to activate and deactivate project functionalities

[![pipeline status](https://gitlab.com/terminus-zinobe/flask-feature-flag/badges/master/pipeline.svg)](https://gitlab.com/terminus-zinobe/flask-feature-flag/-/commits/master) [![coverage report](https://gitlab.com/terminus-zinobe/flask-feature-flag/badges/master/coverage.svg)](https://gitlab.com/terminus-zinobe/flask-feature-flag/-/commits/master)


## Package installation
- Installation
    ```shell
    $ pip3 install flask-feature-flag
    ```

## Configuration

- Feature flag type availables.
    * FLASK_CONFIG
    * MONGO

- Define the following to your `config.py`
    ```python
    FEATURE_FLAG_TYPE=
    ```
    `FEATURE_FLAG_TYPE` is required.

- You should add this to your `config.py` if it's feature type `FLASK_CONFIG`
    ```python
    FEATURE_FLAGS = {
        'ROUTE_ENABLED': os.environ.get('ROUTE_ENABLED', True)
    }
    ```
    `FEATURE_FLAGS` is required.

## Docs

- [Flask-Feature-Flag’s documentation](https://flask-feature-flag-docs.readthedocs.io/en/latest/index.html)

Example:

`is_enabled` this decorator allows to activate or deactivate a functionality and receives as parameters a function to return in case feature is disabled and the name of the feature

    ```python
    from flask_feature_flag import is_enabled

    def error():
        return dict(massage='this is a mistake')

    @is_enabled(error, 'ENV_HELLO')
    def hello(name):
        return dict(message=f'Hi, {name}')
    ```