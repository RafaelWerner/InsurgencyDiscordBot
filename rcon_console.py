
import configparser
import datetime
import socket
import struct

class RCONClient:
    AUTH_FAILURE = -1

    def __init__(self, host, port, password, log):
        self.host = host
        self.port = int(port)
        self.password = password
        self.log = log
        self.socket = None
        self.request_id = 0

    def execute(self, command):
        self._connect()
        self._login()
        response = self._command(command)
        self._close()
        return response

    def _connect(self):
        """Establishes a TCP connection to the RCON server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)  # Set timeout to 5 seconds
        try:
            self.socket.connect((self.host, self.port))
            if self.log:
                print("Connection established.")
        except ConnectionRefusedError:
            raise Exception("Server is not reachable. Connection refused.")
        except socket.error as e:
            raise Exception(f"Socket error: {e}")

    def _login(self):
        """Performs login/authentication with the RCON server using the provided password."""
        if self.socket:
            packet = self._create_packet(3, self.password)
            self.socket.send(packet)
            response = self._receive_response()
            if response['request_id'] == self.AUTH_FAILURE:
                if self.log:
                    print("Authentication failed: Incorrect password.")
                return False
            if self.log:
                print("Authentication successful.")
            return True
        return False

    def _command(self, cmd):
        """Sends a command to the RCON server and processes the response."""
        if self.socket:
            packet = self._create_packet(2, cmd)
            self.socket.send(packet)
            response = self._receive_response()

            if self.log:
                self._handle_response_with_log(cmd, response['body'])

            return response['body']

    def _close(self):
        """Closes the socket connection to the RCON server."""
        if self.socket:
            self.socket.close()
            if self.log:
                print("Connection closed.")

    def _create_packet(self, request_type, body):
        """Creates a packet to be sent to the RCON server."""
        self.request_id += 1
        body_encoded = body.encode('utf-8')
        packet_size = 10 + len(body_encoded)
        packet = struct.pack('<3i', packet_size, self.request_id, request_type) + body_encoded + b'\x00\x00'
        return packet

    def _receive_response(self):
        """Receives and parses the response from the RCON server."""
        try:
            response_data = self.socket.recv(4096)
            if len(response_data) < 12:
                raise Exception("Incomplete response received from the server.")

            response_size, request_id, response_type = struct.unpack('<3i', response_data[:12])
            body = response_data[12:response_size + 4].decode('utf-8').strip()
            return {'size': response_size, 'request_id': request_id, 'type': response_type, 'body': body}
        except socket.timeout:
            raise Exception("Socket timeout occurred while waiting for the response.")
        except Exception as e:
            raise Exception(f"Error receiving response: {e}")

    def _handle_response_with_log(self, command, response_body):
        """Handles the response from the server and logs it with timestamp and command information."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.log:
            print(f"{current_time} - Command: {command}\nResponse: {response_body}")


CONFIGS = configparser.ConfigParser()
CONFIGS.read("config.ini")

RCON = RCONClient(CONFIGS['rcon']['host'], CONFIGS['rcon']['port'], CONFIGS['rcon']['password'], True)

while True:
    entrada = input("> ")

    if entrada.lower() == 'exit' or entrada.lower() == 'exit()':
        print("Exiting...")
        break

    if entrada.strip() == '':
        continue

    try:
        RCON.execute(entrada)
    except Exception as e:
        print(f"Erro ao executar o comando: {e}")
