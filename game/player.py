import pyglet, math
from pyglet.window import key
import physicalobject, resources

class Player(physicalobject.PhysicalObject):
	
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=resources.player_image,
									*args, **kwargs)
		self.thrust = 300.0
		self.rotate_speed = 200.0
		
		self.engine_sprite = pyglet.sprite.Sprite(
			img=resources.engine_image, *args, **kwargs)
		self.engine_sprite.visible = False

		self.key_handler = key.KeyStateHandler()
			
	def update(self, dt):
		super(Player, self).update(dt)
		
		if self.key_handler[key.A]:
			self.rotation -= self.rotate_speed * dt
		if self.key_handler[key.D]:
			self.rotation += self.rotate_speed * dt
		if self.key_handler[key.W]:
			angle_radians = -math.radians(self.rotation)
			force_x = math.cos(angle_radians) * self.thrust * dt
			force_y = math.sin(angle_radians) * self.thrust * dt
			self.velocity_x += force_x
			self.velocity_y += force_y
			self.engine_sprite.rotation = self.rotation
			self.engine_sprite.x = self.x
			self.engine_sprite.y = self.y
			self.engine_sprite.visible = True
		else:
			self.engine_sprite.visible = False
		if self.key_handler[key.S]:
			angle_radians = -math.radians(self.rotation)
			force_x = math.cos(angle_radians) * self.thrust * dt
			force_y = math.sin(angle_radians) * self.thrust * dt
			self.velocity_x -= force_x/2
			self.velocity_y -= force_y/2
		if self.key_handler[key.Q]:
			angle_radians = -math.radians(self.rotation)
			force_x = math.cos(angle_radians) * self.thrust * dt
			self.velocity_x -= force_x
		if self.key_handler[key.E]:
			angle_radians = -math.radians(self.rotation)
			force_x = math.cos(angle_radians) * self.thrust * dt
			self.velocity_x += force_x
	
	def delete(self):
		self.engine_sprite.delete()
		super(Player,self).delete()