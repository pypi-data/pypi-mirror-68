import sys, os
import time

from OpenVisus.PyUtils import *
from OpenVisus.PyImage import *

from PyQt5 import Qt,QtCore,QtGui,QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import PyQt5.sip as sip

# ///////////////////////////////////////////////////////////////
class GuiUtils:

	@staticmethod
	def processEvents():
		QtWidgets.QApplication.instance().processEvents()

	# horizontalLayout
	@staticmethod
	def horizontalLayout(*widgets):
		ret=QHBoxLayout()
		for it in widgets: 
			try:
				ret.addWidget(it) 
			except:
				try:
					ret.addLayout(it)	
				except:
					ret.addItem(it)
		return ret			
		
	# verticalLayout
	@staticmethod
	def verticalLayout(*widgets):
		ret=QVBoxLayout()
		for it in widgets: 
			try:
				ret.addWidget(it) 
			except:
				try:
					ret.addLayout(it)	
				except:
					ret.addItem(it)
		return ret				

	# createPushButton
	@staticmethod
	def createPushButton(text,callback=None, img=None ):
		ret=QPushButton(text)
		#ret.setStyleSheet("QPushButton{background: transparent;}");
		ret.setAutoDefault(False)
		if callback:
			ret.clicked.connect(callback)
		if img:
			ret.setIcon(QtGui.QIcon(img))
		return ret

	# createImageButton  
	def createImageButton(img, callback=None):
		
		class ImageButton(QAbstractButton):
			def __init__(self, pixmap, parent=None):
				super(ImageButton, self).__init__(parent)
				self.pixmap = pixmap

			# paintEvent
			def paintEvent(self, event):
				painter = QPainter(self)
				painter.drawPixmap(event.rect(), self.pixmap)

			# sizeHint
			def sizeHint(self):
				return self.pixmap.size()		
		
		
		ret=ImageButton(QPixmap(img))
		if callback:
			ret.clicked.connect(callback)
		return ret		

	# appendText
	@staticmethod
	def appendText(widget,s):
		widget.moveCursor (QtGui.QTextCursor.End)
		widget.insertPlainText(s + "\n")
		widget.moveCursor (QtGui.QTextCursor.End)		
		
	# getImageFormats
	@staticmethod
	def getImageFormats():

		return {
			0:"QImage::Format_Invalid", #		The image is invalid.
			1:"QImage::Format_Mono",     #		The image is stored using 1-bit per pixel. Bytes are packed with the most significant bit (MSB) first.
			2:"QImage::Format_MonoLSB",  #		The image is stored using 1-bit per pixel. Bytes are packed with the less significant bit (LSB) first.
			3:"QImage::Format_Indexed8", #		The image is stored using 8-bit indexes into a colormap.
			4:"QImage::Format_RGB32",    #		The image is stored using a 32-bit RGB format (0xffRRGGBB).
			5:"QImage::Format_ARGB32",   #		The image is stored using a 32-bit ARGB format (0xAARRGGBB).
			6:"QImage::Format_ARGB32_Premultiplied",#	The image is stored using a premultiplied 32-bit ARGB format (0xAARRGGBB), i.e. the red, green, and blue channels are multiplied by the alpha component divided by 255. (If RR, GG, or BB has a higher value than the alpha channel, the results are undefined.) Certain operations (such as image composition using alpha blending) are faster using premultiplied ARGB32 than with plain ARGB32.
			7:"QImage::Format_RGB16",#		The image is stored using a 16-bit RGB format (5-6-5).
			8:"QImage::Format_ARGB8565_Premultiplied",#		The image is stored using a premultiplied 24-bit ARGB format (8-5-6-5).
			9:"QImage::Format_RGB666",#		The image is stored using a 24-bit RGB format (6-6-6). The unused most significant bits is always zero.
			10:"QImage::Format_ARGB6666_Premultiplied",#		The image is stored using a premultiplied 24-bit ARGB format (6-6-6-6).
			11:"QImage::Format_RGB555",#		The image is stored using a 16-bit RGB format (5-5-5). The unused most significant bit is always zero.
			12:"QImage::Format_ARGB8555_Premultiplied",#		The image is stored using a premultiplied 24-bit ARGB format (8-5-5-5).
			13:"QImage::Format_RGB888",#		The image is stored using a 24-bit RGB format (8-8-8).
			14:"QImage::Format_RGB444",#		The image is stored using a 16-bit RGB format (4-4-4). The unused bits are always zero.
			15:"QImage::Format_ARGB4444_Premultiplied",#		The image is stored using a premultiplied 16-bit ARGB format (4-4-4-4).
			16:"QImage::Format_RGBX888",#		The image is stored using a 32-bit byte-ordered RGB(x) format (8-8-8-8). This is the same as the Format_RGBA8888 except alpha must always be 255.
			17:"QImage::Format_RGBA8888",#		The image is stored using a 32-bit byte-ordered RGBA format (8-8-8-8). Unlike ARGB32 this is a byte-ordered format, which means the 32bit encoding differs between big endian and little endian architectures, being respectively (0xRRGGBBAA) and (0xAABBGGRR). The order of the colors is the same on any architecture if read as bytes 0xRR,0xGG,0xBB,0xAA.
			18:"QImage::Format_RGBA8888_Premultiplied",#		The image is stored using a premultiplied 32-bit byte-ordered RGBA format (8-8-8-8).
			19:"QImage::Format_BGR30",#		The image is stored using a 32-bit BGR format (x-10-10-10).
			20:"QImage::Format_A2BGR30_Premultiplied",#		The image is stored using a 32-bit premultiplied ABGR format (2-10-10-10).
			21:"QImage::Format_RGB30",#		The image is stored using a 32-bit RGB format (x-10-10-10).
			22:"QImage::Format_A2RGB30_Premultiplied",#		The image is stored using a 32-bit premultiplied ARGB format (2-10-10-10).
			23:"QImage::Format_Alpha8",#		The image is stored using an 8-bit alpha only format.
			24:"QImage::Format_Grayscale8",#		The image is stored using an 8-bit grayscale format.		
		}



# ///////////////////////////////////////////////////////////////////////////////////////
class ProgressLine(QHBoxLayout):
	
	# constructor
	def __init__(self):
		super(ProgressLine, self).__init__()
		self.message=QLabel()
		self.bar=QProgressBar()
		self.addWidget(self.message)
		self.addWidget(self.bar)
		self.hide()

	# show
	def show(self):
		self.bar.show()
		self.message.show()
		GuiUtils.processEvents()

	# hide
	def hide(self):
		self.bar.hide()
		self.message.hide()
		GuiUtils.processEvents()

	# setRange
	def setRange(self,min,max):
		self.bar.setMinimum(min)
		self.bar.setMaximum(max)
		self.bar.setValue(min)
		GuiUtils.processEvents()

	# setMessage
	def setMessage(self,msg):
		print(msg)
		self.message.setText(msg)
		GuiUtils.processEvents()

	# value
	def value(self):
		return self.bar.value()
		
	# setValue
	def setValue(self,value):
		value=max(value,self.bar.minimum())
		value=min(value,self.bar.maximum())
		self.bar.setValue(value)
		GuiUtils.processEvents()	

__splash__=None
			
# ////////////////////////////////////////////////////////////////////////////////////////////
def ShowSplash():
	global __splash__
	if __splash__: return
	filename=os.path.join(ThisDir(__file__), 'resources/images/visoar.png')
	if not os.path.isfile(filename): raise Exception('internal error')
	img = QPixmap(filename)
	__splash__ = QSplashScreen(img)
	__splash__.setWindowFlags(QtCore.Qt.FramelessWindowHint) # QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
	__splash__.setEnabled(False)
	__splash__.show()
	__splash__.showMessage("<h1><font color='green'>Welcome</font></h1>", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)	

# ////////////////////////////////////////////////////////////////////////////////////////////
def HideSplash():
	global __splash__
	if not __splash__: return
	__splash__.close()
	__splash__=None

# ////////////////////////////////////////////////////////////////////////////////////////////
class PreviewImage(QWidget):

	# constructor
	def __init__(self,max_size=1024):
		super(PreviewImage,self).__init__()
		self.label = QLabel(self)
		self.max_size=max_size

	# showPreview
	def showPreview(self,img,title):
		img=ResizeImage(img,self.max_size)

		img=img[:,:,0:3]
		H,W,nchannels=img.shape[0:3]

		if nchannels==1:
			qimage = QtGui.QImage(img, W,H, nchannels * W, QtGui.QImage.Format_Grayscale8)
		elif nchannels==2:
			R,G=img[:,:,0], img[:,:,1] 
			img=InterleaveChannels(R,G,G)
			qimage = QtGui.QImage(img, W,H, nchannels * W, QtGui.QImage.Format_RGB888)
		else:
			qimage = QtGui.QImage(img, W,H, nchannels * W, QtGui.QImage.Format_RGB888)

		pixmap = QPixmap(qimage)
		self.label.setPixmap(pixmap)
		self.resize(pixmap.width(),pixmap.height())
		self.setWindowTitle(title)
		self.show()
