from telegram import ParseMode

from utils.parsers import pars_args
from utils.wrappers import UpdateWrapper

from .bot import bot, stat


@bot.command('w', pass_args=True)
def weight(bot, update, args):
    # get info about user
    u = UpdateWrapper(update)
    print('Full name: ', u.get_full_name())
    print('Text: ', u.get_msg_text())
    print('Username: ', u.get_username())


    # a = pars_args(args, {'weight': 'int'})
    # a = pars_args(args, ['weight'])

    # pars taken args
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

    if not a.weight:
        # if user does not pass his weight as argument
        # send help message to him
        bot.send_message(
            chat_id=u.chat_id,
            text=a.help,
            parse_mode=ParseMode.MARKDOWN
        )
        return

    print('weight: ', a.weight, 'kg')

    err = stat.push_metric('weight', {'val': a.weight})
    if err:
        # send to user message with details about error
        bot.send_message(
            chat_id=u.chat_id,
            text=err,
        )

    else:
        # if all is well
        # send to user success message
        bot.send_message(
            chat_id=u.chat_id,
            text=f'Your current weight ({a.weight} kg) saved to database.',
            parse_mode=ParseMode.MARKDOWN
        )


@bot.command('start')
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