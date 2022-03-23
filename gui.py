#! /bin/python3

import tkinter as tk  
from pySerialTransfer import pySerialTransfer as pt

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		#self.master.geometry("320x240")
		self.pack()
		self.connection_status = 'disconnected'
		self.counter = 0
		self.uplimit = None
		self.lowlimit = None
		
		self.create_widgets()
		self.link = pt.SerialTransfer('COM12')
		
	def create_widgets(self):
		self.button1 = tk.Button(self, text = "Move Up", command = self.moveup)
		self.button1.grid(sticky="ew", row = 0, column = 0, padx=4, pady=4)

		self.button2 = tk.Button(self, text = "Move Down", command = self.movedown, padx=4, pady=4)
		self.button2.grid(sticky="ew",row = 1, column = 0)

		self.slider = tk.Scale(self, from_ = 100, to_ = -100, tickinterval=1, command=self.set_position)
		self.slider.grid(sticky="ew", row = 0, column = 1, rowspan = 2, padx=4, pady=4)
		self.slider['state'] = 'disabled'
		#self.slider['state'] = 'normal'


		self.button3 = tk.Button(self, text = "Set uppper limit", command = self.set_upper_limit)
		self.button3.grid(sticky="ew", row = 0, column = 2, padx=4, pady=4)

		self.button4 = tk.Button(self, text = "Set  lower limit", command = self.set_lower_limit)
		self.button4.grid(sticky="ew", row = 1, column = 2, padx=4, pady=4)
	
	def moveup(self):
		self.counter += 1
		self.send_data()
		#print("moveup : ", self.counter)
		print("counter : ", self.counter, end='\r')

		
	def movedown(self):
		self.counter -= 1
		self.send_data()

		#print("movedown : ", self.counter)
		print("counter : ", self.counter, end='\r')


	def set_position(self, slider_value):
		self.counter = int(slider_value)
		self.send_data()

		#print("set_position : ", slider_value)
		print("counter : ", self.counter, end='\r')

		
		
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
		sendsize = 0;
		sendsize = self.link.tx_obj(self.counter, start_pos=sendsize)
		self.link.send(sendsize)
def main():
	root = tk.Tk()
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