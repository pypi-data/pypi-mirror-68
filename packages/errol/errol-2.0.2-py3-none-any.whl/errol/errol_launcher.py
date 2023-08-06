#!/usr/bin/env python3
# Copyright (c) 2018 errol project
# This code is distributed under the GPLv3 License

from errol import watcher
from errol import xmpp
from errol import config_parser
from configparser import NoSectionError, NoOptionError
import logging
import argparse
import asyncio

logging.getLogger("asyncio").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class ErrolLauncher:
    def __init__(self, conf):
        self.conf = conf

    def conf_getter(self):
        return self.conf

    async def launcher(self, ):

        if self.conf['command'] == "xmpp":
            xmpp_handler = xmpp.XmppHandler()
            xmpp_handler.prepare(path=self.conf['path'], filename='test.tmp', action='receive_file',
                                 forever=True, xmpp_conf=self.conf['xmpp'])
            await xmpp_handler.update_xmpp_instance()
            xmpp_instance = xmpp_handler.ret_xmpp_instance()
            xmpp_instance.connect()
        elif self.conf['command'] == "watcher":
            await watcher.watch(path=self.conf['path'], events=self.conf['events'], debug=self.conf['debug'],
                                xmpp_conf=self.conf['xmpp'])
        else:
            return


def config_retriever():
    parser = argparse.ArgumentParser(description='Automatic XMPP file sender and directory watcher')
    parser.add_argument("-e", "--events",
                        type=int,
                        default=10000,
                        help='Number of events to watch (create modify) in the directory. '
                             'Once reached, the programs stops.')
    parser.add_argument("-f", "--file",
                        help='Config file containing XMPP parameters',
                        required=False, default='config.ini')
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("-p", "--path",
                        help='The path watched.',
                        required=True)

    parser.add_argument("-c", "--command",
                        help='The executed command: xmpp or watcher',
                        required=True)
    conf = {}
    args = None
    try:
        args = parser.parse_args()
        logging.basicConfig(level=args.loglevel, format='%(levelname)-8s %(message)s')
        debug = False
        if args.loglevel == logging.DEBUG:
            debug = True
        conf = config_parser.read_config(args.file)
    except (NoSectionError, NoOptionError, SystemExit)as e:

        loop = asyncio.get_event_loop()
        loop.stop()
        return
    conf['command'] = args.command
    conf['path'] = args.path
    conf['events'] = args.events
    conf.setdefault('debug', False)
    if debug:
        conf['debug'] = True
    return conf


async def main():
    conf = config_retriever()
    if conf and conf.get('command'):
        errol_instance = ErrolLauncher(conf)
        await errol_instance.launcher()
    else:
        logger.info("No suitable config found.")


def launcher():
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    try:
        loop.run_forever()
    except (asyncio.CancelledError):
        logger.info('Tasks has been canceled')
        for task in asyncio.all_tasks():
            task.cancel()
    except (RuntimeError, KeyboardInterrupt, SystemExit):
        return 1
    finally:
        loop.stop()


if __name__ == '__main__':
    launcher()

