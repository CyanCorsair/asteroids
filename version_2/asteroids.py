#Asteroids tutorial

import pyglet, random, math
from random import randint
from pyglet.window import key
from game import resources, load, player, asteroid

game_window = pyglet.window.Window(1024, 768)
main_batch = pyglet.graphics.Batch()
second_batch = pyglet.graphics.Batch()
counter_batch = pyglet.graphics.Batch()

key_handler = key.KeyStateHandler()
event_handlers = [key_handler]

player_ship = None
num_asteroids = randint(1,10)
asteroids_present = 0
game_objects = []
event_stack_size = 0

asteroids_label = pyglet.text.Label(
			text="Asteroids: 0", x=10, y=750, batch=counter_batch)
level_label = pyglet.text.Label(text="Asteroids! The Clone",
			x=400, y=750, anchor_x='center', batch=main_batch)
game_over_label = pyglet.text.Label(text="GAME OVER!", 
			x=512, y=-50, anchor_x='center', batch=second_batch)

def init():
	global num_asteroids
	
	asteroids_present = 0
	num_asteroids = 3
	reset_game()

def reset_game():
	global player_ship, game_objects, asteroids_present, event_stack_size
	
	while event_stack_size > 0:
		game_window.pop_handlers()
		event_stack_size -= 1
	
	player_ship = player.Player(x=400, y=300, batch=main_batch)
	asteroids = load.asteroids(num_asteroids, player_ship.position, batch=main_batch)
	asteroids_present += num_asteroids
	asteroids_label.text = "Asteroids: " + str(asteroids_present)
	game_objects = [player_ship] + asteroids
	game_over_label.y = -20
	
	for obj in game_objects:
		for handler in obj.event_handlers:
			game_window.push_handlers(handler)
			event_stack_size += 1
		
@game_window.event
def on_draw():
	game_window.clear()
	main_batch.draw()
	second_batch.draw()
	counter_batch.draw()
	
def update(dt):
	global asteroids_present

	player_dead = False

	for i in xrange(len(game_objects)):
		for j in xrange(i+1, len(game_objects)):
			obj_1 = game_objects[i]
			obj_2 = game_objects[j]
			
			if not obj_1.dead and not obj_2.dead:
				if obj_1.collides_with(obj_2):
					obj_1.handle_collision_with(obj_2)
					obj_2.handle_collision_with(obj_1)
					
	to_add = []
					
	for obj in game_objects:
		obj.update(dt)
		while asteroids_present < 3:
			new_asteroids = load.asteroids(randint(1,4), player_ship.position, batch=main_batch)
			to_add.extend(new_asteroids)
			asteroids_present += len(to_add)
			asteroids_label.text = "Asteroids: " + str(asteroids_present)
		to_add.extend(obj.new_objects)
		obj.new_objects = []
					
	for to_remove in [obj for obj in game_objects if obj.dead]:
		if to_remove == player_ship:
			player_dead = True
			game_over_label.y = 534
			asteroids_present = 0
		to_add.extend(obj.new_objects)
		to_remove.delete()
		game_objects.remove(to_remove)	
	
	if player_dead:
		reset_game()
	
	game_objects.extend(to_add)
		
if __name__ == '__main__':
	init()
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()