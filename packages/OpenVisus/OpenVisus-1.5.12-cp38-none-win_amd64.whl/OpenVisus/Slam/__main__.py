import os,sys
import subprocess
import glob
import platform
import numpy
import cv2
import datetime

from Slam.Slam2D import *
from Slam.Slam3D import *

from OpenVisusGui import *

from PyQt5 import QtCore 

from OpenVisus.PyUtils import *

# ////////////////////////////////////////////////////////////////////////////////////////////
def GetArg(name,default_value=""):

	for I in range(0,len(sys.argv)):
		if sys.argv[I]==name:
			ret=sys.argv[I+1]
			sys.argv=sys.argv[0:I] + sys.argv[I+2:]
			return ret
	return default_value


# //////////////////////////////////////////////////////////////////////////////
class Logger(QtCore.QObject):

	"""Redirects console output to text widget."""
	my_signal = QtCore.pyqtSignal(str)

	# constructor
	def __init__(self, terminal=None, filename="", qt_callback=None):
		super().__init__()
		self.terminal=terminal
		self.log=open(filename,'w')
		self.my_signal.connect(qt_callback)

	# write
	def write(self, message):
		message=message.replace("\n", "\n" + str(datetime.datetime.now())[0:-7] + " ")
		self.terminal.write(message)
		self.log.write(message)
		self.my_signal.emit(str(message))

	# flush
	def flush(self):
		self.terminal.flush()
		self.log.flush()



# ////////////////////////////////////////////////////////////////////////////////////////////
class ExceptionHandler(QtCore.QObject):

	# __init__
	def __init__(self):
		super(ExceptionHandler, self).__init__()
		sys.__excepthook__ = sys.excepthook
		sys.excepthook = self.handler

	# handler
	def handler(self, exctype, value, traceback):
		sys.stdout=sys.__stdout__
		sys.stderr=sys.__stderr__
		sys.excepthook=sys.__excepthook__
		sys.excepthook(exctype, value, traceback)


# ////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":

	# set PYTHONPATH=D:\projects\OpenVisus\build\RelWithDebInfo
	# example: -m Slam --pdim 2 "D:\GoogleSci\visus_slam\TaylorGrant"
	# example: -m Slam --pdim 3 "D:\GoogleSci\visus_dataset\male\RAW\Fullcolor\fullbody"

	SetCommandLine("__main__")
	app = QApplication(sys.argv)
	GuiModule.attach()  

	# since I'm writing data serially I can disable locks
	os.environ["VISUS_DISABLE_WRITE_LOCK"]="1"

	ShowSplash()

	pdim=int(GetArg("--pdim","2"))
	url=sys.argv[-1] if len(sys.argv)>1 else None
	
	win=Slam3DWindow() if pdim==3 else Slam2DWindow()
	#win.resize(1280,1024)
	#win.show()
	win.showMaximized()

	_stdout = sys.stdout
	_stderr = sys.stderr

	logger=Logger(terminal=sys.stdout, filename="~visusslam.log", qt_callback=win.printLog)

	sys.stdout = logger
	sys.stderr = logger

	if url is not None:
		win.setCurrentDir(url)
	else:
		win.chooseDirectory()

	exception_handler = ExceptionHandler()

	HideSplash()
	app.exec()

	sys.stdout = _stdout
	sys.stderr = _stderr
	GuiModule.detach()
	sys.exit(0)
