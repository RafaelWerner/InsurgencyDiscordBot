import asyncio
import struct
import datetime

class RCON:
    AUTH_FAILURE = -1

    def __init__(self, host, port, password, log=False):
        self.host = host
        self.port = int(port)
        self.password = password
        self.log = log
        self.reader = None
        self.writer = None
        self.request_id = 0
        self.status = 0

    async def execute(self, command):
        await self.open()
        response = await self.command(command)
        await self.close()
        return response

    async def __connect(self):
        """Establishes a TCP connection to the RCON server asynchronously."""
        if self.log:
            print(f"Connecting to {self.host}:{self.port}...")

        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.status = 1
            if self.log:
                print("Connection established.")
        except ConnectionRefusedError:
            raise Exception("Server is not reachable. Connection refused.")
        except Exception as e:
            raise Exception(f"Connection error: {e}")

    async def __login(self):
        """Performs login/authentication with the RCON server using the provided password asynchronously."""
        if self.status == 0:
            raise Exception("Connection is not established.")

        if self.log:
            print("Authenticating...")

        if self.writer:
            packet = self._create_packet(3, self.password)
            self.writer.write(packet)
            await self.writer.drain()

            response = await self._receive_response()

            if response["request_id"] == self.AUTH_FAILURE:
                if self.log:
                    print("Authentication failed: Incorrect password.")
                return False

            self.status = 2

            if self.log:
                print("Authentication successful.")
            return True
        return False

    async def open(self):
        """Opens a connection to the RCON server asynchronously."""
        await self.__connect()

        if not await self.__login():
            raise Exception("Authentication failed.")

    async def command(self, cmd):
        """Sends a command to the RCON server and processes the response asynchronously."""
        if self.log:
            print(f"Sending command: {cmd}")

        if self.writer:
            packet = self._create_packet(2, cmd)
            self.writer.write(packet)
            await self.writer.drain()

            response = await self._receive_response()

            if self.log:
                self._handle_response_with_log(cmd, response["body"])

            return response["body"]

    async def close(self):
        """Closes the socket connection to the RCON server asynchronously."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.writer = None
            self.reader = None
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

    async def _receive_response(self):
        """Receives and parses the response from the RCON server asynchronously."""
        try:
            response_data = await self.reader.read(4096)

            if len(response_data) < 12:
                raise Exception("Incomplete response received from the server.")

            response_size, request_id, response_type = struct.unpack("<3i", response_data[:12])
            body = response_data[12:response_size + 4].decode("utf-8").strip()

            return {"size": response_size, "request_id": request_id, "type": response_type, "body": body}
        except asyncio.TimeoutError:
            raise Exception("Socket timeout occurred while waiting for the response.")
        except Exception as e:
            raise Exception(f"Error receiving response: {e}")

    def _handle_response_with_log(self, command, response_body):
        """Handles the response from the server and logs it with timestamp and command information."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} - Command: {command}\n\nResponse:\n\n{response_body}\n")
