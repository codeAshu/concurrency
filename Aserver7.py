# server.py
# Fib microservice

from socket import *
from fib import fib
from collections import deque
from select import select
from concurrent.futures import ThreadPoolExecutor as Pool

pool = Pool(10)

tasks = deque()
recv_wait = { }         # Mapping sockets -> tasks (generators)
send_wait = { }
future_wait = { }

future_notify, future_event = socketpair()

def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')

def future_monitor():
    while True:
        yield 'recv', future_event
        future_event.recv(100)

tasks.append(future_monitor())

def run():

    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # No active tasks to run
            # wait for I/O
            can_recv, can_send, _ = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))


        task = tasks.popleft()
        try :
            why, what =  next(task) # run to the yield

            if why == 'recv':
                # Must go wait somewhere
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            elif why == 'future':
                future_wait[what] = task
                what.add_done_callback(future_done)
            else:

                raise RuntimeError("ARG!")
        except StopIteration:
            print("Task Done!")

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:

        yield 'recv', sock

        client, addr = sock.accept() # blocking ( waiing for connection )
        print("Connection", addr)
        tasks.append(fib_handler(client))


def fib_handler(client):
    while True:

        yield 'recv', client

        req = client.recv(100)
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)

        yield "future", future

        result = future.result()                    # blocks
        resp = str(result).encode('ascii') + b'\n'

        yield 'send', client

        client.send(resp)
    print("Closed")

tasks.append(fib_server(('',25000)))
run()

