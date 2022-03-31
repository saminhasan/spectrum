import time
import tkinter as tk
import serial.tools.list_ports
from pySerialTransfer import pySerialTransfer as pt

class State(object):
	def __init__(self):
		self.acceleration = 100.0
		self.maxspeed = 100.0
		self.position = 0
		self.uplimit = 0
		self.lowlimit = 0
		self.stop = True
		self.set_param = False

		
class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.geometry("1024x600")
		self.pack()
		
		
		self.state = State()
		self.position = 0
		self.uplimit = 0
		self.lowlimit = 0
		self.acceleration = 10
		self.maxspeed = 1000
		self.stop = True
		self.set_param = False
		
		
		self.connected = False
		self.port = 'None'
		self.ports = []

		self.scan_ports()
		self.create_widgets()


	def scan_ports(self):
		self.ports = list(serial.tools.list_ports.comports())
		#self.ports = ['None','Money'] # move in constructor

		
	def create_widgets(self):

		self.button0 = tk.Button(self, text = "Connect", command = self.connect)
		self.button0.grid(sticky="ew", row = 0, column = 3,   padx=4, pady=4)
		if len(self.ports) < 1:
			self.button0['state'] = 'disabled'
		else:
			self.button0['state'] = 'normal'


		self.port_number = tk.StringVar()
		self.port_number.set(self.port)

		self.ddmenu0_0 = tk.OptionMenu(self, self.port_number, *self.ports, command=self.set_port)
		self.ddmenu0_0.grid(sticky="ew", row = 0, column = 0, columnspan=3,  padx=4, pady=4)
		
		if len(self.ports) < 1:
			self.ddmenu0_0['state'] = 'disabled'
		else:
			self.ddmenu0_0['state'] = 'normal'

		self.button2_0 = tk.Button(self, text = "Move Up", command = self.moveup)
		self.button2_0.grid(sticky="ew", row = 1, column = 0, padx=4, pady=4)
		
		self.inputtxt_acc = tk.Text(self, height = 1, width = 24)
		self.inputtxt_acc.insert(tk.END , self.acceleration)
		self.inputtxt_acc.grid(sticky="ew",row=1, column=3, padx=4, pady=4)
		
		self.button3_4 = tk.Button(self, text = "set Acceleration", command = self.setAcceleration, padx=4, pady=4)
		self.button3_4.grid(sticky="ew",row = 2, column = 3, padx=4, pady=4)
		

		
		self.inputtxt_vel = tk.Text(self, height = 1, width = 24)
		self.inputtxt_vel.insert(tk.END , self.maxspeed)
		self.inputtxt_vel.grid(sticky="ew",row=3, column=3, padx=4, pady=4)
		
		
		self.button3_3 = tk.Button(self, text = "set MaxSpeed", command = self.setMaxSpeed, padx=4, pady=4)
		self.button3_3.grid(sticky="ew",row = 4, column = 3, padx=4, pady=4)
		
		
		self.button3_0 = tk.Button(self, text = "Move Down", command = self.movedown, padx=4, pady=4)
		self.button3_0.grid(sticky="ew",row = 4, column = 0, padx=4, pady=4)

		self.slider = tk.Scale(self, from_ = 100, to_ = -100, tickinterval=0, command=self.slider_set_position)
		self.slider.grid(sticky="ew", row = 1, column = 1, rowspan = 4, padx=1, pady=1)
		self.slider['state'] = 'disabled'

		self.button3 = tk.Button(self, text = "Set uppper limit", command = self.set_upper_limit)
		self.button3.grid(sticky="ew", row = 1, column = 2, padx=4, pady=4)

		self.button4 = tk.Button(self, text = "Set  lower limit", command = self.set_lower_limit)
		self.button4.grid(sticky="ew", row = 4, column = 2, padx=4, pady=4)

		self.inputtxt_pos = tk.Text(self, height = 1, width = 24)
		self.inputtxt_pos.insert(tk.END , self.position)
		self.inputtxt_pos.grid(sticky="ew",row=5, column=0, columnspan=3, padx=4, pady=4)

		self.movebutton = tk.Button(self, text = "Move to Position", command = self.move_to_position)
		self.movebutton.grid(sticky="ew", row=5, column=3, padx=4, pady=4)

		self.stopbutton = tk.Button(self, text = "    START   ", command = self.e_stop, bg='green')
		self.stopbutton.grid(sticky="ew", row=6, column=0,columnspan=4, padx=4, pady=4)
		
		self.statusvar = tk.StringVar()
		self.statusvar.set("Disconneted")
		self.sbar = tk.Label(self, textvariable=self.statusvar, relief=tk.SUNKEN, anchor="w")
		self.sbar.grid( row=7, column=0,columnspan=4)
		

		#r,c =  8 , 3
		#
		
		
	def setAcceleration(self):
		inp = self.inputtxt_acc.get(1.0, "end-1c")
		self.acceleration = int(inp)
		self.set_param = True
		self.send_data()
		self.set_param = False

		#print(self.acceleration)
	
	
	def setMaxSpeed(self):
		inp = self.inputtxt_vel.get(1.0, "end-1c")
		self.maxspeed = int(inp)
		#print(self.maxspeed)
		self.set_param = True
		self.send_data()
		self.set_param = False

	
	
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
		inp = self.inputtxt_pos.get(1.0, "end-1c")
		self.position = int(inp)
		self.send_data()


	def moveup(self):
		counter = self.position + 1
		self.update_counter(int(counter))
		self.send_data()


	def movedown(self):
		counter = self.position - 1
		self.update_counter(int(counter))
		self.send_data()


	def slider_set_position(self, slider_value):
			self.update_counter(int(slider_value))


	def update_counter(self, counter):
		self.position = counter
		self.inputtxt_pos.delete('1.0', tk.END)
		self.inputtxt_pos.insert(tk.END , self.position)


	def set_upper_limit(self):
		self.uplimit = self.position
		if self.uplimit is not None and self.lowlimit is not None and int(self.uplimit) > int(self.lowlimit):
			self.slider['state'] = 'normal'
			self.slider.config(from_=self.uplimit, to=self.lowlimit)
		print(" \n set_upper_limit : ", self.uplimit)


	def set_lower_limit(self):
		self.lowlimit = self.position
		if self.uplimit is not None and self.lowlimit is not None and int(self.uplimit) > int(self.lowlimit):
			self.slider['state'] = 'normal'
			self.slider.config(from_=self.uplimit, to=self.lowlimit)
		print("\n set_lower_limit : ", self.lowlimit)


	def send_data(self):
		#print("position : {}".format(self.position), end='\r')
		#sendsize = 0;
		#sendsize = self.link.tx_obj(self.position, start_pos=sendsize)
		#self.link.send(sendsize)
		self.state.acceleration = self.acceleration
		self.state.maxspeed = self.maxspeed
		self.state.position = self.position
		self.state.uplimit = self.uplimit
		self.state.lowlimit = self.lowlimit
		self.state.stop = self.stop
		self.state.set_param = self.set_param
		'''
		self.acceleration = 100.0
		self.maxspeed = 100.0
		self.position = 0
		self.uplimit = 0
		self.lowlimit = 0
		self.stop = True
		self.set_param = False
		'''
		
		sendsize = 0;
		sendsize = self.link.tx_obj(self.state.acceleration, start_pos=sendsize)
		sendsize = self.link.tx_obj(self.state.maxspeed, start_pos=sendsize)
		sendsize = self.link.tx_obj(self.state.position, start_pos=sendsize)
		sendsize = self.link.tx_obj(self.state.uplimit, start_pos=sendsize)
		sendsize = self.link.tx_obj(self.state.lowlimit, start_pos=sendsize)
		sendsize = self.link.tx_obj(self.state.stop, start_pos=sendsize)
		sendsize = self.link.tx_obj(self.state.set_param, start_pos=sendsize)
		self.link.send(sendsize)


	def e_stop(self):

		self.stop = not self.stop

		print(self.stop)

		if self.stop:
			self.stopbutton.configure(text = "Start", bg='green')
			
		else:
			self.stopbutton.configure(text = "Stop", bg='red')

		self.set_param = True
		self.send_data()
		self.set_param = False

		
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
