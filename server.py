import socket
import time

def calculate_ber(sent_data, received_data):
    """Calculate Bit Error Rate (BER)"""
    errors = sum(1 for sent_bit, recv_bit in zip(sent_data, received_data) if sent_bit != recv_bit)
    return errors / len(sent_data) if len(sent_data) > 0 else 0

def server_program():
    server_socket = socket.socket()
    try:
        server_socket.bind(('0.0.0.0', 5000))  # Bind to an available port on the server
        print("Server started and listening on port 5000...")
    except socket.error as e:
        print(f"Error binding to socket: {e}")
        return
    
    server_socket.listen(1)
    print("Waiting for a connection...")

    conn, address = server_socket.accept()
    print(f"Connection from {address} established")
    
    received_packets = 0
    bit_errors = 0
    packet_loss = 0
    expected_sequence_number = 0
    
    start_time = time.time()
    
    try:
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    print("No data received. Closing connection...")
                    break

                if ':' not in data:
                    print(f"Malformed packet: {data}")
                    continue

                received_sequence_number_str, received_data = data.split(":", 1)
                try:
                    received_sequence_number = int(received_sequence_number_str)
                except ValueError:
                    print(f"Invalid sequence number: {received_sequence_number_str}")
                    continue
                
                if received_sequence_number != expected_sequence_number:
                    packet_loss += 1
                    print(f"Packet loss detected: Expected {expected_sequence_number}, got {received_sequence_number}")
                
                received_packets += 1
                expected_sequence_number = received_sequence_number + 1
                
                # Compare received data with expected data (this is simplified for the demo)
                bit_errors += calculate_ber(received_data, received_data)  # Simplified for demo
                
            except socket.error as e:
                print(f"Error receiving data: {e}")
                break
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_bits_sent = received_packets * 64 * 8  # Assuming 64-byte packets
        
        ber = bit_errors / total_bits_sent if total_bits_sent > 0 else 0
        packet_loss_rate = packet_loss / expected_sequence_number if expected_sequence_number > 0 else 0

        print(f"Total Packets Received: {received_packets}")
        print(f"Packet Loss: {packet_loss}")
        print(f"Packet Loss Rate: {packet_loss_rate:.4f}")
        print(f"Bit Errors: {bit_errors}")
        print(f"Bit Error Rate (BER): {ber:.8f}")
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")

        conn.close()
        print("Connection closed.")

if __name__ == '__main__':
    server_program()
