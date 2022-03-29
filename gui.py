import time
import tkinter as tk
from pySerialTransfer import pySerialTransfer as pt
import serial.tools.list_ports


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.geometry("1024x480")
		self.pack()

		self.counter = 0
		self.uplimit = None
		self.lowlimit = None
		self.connected = False
		self.port = None
		self.ports = None

		self.scan_ports()
		self.create_widgets()


	def scan_ports(self):
		self.ports = list(serial.tools.list_ports.comports())

		
	def create_widgets(self):

		self.button0 = tk.Button(self, text = "Connect", command = self.connect)
		self.button0.grid(sticky="ew", row = 0, column = 0, columnspan=3,  padx=4, pady=4)
		
		if len(self.ports) < 1:
			self.button0['state'] = 'disabled'
		else:
			self.button0['state'] = 'normal'


		self.port_number = tk.StringVar()
		self.port_number.set(self.port)

		self.ddmenu = tk.OptionMenu(self, self.port_number, *self.ports,command=self.set_port)
		self.ddmenu.grid(sticky="ew", row = 1, column = 0, columnspan=3,  padx=4, pady=4)
		
		if len(self.ports) == 0:
			self.ddmenu['state'] = 'disabled'
		else:
			self.ddmenu['state'] = 'normal'

		self.button1 = tk.Button(self, text = "Move Up", command = self.moveup)
		self.button1.grid(sticky="ew", row = 2, column = 0, padx=4, pady=4)

		self.button2 = tk.Button(self, text = "Move Down", command = self.movedown, padx=4, pady=4)
		self.button2.grid(sticky="ew",row = 3, column = 0)

		self.slider = tk.Scale(self, from_ = 100, to_ = -100, tickinterval=0, command=self.slider_set_position)
		self.slider.grid(sticky="ew", row = 2, column = 1, rowspan = 2, padx=4, pady=4)
		self.slider['state'] = 'disabled'

		self.button3 = tk.Button(self, text = "Set uppper limit", command = self.set_upper_limit)
		self.button3.grid(sticky="ew", row = 2, column = 2, padx=4, pady=4)

		self.button4 = tk.Button(self, text = "Set  lower limit", command = self.set_lower_limit)
		self.button4.grid(sticky="ew", row = 3, column = 2, padx=4, pady=4)

		self.inputtxt = tk.Text(self, height = 1, width = 24)
		self.inputtxt.insert(tk.END , self.counter)
		self.inputtxt.grid(sticky="ew",row=5, column=0, columnspan=3, padx=4, pady=4)

		self.movebutton = tk.Button(self, text = "Move to Position", command = self.move_to_position)
		self.movebutton.grid(sticky="ew", row=6, column=0, columnspan=3, padx=4, pady=4)

		self.stopbutton = tk.Button(self, text = "    STOP   ", command = self.stop, bg='red')
		self.stopbutton.grid(sticky="ew", row=7, column=0,columnspan=3, padx=4, pady=4)
		
		self.statusvar = tk.StringVar()
		self.statusvar.set("Disconneted")
		self.sbar = tk.Label(self, textvariable=self.statusvar, relief=tk.SUNKEN, anchor="w")
		self.sbar.grid(sticky="s", row=8, column=0,columnspan=3)

		
	def set_port(self, arg):
		port = arg
		self.port = port[0]


	def connect(self):
		if not self.connected:
			if self.port:
				self.link = pt.SerialTransfer(self.port)
				self.connected = self.link.open()
			if self.connected:
				self.button0.configure(text = "Disconnect")
				self.statusvar.set("Conneted - " + str(self.port))
				self.sbar.configure( textvariable=self.statusvar,bg="green")

			else:
				self.button0.configure(text = "Connect")
				self.statusvar.set("Disconneted")
				self.sbar.configure( textvariable=self.statusvar,bg="red")

		else:
			self.connected = self.link.close()
			self.button0.configure(text = "Connect")
			self.statusvar.set("Disconneted")
			self.sbar.configure( textvariable=self.statusvar,bg="red")


	def move_to_position(self):
		inp = self.inputtxt.get(1.0, "end-1c")
		self.counter = int(inp)
		self.send_data()


	def moveup(self):
		counter = self.counter + 1
		self.update_counter(int(counter))
		self.send_data()


	def movedown(self):
		counter = self.counter - 1
		self.update_counter(int(counter))
		self.send_data()


	def slider_set_position(self, slider_value):
			self.update_counter(int(slider_value))


	def update_counter(self, counter):
		self.counter = counter
		self.inputtxt.delete('1.0', tk.END)
		self.inputtxt.insert(tk.END , self.counter)


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
		sendsize = 0;
		sendsize = self.link.tx_obj(self.counter, start_pos=sendsize)
		self.link.send(sendsize)


	def stop(self):
		print("EMERGERCY STOP ->  CUT POWER")


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
