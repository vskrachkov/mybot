from telegram import (
    ext, InlineQueryResultArticle, InputTextMessageContent,
    ParseMode)

from tlib import T

t = T(token='338265680:AAHPlTOyS91BFJ1mA_4xfHGoCoAngnVakj0')

### push to server (stat_app_client)
def push_weight(weight):
    print(f'pushed to server, value : {weight}')


### utils.py
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
    """
    __arg_parser.args = args_names
    return __arg_parser(args)


class UpdateWrapper:
    """Wrapper for <class 'telegram.update.Update'>.
    Class that wraps the objects and provide additional methods
    to them or override existing ones. Helper methods prevents
    you from using multiple dots in your code.

    Be free to inherit from this class and extend existing functionality.
    """
    def __init__(self, update):
        self._origin = update

    def __getattr__(self, item):
        cls = self.__class__

        if hasattr(cls, item):
            # returns attr of the wrapper
            return getattr(self, item)

        # else returns attr of the origin object
        return getattr(self._origin, item)

    @property
    def chat_id(self):
        """Returns id of the chart in which message was sent."""
        return self.message.chat_id

    def get_msg_text(self):
        """Returns text of the user message."""
        return self.message.text

    def get_msg_date(self):
        """Returns date when the user message was sent."""
        return self.message.date

    def get_username(self):
        """Returns 'username' of the user whom sent the message."""
        return self.message.chat.username

    def get_full_name(self):
        """Returns 'full_name' of the user whom sent the message."""
        return f'{self.message.chat.first_name} ' \
               f'{self.message.chat.last_name}'

    def get_photos(self):
        """Returns list of the photos pinned to the message."""
        return self.message.photo

    def get_stickers(self):
        """Returns list of the stickers that was sent by user."""
        return self.message.sticker

    def get_video(self):
        """Returns the video that pinned to the message."""
        return self.message.video


### commands.py
@t.command('w', pass_args=True)
def weight(bot, update, args):
    # pars taken args
    # a = pars_args(args, {'weight': 'int'})
    a = pars_args(
        args,
        {
            'weight': {
                'type': 'float',
                'help': 'Pass your weight as the'
                        'first argument for this command'
            },
            'age': {
                'type': 'int',
                'help': 'Pass your age as the second argument'
            },
        }
    )
    # a = pars_args(args, ['weight'])
    push_weight(a.weight)
    print('weight: ', a.weight, 'kg')

    # get info about user
    u = UpdateWrapper(update)
    print('Full name: ', u.get_full_name())
    print('Text: ', u.get_msg_text())
    print('Username: ', u.get_username())

    if not a.weight:
        bot.send_message(
            chat_id=u.chat_id,
            text=a.help,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        bot.send_message(
            chat_id=u.chat_id,
            text=f'Your current weight ({a.weight} kg) saved to database.',
            parse_mode=ParseMode.MARKDOWN
        )


@t.command('start')
def start(bot, update):
    from pprint import pprint

    print('bot: ')
    pprint(vars(bot))

    print('message text: ', update.message.text)
    print('date: ', update.message.date)
    print('username: ', update.message.chat.username)
    print('chat_id: ', update.message.chat_id)
    print('photos list: ', update.message.photo)
    print('stickers: ', update.message.sticker)
    print('video: ', update.message.video)

    print('Full name: ',
          f'{update.message.chat.first_name} '
          f'{update.message.chat.last_name}')

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello i am your updated bot !"
    )


### messages.py
@t.message(ext.Filters.command)
def unknown_msg(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command."
    )


### inline.py
@t.inline
def upper_or_lower(bot, update):
    q = update.inline_query.query

    if not q:
        return

    results = list()
    results.append(
        InlineQueryResultArticle(
            id=q.upper(),
            title='Upper',
            input_message_content=InputTextMessageContent(q.upper())
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=q.lower(),
            title='Lower',
            input_message_content=InputTextMessageContent(q.lower())
        )
    )

    bot.answer_inline_query(update.inline_query.id, results)


### jobs.py
@t.job(interval=1000, first=1000, repeating=True)
def send_hello(bot, job):
    from pprint import pprint

    print('job: ')
    pprint(vars(job))

### errors.py
@t.error
def errors_handler(bot, update, error):
    print(error)


if __name__ == '__main__':
    t.run()