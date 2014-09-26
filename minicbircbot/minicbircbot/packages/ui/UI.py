import sys
import os
import PySide
import PySide.QtCore as _qc
import PySide.QtGui as _qg



class UI(_qg.QWidget):

	def __init__(self):
		super().__init__()




if __name__ == "__main__":

	#test
	app = _qg.QApplication(sys.argv)
	gui  = UI()

	gui.showNormal()
	app.exec_()
