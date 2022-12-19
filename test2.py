
from threading import Thread
from time import sleep

def test(name):
	for i in range(5):
		print(name.a)
		sleep(1)

class A:
	def __init__(self, a) -> None:
		self.a = a

a = A(3)
thread = Thread(target = test, args = (a, ))
a.a = 2
thread.start()
print("FINISHED")