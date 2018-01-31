import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from bot.start import start_cmd
from bot.help import help_cmd_factory
from bot.calculator import calculator_cmd_factory
from bot.matches import matches_cmd, matches_cb
from bot.tictactoe import tictactoe_cmd, tictactoe_cb

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def common_cb_handler(bot, update):
    path, val = update.callback_query.data.split('_')
    update.callback_query.data = val

    if path == 'tictactoe':
        tictactoe_cb(bot, update)

    if path == 'matches':
        matches_cb(bot, update)

    if path == 'xo':
        pass


def run(env):
    if not env:
        raise Exception("No env")

    updater = Updater(env['TELEGRAM_TOKEN'])

    calc = calculator_cmd_factory(env['WOLFRAM_TOKEN'])
    help = help_cmd_factory(env['HELP_TEXT'])
    start = start_cmd

    updater.dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('help', help, pass_args=True))

    updater.dispatcher.add_handler(CommandHandler('calc', calc, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('tictactoe', tictactoe_cmd, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('matches', matches_cmd, pass_args=True))

    updater.dispatcher.add_handler(CallbackQueryHandler(common_cb_handler))


    updater.start_polling()
    updater.idle()
