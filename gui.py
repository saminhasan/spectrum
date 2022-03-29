#! /bin/python3
import time
import tkinter as ttk  
from pySerialTransfer import pySerialTransfer as pt
import serial.tools.list_ports


class Application(ttk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.geometry("480x320")
		self.pack()
		
				
				
		
		self.counter = 0
		self.uplimit = None
		self.lowlimit = None
		self.connected = False
		self.port = None
		self.ports = list(serial.tools.list_ports.comports())
		for port in self.ports:
			if "Arduino Mega 2560" in p.description:
				print (port[0])
				self.port = port[0]
		self.ports.append("None")
		
		self.create_widgets()
		#self.link = pt.SerialTransfer(self.port)
		
	def create_widgets(self):
	
		self.button0 = ttk.Button(self, text = "Connect", command = self.connect)
		self.button0.grid(sticky="ew", row = 0, column = 0, columnspan=3,  padx=4, pady=4)
		if len(self.ports) ==1:
			self.button0['state'] = 'disabled'
		else:
			self.button0['state'] = 'normal'
		
		
		self.port_number = ttk.StringVar()
		self.port_number.set(self.port)
		
		self.ddmenu = ttk.OptionMenu(self, self.port_number, *self.ports)
		self.ddmenu.grid(sticky="ew", row = 1, column = 0, columnspan=3,  padx=4, pady=4)	
		if len(self.ports) == 0:
			self.ddmenu['state'] = 'disabled'
		else:
			self.ddmenu['state'] = 'normal'

		
		self.button1 = ttk.Button(self, text = "Move Up", command = self.moveup)
		self.button1.grid(sticky="ew", row = 2, column = 0, padx=4, pady=4)

		self.button2 = ttk.Button(self, text = "Move Down", command = self.movedown, padx=4, pady=4)
		self.button2.grid(sticky="ew",row = 3, column = 0)

		self.slider = ttk.Scale(self, from_ = 100, to_ = -100, tickinterval=0, command=self.slider_set_position)
		self.slider.grid(sticky="ew", row = 2, column = 1, rowspan = 2, padx=4, pady=4)
		self.slider['state'] = 'disabled'
		#self.slider['state'] = 'normal'


		self.button3 = ttk.Button(self, text = "Set uppper limit", command = self.set_upper_limit)
		self.button3.grid(sticky="ew", row = 2, column = 2, padx=4, pady=4)

		self.button4 = ttk.Button(self, text = "Set  lower limit", command = self.set_lower_limit)
		self.button4.grid(sticky="ew", row = 3, column = 2, padx=4, pady=4)
	
		self.inputtxt = ttk.Text(self, height = 1, width = 24)
		self.inputtxt.insert(ttk.END , self.counter)
		self.inputtxt.grid(sticky="ew",row=5, column=0, columnspan=3, padx=4, pady=4)
		
		self.movebutton = ttk.Button(self, text = "Move to Position", command = self.move_to_position)
		self.movebutton.grid(sticky="ew", row=6, column=0, columnspan=3, padx=4, pady=4)	
		
		self.stopbutton = ttk.Button(self, text = "    STOP   ", command = self.stop, bg='red')
		self.stopbutton.grid(sticky="news", row=7, column=0,columnspan=3, padx=4, pady=4)
		
		
	def connect(self):
		if self.port is not None:
		
			try:
				self.link = pt.SerialTransfer(self.port)
				if self.link:
					self.connected = True
			except Exception as exception:
				print(exception)
		else:
			print("Microcontroller Port Not Found")
		
		
	def move_to_position(self):
		inp = self.inputtxt.get(1.0, "end-1c")
		#print(inp)
		self.counter = int(inp)
		self.send_data()
			


		
	def moveup(self):
		self.counter += 1
		self.inputtxt.delete('1.0', ttk.END)
		self.inputtxt.insert(ttk.END , self.counter)

		self.send_data()
		#print("moveup : ", self.counter)

		
	def movedown(self):
		self.counter -= 1
		self.inputtxt.delete('1.0', ttk.END)
		self.inputtxt.insert(ttk.END , self.counter)
		self.send_data()
		#print("movedown : ", self.counter)


	def slider_set_position(self, slider_value):

			self.counter = int(slider_value)
			self.inputtxt.delete('1.0', ttk.END)
			self.inputtxt.insert(ttk.END , self.counter)
			self.send_data()
			#print("set_position : ", slider_value)

		
	def set_upper_limit(self):
		self.uplimit = self.counter
		if self.uplimit is not None and self.lowlimit is not None and int(self.uplimit) > int(self.lowlimit):
			self.slider['state'] = 'normal'
			self.slider.config(from_=self.uplimit, to=self.lowlimit)
		print(" \n set_upper_limit : ", self.uplimit)


		
	def set_lower_limit(self):
		self.lowlimit = self.counter
		if self.uplimit is not None and self.lowlimit is not None and int(self.uplimit) > int(self.lowlimit):
			self.slider['state'] = 'normal'
			self.slider.config(from_=self.uplimit, to=self.lowlimit)
		print("\n set_lower_limit : ", self.lowlimit)
		
		
	def send_data(self):
		print("counter : {}".format(self.counter), end='\r')

		return
		sendsize = 0;
		sendsize = self.link.tx_obj(self.counter, start_pos=sendsize)
		self.link.send(sendsize)
	
	def stop(self):
		print("EMERGERCY STOP TBI")
		
def main():
	root = ttk.Tk()
	root.title("Open-Loop Height Control")
	#root.resizable(0, 0)

	app = Application(master=root)
	app.mainloop()
	'''
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("KeyboardInterrupt")
	'''
if __name__ == "__main__":
	main()