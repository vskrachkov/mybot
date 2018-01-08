"""
    module: schema.py

    Defines basic class and utils for schema declaration and validation
"""
import warnings

from validation.errors import ValidationError


class Schema:
    """Basic class for schema declaration.
    Mostly for dict validation and for lists that consists of dicts

    Params::
        :param schema_declaration: list or dict which
            declare schema for validation

    Usage::
        >>> # define schema for dict structure validation
        >>> # key of the schema dictionary is the name of the key that expects
        >>> # the values are the type casters or validators.
        >>> # you can use default Python types as type casters or other
        >>> # classes callable objects that can cast or validate taken value
        >>>
        >>> # simple schema with just type casting
        >>> # if taken value cannot be casted the TypeError or
        >>> # ValueError will be raised in this case
        >>> schema = Schema({
        >>>     'id': int,
        >>>     'name': str,
        >>>     'age': int,
        >>>     'balance': Decimal
        >>> })
        >>> data = {
        >>>     'id': '12',
        >>>     'name': 'Bill Gates',
        >>>     'age': 63,
        >>>     'balance': '450005443.4'
        >>> }
        >>> # perform validation
        >>> schema.validate(data)
        >>>
        >>> # than you can access to validated data
        >>> schema.data
        >>> {
        >>>     'id': 12,
        >>>     'name': 'Bill Gates',
        >>>     'age': 63,
        >>>     'balance': Decimal('450005443.4')
        >>> }
        >>>
        >>> # if you want raise custom error on validation failing
        >>> # or provide custom error handling you can pass error_handler,
        >>> # callable that have takes errors list as an argument,
        >>> # each errors list item is a tuple contains
        >>> # key which are not validated as 0-position item,
        >>> # value of this key as 1-position item
        >>> # and raised error as 2-position item
        >>> def error_handler(errors):
        >>>     for err in errors:
        >>>         print(err)
        >>>
        >>> # in this case if error will be raised it will
        >>> # be wrapper by CustomValidationError
        >>> schema = Schema({'id': int}, error_handler=error_handler)
        >>> # also you can create schema for list of dicts validation
        >>> # just wrap you schema dict by list
        >>> # take in mind that if you pass more than one item to the list,
        >>> # that will do not have any effect
        >>> schema = Schema([{'id': int}])
        >>> a_list = [
        >>>     {'id': '2'},
        >>>     {'id': '3'},
        >>>     {'id': '4'},
        >>> ]
        >>> schema.validate(a_list)
        >>> schema.data
        >>> # returns
        >>> [
        >>>     {'id': 2},
        >>>     {'id': 3},
        >>>     {'id': 4},
        >>> ]
        >>> # for enabling nested schema validation pass `nested=True` argument
        >>> # define `User` schema
        >>> user_schema = Schema({
        >>>     'id': int
        >>>     'name': str
        >>> })
        >>> # define `Employee` schema with user_schema as the key value
        >>> employee_schema = Schema({
        >>>     'emp_id': int,
        >>>     'user': user_schema,
        >>>     'department': str
        >>> }, nested=True)
    """

    def __init__(self, schema_declaration, error_handler=None, nested=False,
                 validate_all=False):
        self._schema = schema_declaration
        self._error_handler = error_handler
        self._validate_all = validate_all
        self._nested = nested
        self._errors = []
        self._data = None

    def _validate_object(self, dict_data, schema):
        # check that taken data is a dict
        if not isinstance(dict_data, dict):
            raise ValidationError('Input data must be a dict')

        # and initialize result data as a dict
        self._data = {}

        # perform validation
        for key, val in dict_data.items():
            validator = schema[key]
            assert callable(validator), 'The value of the schema dict ' \
                                        'key must be a callable object'
            try:
                if self._nested and hasattr(validator, 'validate'):
                    # in case when we have nested schema and we also need
                    # to check that schema item key is a schema object
                    self._data[key] = validator.validate(val)
                self._data[key] = validator(val)
            except Exception as error:
                # save raised error to the errors list for processing
                # or ignoring it in the handle_errors method
                self._errors.append((key, val, error))

    def _validate_objects_list(self, list_data):
        # check that taken data also a dict
        if not isinstance(list_data, list):
            raise ValidationError('Input data must be a list')

        # get first argument as schema
        schema = self._schema[0]

        # and initialize result data as a list
        self._data = []

        # perform iteration throw the taken list
        for item in list_data:
            # for each item in the taken list we perform validation
            # and append validated item to the result object
            validated_item = self._validate_object(item, schema)
            self._data.append(validated_item)

            # also we need to check our error container if this container
            # is not empty than we do not need to perform validation
            # for remaining items. But if you want to perform validation of
            # the whole items, pass `validate_all=True` as an named argument.
            # In this case the structure of the errors container will be
            # the same but the container can contains duplicates.
            if self._errors:
                # check that user provide `_validate_all=True`
                # if argument are provided than we continue validation
                if self._validate_all:
                    continue
                # else break validation on the first item were we catch an error
                break

    def validate(self, data):
        if isinstance(self._schema, dict):
            self._validate_object(data, schema=self._schema)
        elif isinstance(self._schema, list):
            self._validate_objects_list(data)
        self.handle_errors(self._errors)

    def handle_errors(self, errors):
        if errors:
            if self._error_handler:
                assert callable(self._error_handler), \
                    'error_handler must be callable'
                self._error_handler(errors)
            else:
                warnings.warn(f'These errors: {self._errors} are not handled',
                              Warning)

    @property
    def data(self):
        if not self._data:
            warnings.warn('`data` attribute is empty, maybe you do not call '
                          'method `validate(data)` before accessing to '
                          'the `data` param or occurs some error which '
                          'you does not handle', Warning)
        return self._data