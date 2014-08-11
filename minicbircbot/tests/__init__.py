import os
import sys



class A:

	def __init__(self):
		print ("Carregado")


	def methA(self):
		print ("Method A Loaded from Class A")
		

	def methB(self):
		print ("Method A Loaded from Class A")
		



class B(A):

	def __init__(self):
		super().__init__()

	def methA(self):
		print ("Callin Method A from Class B")

	def methB(self):
		print ("Callin Method B from Class B")


if __name__ == "__main__":

	b = B()

	b.methA()
	b.methB()