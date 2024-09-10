import socket
import struct
import datetime

class RCON:
    AUTH_FAILURE = -1

    def __init__(self, config):
        self.host = config["host"]
        self.port = int(config["port"])
        self.password = config["password"]
        self.log = config["log"] == "true"
        self.socket = None
        self.request_id = 0
        self.status = 0

    def execute(self, command):
        self.open()
        response = self.command(command)
        self.close()
        return response

    def __connect(self):
        """Establishes a TCP connection to the RCON server."""
        if self.log:
            print(f"Connecting to {self.host}:{self.port}...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)  # Set timeout to 5 seconds

        try:
            self.socket.connect((self.host, self.port))
            self.status = 1
            if self.log:
                print("Connection established.")
        except ConnectionRefusedError:
            raise Exception("Server is not reachable. Connection refused.")
        except socket.error as e:
            raise Exception(f"Socket error: {e}")

    def __login(self):
        """Performs login/authentication with the RCON server using the provided password."""
        if self.status == 0:
            raise Exception("Connection is not established.")

        if self.log:
            print("Authenticating...")

        if self.socket:
            packet = self._create_packet(3, self.password)
            self.socket.send(packet)
            response = self._receive_response()

            if response["request_id"] == self.AUTH_FAILURE:
                if self.log:
                    print("Authentication failed: Incorrect password.")
                return False

            self.status = 2

            if self.log:
                print("Authentication successful.")
            return True
        return False

    def open(self):
        """Opens a connection to the RCON server."""
        self.__connect()

        if not self.__login():
            raise Exception("Authentication failed.")

    def command(self, cmd):
        """Sends a command to the RCON server and processes the response."""

        if self.log:
            print(f"Sending command: {cmd}")

        if self.socket:
            packet = self._create_packet(2, cmd)
            self.socket.send(packet)
            response = self._receive_response()

            if self.log:
                self._handle_response_with_log(cmd, response["body"])

            return response["body"]

    def close(self):
        """Closes the socket connection to the RCON server."""
        if self.socket:
            self.socket.close()
            self.socket = None
            self.request_id = 0

            if self.log:
                print("Connection closed.")

    def _create_packet(self, request_type, body):
        """Creates a packet to be sent to the RCON server."""
        self.request_id += 1

        body_encoded = body.encode("utf-8")
        packet_size = 10 + len(body_encoded)
        packet = struct.pack("<3i", packet_size, self.request_id, request_type) + body_encoded + b"\x00\x00"

        return packet

    def _receive_response(self):
        """Receives and parses the response from the RCON server."""
        try:
            response_data = self.socket.recv(4096)

            if len(response_data) < 12:
                raise Exception("Incomplete response received from the server.")

            response_size, request_id, response_type = struct.unpack("<3i", response_data[:12])
            body = response_data[12:response_size + 4].decode("utf-8").strip()

            return {"size": response_size, "request_id": request_id, "type": response_type, "body": body}
        except socket.timeout:
            raise Exception("Socket timeout occurred while waiting for the response.")
        except Exception as e:
            raise Exception(f"Error receiving response: {e}")

    def _handle_response_with_log(self, command, response_body):
        """Handles the response from the server and logs it with timestamp and command information."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} - Command: {command}\n\nResponse:\n\n{response_body}\n")
