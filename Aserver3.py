# server.py
# Fib microservice

from socket import *
from fib import fib
from collections import deque

tasks = deque()

def run():
    while tasks:
        task = tasks.popleft()
        try :
            why, what =  next(task) # run to the yield

            if why == 'recv':
                pass
            elif why == 'send':
                pass
            else:
                raise RuntimeError("ARG!")

            tasks.append(task)
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
        fib_handler(client)


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

fib_server(('',25000))
