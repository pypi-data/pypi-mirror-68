#!/usr/bin/env python
# Copyright (c) 2018 odoo_cep project
# This code is distributed under the GPLv3 License

import os
import asyncio
import logging
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout, XMPPError
from slixmpp.xmlstream import ET
from datetime import datetime

# TODO test if the pubsub node can be accessed with disco

logging.getLogger("asyncio").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

REMOTE_FILENAME = 'remote.file'


class XmppManager(slixmpp.ClientXMPP):
    """
    A basic example of creating and using a SOCKS5 bytestream.
    """

    def __init__(self, jid=None, password=None, filename=None, server=None,
                 action_str=None, full_filename=None, node=None, path=None,
                 nick='nick', presence_file='/tmp/test.txt', room=None, pubsub_enable=False, muc_enable=False,
                 errol_receiver=None, nick_reveiver=None, nick_sender=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        # loop = asyncio.get_event_loop()
        # self.init_future = loop.run_in_executor(None, self._reading_init)
        logger.info("XMPP Initialization")
        self.remote_filename = 'unknown_filename'
        self.full_filename = full_filename
        self.filename = filename
        self.tmp_filename = filename # copy temporary filename
        self.node = node
        self.pubsub_enable = pubsub_enable
        self.muc_enable = muc_enable
        self.pubsub_server = server
        self.action_str = action_str
        self.file_obj = None
        self.path = path
        self.presence_file = presence_file
        # at first, the receiver is marked offline
        self.write_presence_file(0)
        self.received = set()
        self.presences_received = asyncio.Event()
        if action_str == 'receive_file':
            self.file_obj = open(self.full_filename, 'wb')
        self.nick = nick
        self.nick_receiver = nick_reveiver
        self.nick_sender = nick_sender
        self.errol_receiver = errol_receiver
        self.room = room
        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use.
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        # self.add_event_handler("muc::%s::got_online" % self.room,
        #                       self.muc_online)
        self.add_event_handler("groupchat_message", self.muc_message)

        self.add_event_handler("socks5_connected", self.stream_opened)
        self.add_event_handler("socks5_data", self.stream_data)
        self.add_event_handler("socks5_closed", self.stream_closed)

        self.add_event_handler('pubsub_publish', self._publish)
        self.add_event_handler('pubsub_purge', self._purge)
        self.add_event_handler("changed_status", self.wait_for_presences)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pubsub_template_file = os.path.join(dir_path, './data/template.xml')
        with open(pubsub_template_file, 'r') as xmlfile:
            txt_xml = xmlfile.read()
        self.xml_publish = txt_xml

    async def start(self, event):
        self.send_presence()
        self.get_roster()
        self.plugin['xep_0045'].join_muc(self.room,
                                         self.nick,
                                         # If a room password is needed, use:
                                         # password=the_room_password,
                                         wait=True)

        logger.info("START")
        if self.action_str == 'send_file':
            await self.send_file()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            logger.debug("Received message : {}".format(msg['body']))
            if self.errol_receiver == msg['to'].full:
                self.get_filename_from_message(msg['body'])

    def send_msg_receiver(self, msg):
        self.send_message(mto=self.errol_receiver,
                          mbody=msg,
                          mtype='chat')  # normal or chat

    def send_muc(self, msg):
        if self.muc_enable:
            self.send_message(mto=self.room,
                              mbody=msg,
                              mtype='groupchat')
            return True
        return False

    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
        if self.nick not in presence['muc']['nick']:
            # mto=presence['from'].bare,
            self.send_message(mto=self.room,
                              mbody="Bonjour, %s %s" % (presence['muc']['role'],
                                                        presence['muc']['nick']),
                              mtype='groupchat')

    def muc_message(self, msg):
        """
            Process incoming message stanzas from any chat room. Be aware
            that if you also have any handlers for the 'message' event,
            message stanzas may be processed by both handlers, so check
            the 'type' attribute when using a 'message' event handler.
            Whenever the bot's nickname is mentioned, respond to
            the message.
            IMPORTANT: Always check that a message is not from yourself,
                       otherwise you will create an infinite loop responding
                       to your own messages.
            This handler will reply to messages that mention
            the bot's nickname.
            Arguments:
                msg -- The received message stanza. See the documentation
                       for stanza objects and the Message stanza to see
                       how it may be used.
            """
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="I heard that, %s." % msg['mucnick'],
                              mtype='groupchat')

        if self.nick_sender in msg['mucnick']:
            self.get_filename_from_message(msg['body'])

    def get_filename_from_message(self, message):
        if 'Send file: ' in message:
            msg_split = message.split(': ')
            filename = msg_split[1]
            logger.info("Got a new Remote filename: %s" % filename)
            self.remote_filename = filename


    # FILE STREAM s5b #
    async def send_file(self, ):
        if os.path.isdir(self.full_filename):
            logger.error("Filename is a directory")
            return
        logger.info("Send file %s" % self.full_filename)
        self.file_obj = open(self.full_filename, 'rb')
        try:
            # Open the S5B stream in which to write to.
            proxy = await self['xep_0065'].handshake(self.errol_receiver)
            # Send the entire file.
            while True:
                data = self.file_obj.read(100)
                if not data:
                    break
                await proxy.write(data)
            # And finally close the stream.
            proxy.transport.write_eof()
        except (IqError, IqTimeout) as ex:
            logger.error('File transfer failed')
            logger.error(ex)
            # FIXME: if the service is unavailable, send a message to the muc

        finally:
            logger.info("File sent %s " % self.filename)
            self.file_obj.close()
            # self.disconnect()
            msg_ = "Send file: {}".format(self.filename)
            if not self.send_muc(msg_):
                self.send_msg_receiver(msg_)
            await self.publish('sent')

    # Receive file
    def stream_opened(self, sid):
        logger.info('Stream opened. %s', sid)

    def stream_data(self, data):
        self.file_obj.write(data)

    async def stream_closed(self, exception):
        logger.info('Stream closed. %s', exception)
        self.file_obj.close()
        if not self.tmp_filename in self.filename:
            # avoid printing about tmp file
            self.send_muc("New file: {}".format(self.filename))
        if self.action_str == 'receive_file':
            path = os.path.dirname(self.full_filename)
            await asyncio.sleep(5)
            full_remote_filename = os.path.join(path, self.remote_filename)
            self.remote_filename = 'unknown_filename'
            os.rename(self.full_filename, full_remote_filename)
            self.file_obj = open(self.full_filename, 'wb')
            await self.publish('received')

        # Once we have receive the file, we can disconnect
        if self.action_str == 'send_file':
            self.disconnect()

    # PUBSUB EVENTS
    def _publish(self, msg):
        """Handle receiving a publish item event."""
        log_msg = 'Published item %s to %s:' % (
            msg['pubsub_event']['items']['item']['id'],
            msg['pubsub_event']['items']['node'])
        logger.info(log_msg)
        data = msg['pubsub_event']['items']['item']['payload']
        if data is not None:
            log_msg = "data in publish = {}".format(data)
            logger.info(log_msg)
        else:
            logger.info('No item content')

    def _purge(self, msg):
        """Handle receiving a node purge event."""
        print('Purged all items from %s' % (
            msg['pubsub_event']['purge']['node']))

    async def publish(self, action_str):
        if self.pubsub_enable:
            string_entry = self.xml_publish
            datetime_str = str(datetime.now())
            if action_str == 'sent':
                filename = self.filename
            else:
                filename = self.remote_filename
            string_entry = string_entry.replace('DATE', datetime_str).replace('*FILE*', filename).replace('ACTION',
                                                                                                          action_str)
            string_entry = string_entry.replace('AUTHOR', self.jid)
            payload = ET.fromstring(string_entry)
            try:
                result = await self['xep_0060'].publish(self.pubsub_server, self.node, payload=payload)
                logger.info('Published at item id: %s', result['pubsub']['publish']['item']['id'])
            except XMPPError as error:
                logger.error('PUBLISH ERROR: Could not publish to %s: %s', self.node, error.format())

    def wait_for_presences(self, presence):
        """
        track presence changes
        Inspired by https://github.com/poezio/slixmpp/blob/master/examples/roster_browser.py
        Thanks to Link Mauve
        """

        self.received.add(presence['from'])
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

        if self.errol_receiver == str(presence['from']):
            if 'unavailable' == str(presence.values['type']):
                self.write_presence_file(0)
            else:
                self.write_presence_file(1)

    def write_presence_file(self, msg):
        try:
            with open(self.presence_file, 'w') as pf:
                pf.write('{}\n'.format(msg))
        except FileNotFoundError:
            self.create_presence_file(self.presence_file)

    def create_presence_file(self, presence_file):
        # the default presence is 0 (not connected)
        logger.info(
            'Presence file {} donot exist. We create it with a disconnected value (0)'.format(self.presence_file))
        with open(presence_file, 'w') as pf:
            pf.write('0\n')


class XmppHandler:
    def __init__(self):
        self.tmp_filename = None
        self.jid = None
        self.password = None
        self.node = None
        self.server = None
        self.nick = None
        self.xmpp_instance = None
        self.forever = None
        self.debug = None
        self.path = None
        self.action = None
        self.filename = None
        self.full_filename = None
        self.presence_file = None
        self.room = None
        self.pubsub_enable = None
        self.errol_receiver = None
        self.muc_enable = None
        self.nick_sender = None
        self.nick_receiver = None

    def prepare(self, path=None, filename=None, action=None, forever=False, debug=False, xmpp_conf=None):
        logger.info("Start XMPP")
        self.path = path
        self.action = action
        self.forever = forever
        self.tmp_filename = '.tmp.file'
        self.jid = xmpp_conf['jid']
        self.password = xmpp_conf['password']
        self.errol_receiver = xmpp_conf['receiver'] # jid of the receiver
        self.node = xmpp_conf['node']
        self.server = xmpp_conf['pubsub_server']
        self.debug = debug
        self.presence_file = xmpp_conf['presence_file']
        self.room = xmpp_conf['room']
        self.pubsub_enable = xmpp_conf['pubsub_enable']
        self.muc_enable = xmpp_conf['muc_enable']
        self.nick_sender = xmpp_conf['nick_sender']
        self.nick_receiver = xmpp_conf['nick_receiver']
        if self.jid is None or self.password is None or self.errol_receiver is None:
            logger.error("Error in config file")
            return 1

        if self.action == 'send_file':
            self.full_filename = os.path.join(path, filename)
            self.jid = self.jid + xmpp_conf['ressource_sender']
            self.nick = xmpp_conf['nick_sender']
        else:
            self.filename = os.path.join(self.path, self.tmp_filename)
            self.full_filename = self.filename
            self.jid = self.jid + xmpp_conf['ressource_receiver']
            self.nick = xmpp_conf['nick_receiver']

    def xmp_connect(self, ):
        logger.debug("Connect")
        self.xmpp_instance.connect()
        logger.debug('Process')
        self.xmpp_instance.process(forever=self.forever)

    def ret_xmpp_instance(self):
        return self.xmpp_instance

    def update_filename(self, filename):
        self.filename = os.path.basename(filename)
        self.full_filename = filename

    async def update_xmpp_instance(self):
        self.xmpp_instance = XmppManager(jid=self.jid, password=self.password,
                                         filename=self.filename,
                                         server=self.server, action_str=self.action,
                                         full_filename=self.full_filename, node=self.node, nick=self.nick,
                                         path=self.path, presence_file=self.presence_file, room=self.room,
                                         pubsub_enable=self.pubsub_enable, muc_enable=self.muc_enable,
                                         errol_receiver=self.errol_receiver, nick_reveiver=self.nick_receiver,
                                         nick_sender=self.nick_sender)

        self.xmpp_instance.register_plugin('xep_0030')  # Service Discovery
        self.xmpp_instance.register_plugin('xep_0065', {'auto_accept': True})  # SOCKS5 Bytestreams
        self.xmpp_instance.register_plugin('xep_0030')
        self.xmpp_instance.register_plugin('xep_0045')
        self.xmpp_instance.register_plugin('xep_0059')
        self.xmpp_instance.register_plugin('xep_0060')
        self.xmpp_instance.register_plugin('xep_0198')
        self.xmpp_instance.register_plugin('xep_0199')


if __name__ == '__main__':
    PATH = '/home/arnaud/files/programmation/python/django/cep/odoo_cep/static/withdraw'
    file_name = 'test.txt'
    action = 'send_file'
