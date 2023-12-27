import socket
import json
import threading

PORT = 7000
ADDR = ("0.0.0.0", PORT)
ALL_CLIENT = "255.255.255.255"
BUFFER_SIZE = 2048


class VectorClock:
    def __init__(self, client_name):
        self.name = client_name
        self.vector = {}

        # set up receiver configuration
        self.socket_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_receiver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.socket_receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # if there is error saying "Port is already in use" while running, comment above line and uncomment line 21
        self.socket_receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_receiver.bind(ADDR)

        # set up sender configuration
        self.socket_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.vector[self.name] = 0
        self.socket_sender.sendto((f"NEW_CONNECTION=={self.name}").encode(), (ALL_CLIENT, PORT))

    def broadcast_message(self):
        while True:
            client_message = ""
            while True:
                client_message = input("\nPlease enter your message: ")
                if not client_message:
                    print("Client message cannot be empty!")
                else:
                    break

            print(f"\nVector before sending message: {json.dumps(self.vector)}")

            # update own vector and send message
            self.vector[self.name] += 1
            vector_str = json.dumps(self.vector)
            self.socket_sender.sendto((f"{self.name}##{client_message}@@{vector_str}").encode(), (ALL_CLIENT, PORT))

            print(f"Message sent: {client_message}")
            print(f"\nVector after sending message: {json.dumps(self.vector)}")

    def receive_message(self):
        while True:
            data = self.socket_receiver.recvfrom(BUFFER_SIZE)
            message = data[0].decode()

            # if message is of type new connection
            if "NEW_CONNECTION==" in message:
                new_client_name = message.split("==")[1]
                if new_client_name != self.name:
                    self.vector[new_client_name] = 0
                    self.socket_sender.sendto((f"EXISTING_CONNECTION=={self.name}").encode(), (ALL_CLIENT, PORT))

            # if message is of type existing connection
            elif "EXISTING_CONNECTION==" in message:
                existing_client_name = message.split("==")[1]
                if existing_client_name != self.name:
                    if existing_client_name not in self.vector:
                        self.vector[existing_client_name] = 0

            # for all other messages
            else:
                sender_name, sender_message_vector = message.split("##")

                if sender_name != self.name:
                    sender_message, vector_str_received = sender_message_vector.split("@@")
                    vector_received = json.loads(vector_str_received)

                    print(f"\nVector before receiving message: {json.dumps(self.vector)}")
                    print(f"Message from {sender_name}: {sender_message}")

                    # compare received vector with own vector and update own vector
                    for key in vector_received:
                        if vector_received[key] > self.vector[key]:
                            self.vector[key] = vector_received[key]

                    print(f"\nVector after receiving message: {json.dumps(self.vector)}")


def main():
    client_name = ""

    while True:
        client_name = input("\nPlease enter the client name: ")
        if not client_name:
            print("Client name cannot be empty!")
        else:
            break

    vector_clock = VectorClock(client_name)

    # create a thread for broadcasting messages
    send_message_thread = threading.Thread(target=vector_clock.broadcast_message)
    send_message_thread.start()

    # create a thread for receiving messages
    receive_message_thread = threading.Thread(target=vector_clock.receive_message)
    receive_message_thread.start()


if __name__ == "__main__":
    main()
