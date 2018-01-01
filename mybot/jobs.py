from .bot import bot


@bot.job(interval=1000, first=1000, repeating=True)
def send_hello(bot, job):
    from pprint import pprint

    print('job: ')
    pprint(vars(job))