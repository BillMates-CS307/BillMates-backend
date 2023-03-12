import threading

# Given a function (func), and arguments (arg), start a thread with this information

def fire(func, args):
    threading.Thread(target=func, args=args).start()