import pyglet, util

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image("player.png")
bullet_image = pyglet.resource.image("bullet.png")
asteroid_image = pyglet.resource.image("asteroid.png")
engine_image = pyglet.resource.image("engine_trail.png")
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height/2
	
util.center_image(player_image)
util.center_image(bullet_image)
util.center_image(asteroid_image)