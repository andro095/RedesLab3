from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.asyncio import asyncio
from threading import Thread
from mymenu import menu
import logging
import os
import blessed

#Blessed!
UITerminal = blessed.Terminal()

class xmpclient(ClientXMPP):

    def __init__(self, jid, password, node_name):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("register", self.register)

        ## Chat parameters
        self.node_name = node_name
        self.recipient = ''

        self.messages_pool = []

        self.auto_subscribe = True

        # Menu functions
        functions = {
            ## Message functions
            'send_message': self.send_msg,
            'set_contact': self.set_contact,
            'show_messages': self.show_messages,

            ## Disconnect
            'exit': self.terminate
        }

        ## Instantiate blessed menu in backgounrd
        self.menuInstance = Thread(target = menu, args = (functions,))



    def session_start(self, event):
        '''
        Session start - Starts session and menu instance
        event: dummy variable
        Status: Working
        '''
        self.send_presence()
        self.get_roster()
        self.menuInstance.start()

    async def register(self, iq):
        '''Self Register - Registers user if does not exist
        iq: stanza with register information, ends up being dummy due to stanza generated within function
        Status: Working
        '''
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Account already exists.")
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

    def message(self, msg):
        '''
        Message - Read messages
        msg: message that has been received
        BUG: Kind of works, sometimes takes up to five minutes to receive messages, sometimes crashes.
        '''
        if msg['type'] in ('chat', 'normal'):
            self.messages_pool.append(msg)

    def show_messages(self, dummy):
        for msg in self.messages_pool:
            print(UITerminal.yellow(str(msg['from'])+ ' > ') + UITerminal.white(msg['body']))

        self.messages_pool.clear()


    def send_msg(self, msg):
        '''
        Send message - Send message
        msg: message to be sent (recipient is determined from set contact)
        BUG: Again, sometimes takes up to five minutes, sometimes crashes.
        '''
        if self.recipient != '':
            self.send_message(mto=self.recipient, mbody=msg, msubject='normal message', mfrom=self.boundjid)


    def set_contact(self, recipient):
        '''
        Set contact - Sets recipient for future messages
        recipient: recipient
        Status: Working
        '''
        self.recipient = recipient


    def terminate(self, session):
        '''
        Terminate - Ends session and disconnects
        session: dummy variable
        BUG: Disconnects, but leaves menu thread running, so doesn't close entirely
        '''
        self.disconnect(wait=1.0)
        os._exit(1)
