# import threading
#
# def my_func():
#     print(threading.currentThread().isDaemon())
#
#
# new_thread = threading.Thread(target=my_func)
# new_thread.setDaemon(True)
# new_thread.start()          # True



# def my_func():
#     print(threading.currentThread().getName())
#
#
# new_thread = threading.Thread(target=my_func())
# new_thread.start()      # MainThread
#

# def my_function():
#     time.sleep(2)   # after 2 seconds (False)
#
#
# new_thread = threading.Thread(target=my_function())
# new_thread.start()
#
# print(new_thread.is_alive())
# time.sleep(3)       # after 3 seconds (False)
# print(new_thread.is_alive())


# def my_function():
#     print(threading.currentThread().getName())
#
#
# new_thread = threading.Thread(target=my_function, name="MyNewThread")
# new_thread.start()      # MyNewThread



def smart_divide(func):
    def inner(a, b):
        print(f"this is {a} and {b}")
        if b == 0:
            print("Please Dont")
            return
        return func(a, b)
    return inner


@smart_divide
def divide(a, b):
    print(a/b)


divide(10, 4)
divide(2, 5)
