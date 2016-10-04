import json
import socket


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def warn(txt):
    print (
        bcolors.WARNING +
        txt +
        bcolors.ENDC)


class StatusError(Exception):
    pass


class UDPConnection(object):
    """
    This class establishes an UDP connection to the provided address.
    This connection allows sending and receiving messages to the remote host.

    @params:
    - TARGET_IP: string, IP address or hostname of the target computer
    - TARGET_PORT: integer, port number where the messages are sent
        default 5005
    - UDP_PORT: integer, port number where the messages are received
        default 5005

    Initialization:
    This machine can be set to remote initialized state by not provding
    the TARGET_IP address argument. When the machine receives a message
    'initialize' the sender address is read and set as the target IP.
    This transaction is confirmed by automatic message 'initialization
    complete'.
    """
    initialized = False

    def __init__(
            self, TARGET_IP=None, UDP_IP=None,
            TARGET_PORT=5005, UDP_PORT=5005):
        super(UDPConnection, self).__init__()
        self.TARGET_IP = TARGET_IP
        self.TARGET_PORT = TARGET_PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if UDP_IP is None:
            self.sock.bind((socket.gethostbyname(socket.gethostname()), 5005))
        else:
            self.sock.bind((UDP_IP, 5005))
        self.target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.TARGET_IP is not None:
            self.initialized = True

    def query_message(self):
        '''
        Waits until the next message, sends a confirmation and returns the
        received unJSONed message. In case it is an 'initialize' message,
        the sender address is saved to TARGET_IP.
        '''
        msg, addr = self.sock.recvfrom(1024)
        msg = json.loads(msg)
        if msg['status'] is None:
            print 'Got message: %s from address: %s' % (msg, addr)
            if msg['message'] == 'initialize' and self.TARGET_IP is None:
                self.TARGET_IP = addr[0]
                self.initialized = True
                self.send_message('initialization complete', True)
                print 'Remote initialization done'
            else:
                self.send_message('confirmed', True)
        elif msg['status'] is False:
            warn(msg['message'])
        elif msg['status'] is True:
            print 'Message confirmed'
        else:
            raise StatusError('No status or incorrect status received')
        return msg

    def send_message(self, msg, ok=None):
        '''
        Sends the given message to the TARGET_IP address in JSON format:
            {'message':msg, 'status': ok}

        '''
        if self.TARGET_IP is not None and self.TARGET_PORT is not None:
            message = {
                'message': msg,
                'status': ok
            }
            self.target.sendto(
                json.dumps(message),
                (self.TARGET_IP, self.TARGET_PORT))
            if ok is None:
                try:
                    self.sock.settimeout(10)
                    response = self.query_message()['status']
                    return response
                except socket.timeout:
                    return False
                finally:
                    self.sock.settimeout(None)
        else:
            warn('Message not sent. No target address specified.')

    def shutdown(self):
        '''
        This function should be called every time the connection is closed.
        '''
        try:
            self.sock.shutdown(socket.SHUT_WR)
        except:
            pass
        try:
            self.target.shutdown(socket.SHUT_WR)
        except:
            pass
        self.sock.close()
        self.target.close()
