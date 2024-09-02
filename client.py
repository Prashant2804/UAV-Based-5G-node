import socket
import time
import random
import string

def generate_packet(sequence_number, packet_size=64):
    """Generates a packet with a sequence number and random data"""
    sequence_str = f"{sequence_number:08d}"  # Fixed-length sequence number
    random_data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=packet_size - len(sequence_str) - 1))
    packet = f"{sequence_str}:{random_data}"
    return packet

def client_program():
    client_socket = socket.socket()
    server_ip = 'SERVER_IP_ADDRESS'  # Replace with the IP address of the server
    port = 5000
    packet_size = 64  # Set packet size (in bytes)
    packet_count = 1000  # Set number of packets to send
    delay = 0.01  # Delay between packets (in seconds)
    
    try:
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
    except socket.error as e:
        print(f"Error connecting to server: {e}")
        return
    
    for sequence_number in range(packet_count):
        packet = generate_packet(sequence_number, packet_size)
        try:
            client_socket.send(packet.encode())
            print(f"Sent: {packet}")
        except socket.error as e:
            print(f"Error sending packet {sequence_number}: {e}")
            break
        time.sleep(delay)

    client_socket.close()
    print("Connection closed.")

if __name__ == '__main__':
    client_program()
