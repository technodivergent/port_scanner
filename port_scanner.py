"""
Purpose: Multi-threaded port scanner
Author: Kassidy Hall (technodivergent)
Date: April 2022
"""
import socket
import argparse
import ipaddress
import threading
from queue import Queue
import time

# create a task queue
q = Queue()

# create mutex
THREAD_LOCK = threading.Lock()

def port_scan(host: str, port: int) -> None:
    """ Scan the provided host:port """

    # attempt to connect to host:port
    # if port not open, socket error exception will occur
    try:
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.connect((host, port))

        # prevent other threads from accessing port variable
        with THREAD_LOCK:
            print('Port %d is open' % port)

        # disconnect from socket
        con.close()
    except socket.error:
        pass

def scanner() -> None:
    """ Execute this thread's task """
    while True:
        # retrieve target from the queue
        target = q.get()

        # target is stored as list containing two columns, host and port
        host = target[0]
        port = target[1]

        # run the scan on this socket
        port_scan(host, port)

        # inform the queue that this queued task has been processed
        q.task_done()

def valid_ip_addr(target: str) -> str:
    """ Validate target to scan is a valid private IP address """
    if not ipaddress.ip_address(target).is_private:
        raise argparse.ArgumentTypeError("Target is limited to private IP address space (/24)")
    return target

def start_threads(num_threads:int ) -> None:
    """ Creates threads for executing scans in parallel """

    for thread in range(num_threads):
        # target refers to the algorithm followed by each individual thread
        thread = threading.Thread(name='scanner_'+ str(thread), target=scanner)
        thread.daemon = True
        thread.start()

def main() -> None:
    """ Parent thread that spawns children processes to scan multiple ports """
    argp = argparse.ArgumentParser(description='Perform a basic port scan')

    # add available arguments
    argp.add_argument(
        '-s', '--start',
        required=True,
        type=int,
        default=None,
        help='Specify the start of the port range')
    argp.add_argument(
        '-e', '--end',
        type=int,
        default=None,
        help='Specify the end of the port range')
    argp.add_argument(
        '-t', '--threads',
        type=int,
        default=24,
        help='Specify the number of threads to spawn')
    argp.add_argument(
        'HOST',
        type=valid_ip_addr,
        default=None,
        help='Specify the host to scan')
    args = argp.parse_args()

    # give args a friendly name
    host = args.HOST
    num_threads = args.threads

    if (args.start is not None) and (args.end is None):
        # if only start port is issued
        start_port = args.start
        end_port = args.start + 1
    elif (args.start is not None) and (args.end is not None):
        # if both args are issued
        start_port = args.start
        end_port = args.end + 1
    else:
        raise argp.error("[HOST] and --start are required, --end is optional")

    # track start time for performance display
    start_time = time.time()

    # spawn a number of threads to scan a queue of ports
    start_threads(num_threads)

    # queue up the ports to be scanned
    for port in range(start_port, end_port):
        # use a list to store host:port on a single queue entry
        q.put([host, port])

    # hold until all ports have been scanned
    q.join()

    # display performance data
    run_time = float("%0.2f" % (time.time() - start_time))
    print("Run Time: %f seconds" % run_time)

if __name__ == '__main__':
    main()
