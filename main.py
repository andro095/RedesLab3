import mymenu
from client import UITerminal, xmpclient
import blessed
import logging
from getpass import getpass
UITerminal = blessed.Terminal()

if __name__ == '__main__':
    with UITerminal.fullscreen():
        mymenu.showTitleChat()
        JID = input(UITerminal.peachpuff('Su JID: '))
        password = getpass(mymenu.CLI_Terminal.peachpuff('Su contraseña: '))
        node_name = input(mymenu.CLI_Terminal.peachpuff('Apodo del usuario: '))

        xmpp = xmpclient(JID, password, node_name)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0004') # Data forms
        xmpp.register_plugin('xep_0060') # PubSub
        xmpp.register_plugin('xep_0047') # In-band Bytestreams
        xmpp.register_plugin('xep_0066') # Out-of-band Data
        xmpp.register_plugin('xep_0199') # Ping
        xmpp.register_plugin('xep_0045')
        xmpp.register_plugin('xep_0065', {
            'auto_accept': True
        }) # SOCKS5 Bytestreams
        xmpp.register_plugin('xep_0077') # In-band Registration
        xmpp['xep_0077'].force_registration = True

        # Setup logging.
        logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s %(message)s')

        xmpp.connect(address=("localhost", 5222))
        xmpp.process()
