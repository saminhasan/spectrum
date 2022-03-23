#! /bin/python3
import time
import tkinter as tk  
from pySerialTransfer import pySerialTransfer as pt
import serial.tools.list_ports
class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		#self.master.geometry("320x240")
		self.pack()
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino Mega 2560" in p.description:
				print (p[0] )
				self.port = p[0]
				
				#p.close()
				
		time.sleep(1)
		
		self.connection_status = 'disconnected'
		self.counter = 0
		self.uplimit = None
		self.lowlimit = None
		
		self.create_widgets()
		#self.port = 'COM12'
		self.link = pt.SerialTransfer(self.port)
		
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
	
		self.inputtxt = tk.Text(self, height = 1, width = 24)
		#self.inputtxt.insert(tk.END, self.DEVICE_IP)
		self.inputtxt.grid(sticky="ew",row=2, column=0, columnspan=3, padx=4, pady=4)
		# Button Creation
		printButton = tk.Button(self, text = "Print", command = self.printInput)
		printButton.grid(sticky="ew", row=3, column=0, columnspan=3, padx=4, pady=4)
		
	def printInput(self):
		inp = self.inputtxt.get(1.0, "end-1c")
		self.counter = int(inp)
		self.send_data()
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