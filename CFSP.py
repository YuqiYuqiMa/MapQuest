
###CFSP

from collections import namedtuple
import connectfour
import common_ui
import socket
CONNECTFOUR_HOST = 'sgagomas-office.calit2.uci.edu'
CONNECTFOUR_PORT = 4444

ConnectfourConnection = namedtuple('ConnectfourConnection', ['socket', 'input', 'output'])

SHOW_DEBUG_TRACE = False
HELLO = 0
NO_USER = 5


class ConnectfourProtocolError(Exception):
    pass

def ask_host() -> str:
    '''
    ask for the host name
    '''
    while True:
        host = input('Host: ').strip()

        if host == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host



def ask_port() -> int:
    '''
    ask for the port number
    between 0 and 65535
    '''
    while True:
        try:
            port = int(input('Port: ').strip())

            if port < 0 or port > 65535:
                print('Ports must be an integer between 0 and 65535')
            else:
                return port

        except ValueError:
            print('Ports must be an integer between 0 and 65535')
    

def connect(host: str, port: int) -> ConnectfourConnection:
    '''
    connects to a Connectfour server running on the given host
    and the given port
    returns a ConnectfourConnection if successful,
    or print: connection failure
    '''
    try:
        connectfour_socket = socket.socket()
        connectfour_socket.connect((host, port))
        connectfour_input = connectfour_socket.makefile('r')
        connectfour_output = connectfour_socket.makefile('w')
    except ConnectfourProtocolError:
        print('Connection Failure')

    return ConnectfourConnection(socket = connectfour_socket, input = connectfour_input, output = connectfour_output)


def hello(connection: ConnectfourConnection, username: str) -> HELLO or NO_USER:
    '''
    Log the given user into the ConnectfourConnection server
    and complete first conversation between user and server:
    
    I32CFSP_HELLO username     WELCOME username
    '''
    _write_line(connection, str('I32CFSP_HELLO ' + username))

    response = read_line(connection)

    if response == 'WELCOME ' + username:
        return HELLO
    elif response.startswith('NO_USER '):
        return NO_USER
    
def greeting(connection: ConnectfourConnection, username) -> None:
    '''
    after connecting to the server,
    this function completes the rest of the conversation between
    uer and server before the actual game starts:

    I32CFSP_HELLO username     WELCOME username
    AI_GAME                    READY
    '''
    hello(connection, username)
    _write_line(connection, 'AI_GAME')
    response = read_line(connection)

def close(connection: ConnectfourConnection) -> None:
    '''
    closes the ConnectfourConnection to the server
    '''
    connection.input.close()
    connection.output.close()
    connection.socket.close()

def read_line(connection: ConnectfourConnection) -> str:
    '''
    Reads a line sent from the server and returns it without
    a newline on the end of it
    '''
    line = connection.input.readline()[:-1]
    # The [:-1] uses the slice notation to remove the last character
    # from the string.

    if SHOW_DEBUG_TRACE:
        print('RCVD: ' + line)

    return line
    
def _write_line(connection: ConnectfourConnection, line: str) -> None:
    '''
    Writes a line of text to the server, including the appropriate
    newline sequence, and ensures that it is sent immediately.
    '''
    connection.output.write(line + '\r\n')
    connection.output.flush()

    if SHOW_DEBUG_TRACE:
        print(line)

def user_move(connection: ConnectfourConnection, command: str, col_num: int) -> bool:
    '''
    sends the user's move to the server
    and check if the server's response is 'OKAY'
    '''
    line1 = command + str(col_num+1)
    # transer user's move to the form DROP 1 or POP 3
    _write_line(connection, line1)
    # sends the correct form of user move to server
    r1 = read_line(connection)
    if r1.startswith('OKAY'):#check if server's response is 'OKAY'
        return True
    if r1.startswith('INVALID'):
        r1 = read_line(connection) # read the ready
        return False
    

def server_move(connection: ConnectfourConnection, game_state: connectfour.ConnectFourGameState) -> connectfour.ConnectFourGameState:
    '''
    receives server's move and prints it on the game table
    returns a new game_state
    '''
    r2 = read_line(connection)
    r21 = r2.split()  #split the spaces in server's response

    if r21[0] == 'DROP':
        common_ui.show_player_turn(game_state)
        # prints out player's turn for server
        # YELLOW
        col_num = int(r21[1]) - 1
        game_state = common_ui.check_error_drop(game_state, col_num)
        #prints put the game table after the server makes its move
        common_ui.show_player_turn(game_state)
        # prints out the player turn after the server's move
        # RED
    elif r2[0] == 'POP':
        common_ui.show_player_turn(game_state)
        # prints out player's turn for server
        # YELLOW
        col_num = int(r21[1]) - 1
        common_ui.check_error_drop(game_state, col_num)
        #prints put the game table after the server makes its move
        common_ui.show_player_turn(game_state)
        # prints out the player turn after the server's move
        # RED
    return game_state
