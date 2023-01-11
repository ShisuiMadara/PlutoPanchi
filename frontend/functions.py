
class req ():

	def __init__ (self, roll, pitch, yaw, throttle, head_free, dev_mode, alt_hold, is_armed, command_type):

		self.roll = 1500
		self.pitch = 1500
		self.yaw = 1500
		self.throttle = 1500
		self.head_free = True
		self.dev_mode = True
		self.alt_hold = True
		self.is_armed = False
		

	def arm (self):

		#do arming 
		self.is_armed = True

		#publish

	def disarm (self):

		#do disarming
		self.is_armed = False

		#publish

	def forward (self):

		self.pitch += 200

		#publish

	def backward (self):

		self.pitch -= 200

		#publish

	def left (self):

		self.roll -= 200

		#publish

	def right (self):

		self.roll += 200

		#publish

	def left_yaw (self):

		self.yaw -= 200

		#publish

	def right_yaw (self):

		self.yaw += 200

		#publish

	def increase_height (self):

		self.throttle += 100

		#publish

	def decrease_height (self):

		self.throttle -= 100

		#publish

	def take_off (self):

		self.arm()
		self.command_type = 1

		#publish

	def land (self):

		self.command_type = 2

		#publish

	def reset (self):

		self.roll = 1500
		self.yaw = 1500
		self.pitch = 1500
		self.throttle = 1500

		#publish

if __name__ == '__main__':
	test = req()






