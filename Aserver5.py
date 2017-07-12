# server.py
# Fib microservice

from socket import *
from fib import fib
from collections import deque
from select import select

tasks = deque()

recv_wait = { }         # Mapping sockets -> tasks (generators)
send_wait = { }

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

        req = client.recv(100)  #blocking ( waiting for data )
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'

        yield 'send', client

        client.send(resp) #blocking  ( send data - buffer blocking )
    print("Closed")

tasks.append(fib_server(('',25000)))
run()

# RUN Commands

# python -i Aserver4.py
# run perf1.py
# run perf2.py
# It faces same problems
# fix it with Pool