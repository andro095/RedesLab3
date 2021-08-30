import blessed
import getpass

CLI_Terminal = blessed.Terminal()
title_chat = '''
    ___            _                        ___    _                _     
   | __|  __ _    | |__    ___      o O O  / __|  | |_     __ _    | |_   
   | _|  / _` |   | / /   / -_)    o      | (__   | ' \   / _` |   |  _|  
  _|_|_  \__,_|   |_\_\   \___|   TS__[O]  \___|  |_||_|  \__,_|   _\__|  
_| """ |_|"""""|_|"""""|_|"""""| {======|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''

mmenu = '''
    Mensajería:
    Escriba / para enviar un mensaje al contacto previamente fijado
    /set_contact <contact>: fijar el contacto al cual enviar el mensaje 
    /show_messages: Mostrar los mensajes recibidos
    
    Salir:
    /exit: Salir del programa

'''
OPTIONS_SHOWN = True

# CLI_Terminal.center()

def showTitleChat():
    print(CLI_Terminal.blink(CLI_Terminal.sienna1(title_chat)))

def showMenu(args=''):

    if OPTIONS_SHOWN:
        useterminal = CLI_Terminal.location(0, int(CLI_Terminal.height/2))
    else:
        useterminal = CLI_Terminal.location()
    with useterminal:
        print(CLI_Terminal.center(CLI_Terminal.blink('Commands')))
        print(CLI_Terminal.center(mmenu))

def menu(functions):
    ## Start menu
    showMenu()
    OPTIONS_SHOWN = False
    while True:
        # Expect input
        message = input(CLI_Terminal.move(CLI_Terminal.height - 1, 0) + '>')
        # Handle commands
        if message.startswith('/'):
            command = message.strip().split()[0][1:]
            if command in functions:
                arg = message[2 + len(command):]
                print(arg)
                functions[command](arg)
            else:
                print(CLI_Terminal.red('Unknown command.'))
        else:
            functions['send_message'](message)