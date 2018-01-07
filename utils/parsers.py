"""
    module: parsers.py
"""

CASTERS = {
    'int': int,
    'str': str,
    'float': float,
}


def cast_to(caster, val, default=None, raise_exception=False):
    """
    :param caster: callable that will be using for casting
    :param val: value that will be casted
    :param default: default value if exception will be raised
    :param raise_exception: bool, if `True` than exception will
        not be suppressed but raised. If `False` than default
        value will be returned
    :return: casted value or default
    """
    try:
        if callable(caster):
            return caster(val)
        elif isinstance(caster, str):
            cast = CASTERS.get(caster)
            if cast:
                return cast(val)
        raise Exception('Unknown caster')
    except (ValueError, TypeError) as err:
        if raise_exception:
            raise err
        return default


class BaseArgsParser:
    """Provide base functionality for parsing command arguments.
    Params:
        :param args: list of the arguments names that command can take.
            Take in mind that order is counts.

    Usage:
        >>> # define your own args parser
        >>> class MyArgsParser(BaseArgsParser):
        ...     args = ['first', 'second', 'third']
        ...
        >>> # create template list for testing
        >>> args = [1, 3, 'some text']

        >>> # pass args to the out args parser
        >>> my_args_parser = MyArgsParser(args)

        >>> # and that we can take parsed arguments
        >>> # by the names that we provided earlie
        >>> my_args_parser.first # prints: 1
        >>> my_args_parser.second # prints: 3
        >>> my_args_parser.third # prints: 'some text'
        >>>
        >>> # if you want to validate taken arguments
        >>> # than define 'args' as the dictionary
        >>> # for example:
        >>> class MyArgsParser2(BaseArgsParser):
        ...     args = {
        ...         'integer': 'int', # just cast to type
        ...         'string': {
        ...             'type': 'str', # cast to type `str`
        ...             'validators': [validate, ...] # additional validators
        ...             'help': [validate, ...] # help text that will be
        ...                                     # displayed if user pass
        ...                                     # invalid arg or does pass
        ...                                     # a ny args
        ...         },
        ...         'val': [check_len, check_conent] # just call validators
        ...     }
        ...
        >>> # validator is just a function that takes an value as argument
        >>> # and returns validated value
        >>> def validate(val):
        ...     # perform validation
        ...     return val
        >>> my_args_parser.help # returns help text for arguments

    """

    # defines list of the arguments names to which will be mapped values
    args = []

    def __init__(self, args):
        # map of the arguments names and their values
        self._args_map = {}

        # list of the arguments values
        self.values = args

        # map arguments values to their names
        self._map()

    def __getattr__(self, argname):
        cls = self.__class__

        if hasattr(cls, argname):
            # returns attr of the args parser class
            return getattr(self, argname)

        # else returns arguments values by their
        # arguments names from args map
        return self._args_map.get(argname)

    def __bool__(self):
        return bool(self._args_map)

    @property
    def help(self):
        args_list = ''
        tmp = '`{name}` --> {description};\n'

        if isinstance(self.args, list):
            # just list arguments names
            for name in self.args:
                args_list += tmp.format(name=name,
                                        description='no detail')

        elif isinstance(self.args, dict):

            for name, val in self.args.items():

                if isinstance(val, str):
                    # list arguments names and expected types
                    args_list += tmp.format(name=name, description=val)

                elif isinstance(val, list):
                    # list arguments names and validators names
                    # todo/ i need to come up with something better
                    # todo/ than just show validators list as description
                    args_list += tmp.format(name=name, description=val)

                elif isinstance(val, dict):
                    # get provided help text
                    if val.get('help'):
                        args_list += tmp.format(
                            name=name, description=val.get('help'))
                    else:
                        # else just list args
                        args_list += tmp.format(
                            name=name, description='no detail')

        return f'This command takes the arguments: \n\n{args_list}'

    def _cast(self, caster, argname):
        # cast value using specified caster
        self._args_map[argname] = cast_to(
            caster, self._args_map.get(argname)
        )

    def _run_validators(self, validators, val):
        # runs validators for val and save validated
        # value to the args map
        if not validators:
            return

        for validator in validators:
            # validator must be callable
            assert callable(validator)

            # run validation and save validated value to args_map
            self._args_map[val] = validator(self._args_map[val])

    def _map(self):
        """Performs mapping arguments values to their arguments names.
        Also performs validation for these values.
        """
        if isinstance(self.args, list):
            # just map values to their names
            self._args_map = dict(zip(self.args, self.values))

        elif isinstance(self.args, dict):
            names = self.args.keys()
            self._args_map = dict(zip(names, self.values))
            for name, val in self.args.items():

                if isinstance(val, str):
                    # cast value to specified type
                    self._cast(val, self._args_map.get(name))

                elif isinstance(val, list):
                    # perform validation
                    self._run_validators(val, name)

                elif isinstance(val, dict):
                    # try cast to type at first
                    self._cast(val.get('type'), self._args_map.get(name))

                    # perform validation
                    self._run_validators(val.get('validators'), name)


# util class for using it in the `pars_args` function
__arg_parser = type('ParseResult', (BaseArgsParser, ), {})


def pars_args(args, args_names):
    """Util that prevent us from creation of redundant classes,
    and just provide functionality that we really needs.

    Params:
        :param args: list of the arguments to parse;
        :param args_names: list of the arguments names
            to which will be mapped values.

    Usage:
        >>> # create template list for testing
        >>> args = [1, 3, 'some text']
        >>> mapped = pars_args(args, ['first', 'second', 'third'])
        >>> mapped.first # prints: 1
        >>> mapped.second # prints: 4
        >>> mapped.third # prints: 'some text'

        >>> a = pars_args(
        >>>     args,
        >>>     {
        >>>         'weight': {
        >>>             'type': 'float',
        >>>             'help': 'Pass your weight as the'
        >>>                     'first argument for this command'
        >>>         },
        >>>         'age': {
        >>>             'type': 'int',
        >>>             'help': 'Pass your age as the second argument'
        >>>         },
        >>>     }
        >>> )
    """
    __arg_parser.args = args_names
    return __arg_parser(args)
