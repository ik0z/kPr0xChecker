import threading
import socket
import colorama

from colorama import Fore, Style

# Initialize colorama for colored output
colorama.init()

logo = '''
 __  _   ____  _____ 
|  |/ ] /    ||     |
|  ' / |  o  ||__/  |
|    \ |     ||   __|
|     \|  _  ||  /  |
|  .  ||  |  ||     |
|__|\_||__|__||_____|   ENG. Khaled
                     
'''
print(logo)
# Define the filename of the input file
input_filename = 'proxylist.txt'

# Define the filename of the output file
output_filename = 'goodlist-socks.txt'

# Define a function to check the validity of a SOCKS proxy
def check_proxy(proxy):
    try:
        # Split the proxy string into host and port
        host, port = proxy.split(':')

        # Create a socket object for the proxy
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        # Connect to the proxy and send a SOCKS5 request
        sock.connect((host, int(port)))
        sock.sendall(b'\x05\x01\x00')

        # Receive the SOCKS5 response
        response = sock.recv(2)

        # Check if the SOCKS5 response indicates success
        if response == b'\x05\x00':
            print(Fore.GREEN + 'Valid proxy: ' + proxy)
            with open(output_filename, 'a') as output_file:
                output_file.write(proxy + '\n')

        # Close the socket connection
        sock.close()
    except Exception as e:
        pass

# Read the list of proxies from the input file
try : 
    with open(input_filename, 'r') as input_file:
        proxies = input_file.read().splitlines()
except : 
    print("can't find proxylist.txt file .")

# Create a thread for each proxy to check their validity
try : 
    threads = []
    for proxy in proxies:
        thread = threading.Thread(target=check_proxy, args=[proxy])
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
except : 
    print("issues found :(")
# Reset colorama to default settings
Style.RESET_ALL
press = input("\n Press any key to close :)")