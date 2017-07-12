def countdown(n):
    while n>0:
        yield  n
        n-=1


from collections import deque
tasks = deque()

tasks.extend([countdown(10), countdown(5), countdown(3)])


def run():
    while tasks:
        task = tasks.popleft()
        try :
            x = next(task)
            print(x)
            tasks.append(task)
        except StopIteration:
            print("Task")

run()


