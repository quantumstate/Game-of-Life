import sys
import pygtk
pygtk.require('2.0')
import gtk  	
import gtk.glade

size = [50,50]
drawScale = 4

class HellowWorldGTK:
	"""This is an Hello World GTK application"""

	def __init__(self):
		
		#Set the Glade file
		self.gladefile = "gui.glade"  
		self.wTree = gtk.glade.XML(self.gladefile) 
		
		#Get the Main Window, and connect the "destroy" event
		self.window = self.wTree.get_widget("MainWindow")
		self.lifeDisplay = self.wTree.get_widget("display_life")
		if (self.window):
			#Create our dictionay and connect it
			dic = { "on_start_clicked" : self.btn_start_clicked,
			        "on_step_clicked" : self.btn_step_clicked,
			        "on_life_event_button_press_event" : self.btn_life,
			        "on_MainWindow_destroy" : gtk.main_quit }
			self.wTree.signal_autoconnect(dic)
			self.window.connect("destroy", gtk.main_quit)
		
		self.pixBuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, size[0], size[1])
		self.pixBuf.fill(0xFFFFFFFF)
		self.pix = self.pixBuf.get_pixels_array()
		#self.pix2 = self.pixBuf.get_pixels()
		#self.lifeDisplay.set_from_pixbuf(self.pixBuf)
		self.update_display()
		
	def update_display(self):
		self.pixBuf = gtk.gdk.pixbuf_new_from_array(self.pix, gtk.gdk.COLORSPACE_RGB, 8)
		self.lifeDisplay.set_from_pixbuf(self.pixBuf.scale_simple(drawScale*size[0], drawScale*size[1], gtk.gdk.INTERP_TILES))
			
	def btn_start_clicked(self, widget):
		for i in range(10,25):
			self.pix[i][4] = [0,0,0]
		self.update_display()
	
	def btn_step_clicked(self, widget):
		#print "step"
		calculate_turn(self.pix)
		self.update_display()
		
	def btn_life(self, widget, event):
		(y,x) = (int(event.x / drawScale), int(event.y/drawScale))
		if x < len(self.pix) and y < len(self.pix[0]):
			if self.pix[x][y][0] == 255:
				self.pix[x][y] = [0,0,0]
			else:
				self.pix[x][y] = [255,255,255]
		#print (event.x, event.y)
		self.update_display()
		
def calculate_turn(grid):
	#print "hi"
	for x in range(1, len(grid)-1):
		for y in range(1, len(grid[0])-1):
			neighbours = count_neighbours(x,y,grid)
			if neighbours <= 1 or neighbours >=4:
				grid[x][y][1] = 255
			if neighbours == 3:
				grid[x][y][1] = 0
	for x in range(1, len(grid)-1):
		for y in range(1, len(grid[0])-1):
			grid[x][y] = [grid[x][y][1],grid[x][y][1],grid[x][y][1]]


#count the number of black neighbours
def count_neighbours(x,y,grid):
	count = 0
	points = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
	for p in points:
		if grid[x+p[0]][y+p[1]][0] == 0:
			count += 1
	return count

hwg = HellowWorldGTK()
gtk.main()
