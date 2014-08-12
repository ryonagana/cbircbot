import os
import sys



class A:

	def __init__(self):
		print ("Carregado")


	def methA(self):
		print ("Method A Loaded from Class A -- Dad")
		pass
		

	def methB(self):
		print ("Method A Loaded from Class A -- Dad")
		pass
		



class B(A):

	def __init__(self):
		super().__init__()

	def methA(self):
		super().methA()
		print ("Callin Method A from Class B - Child")

	def methB(self):
		super().methB()
		print ("Callin Method B from Class B -- Child")


if __name__ == "__main__":

	b = B()

	b.methA()
	b.methB()