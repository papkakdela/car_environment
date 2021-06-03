import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes
import pygame
import math


def getCollisionPoint(x1, y1, x2, y2, x3, y3, x4, y4):

	uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
	uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
	if 0 <= uA <= 1 and 0 <= uB <= 1:
		intersectionX = x1 + (uA * (x2 - x1))
		intersectionY = y1 + (uA * (y2 - y1))
		return [intersectionX, intersectionY]
	return None


def dist(x1, y1, x2, y2):
	return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class MyWindow(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_minimum_size(400, 300)

		self.car_image = pyglet.image.load('car.png')
		self.car_image.anchor_x = self.car_image.width // 4
		self.car_image.anchor_y = self.car_image.height // 2
		self.car = pyglet.sprite.Sprite(self.car_image, x=50, y=50)
		self.batch = pyglet.graphics.Batch()

		self.tmp_x = -1
		self.tmp_y = -1

		self.lines = []
		self.lines.append(shapes.Line(10, 11, 11, 890, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1590, 11, 1591, 890, width=1, batch=self.batch))
		self.lines.append(shapes.Line(10, 11, 1590, 10, width=1, batch=self.batch))
		self.lines.append(shapes.Line(10, 891, 1590, 890, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1047, 620, 572, 668, width=1, batch=self.batch))
		self.lines.append(shapes.Line(572, 668, 298, 572, width=1, batch=self.batch))
		self.lines.append(shapes.Line(298, 572, 260, 469, width=1, batch=self.batch))
		self.lines.append(shapes.Line(260, 469, 335, 327, width=1, batch=self.batch))
		self.lines.append(shapes.Line(335, 327, 459, 245, width=1, batch=self.batch))
		self.lines.append(shapes.Line(459, 245, 626, 214, width=1, batch=self.batch))
		self.lines.append(shapes.Line(626, 214, 866, 205, width=1, batch=self.batch))
		self.lines.append(shapes.Line(866, 205, 1123, 238, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1123, 238, 1255, 363, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1255, 363, 1211, 501, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1211, 501, 1047, 620, width=1, batch=self.batch))
		self.lines.append(shapes.Line(542, 820, 145, 731, width=1, batch=self.batch))
		self.lines.append(shapes.Line(145, 731, 92, 522, width=1, batch=self.batch))
		self.lines.append(shapes.Line(92, 522, 82, 328, width=1, batch=self.batch))
		self.lines.append(shapes.Line(82, 328, 153, 162, width=1, batch=self.batch))
		self.lines.append(shapes.Line(153, 162, 375, 107, width=1, batch=self.batch))
		self.lines.append(shapes.Line(375, 107, 660, 64, width=1, batch=self.batch))
		self.lines.append(shapes.Line(660, 64, 1019, 60, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1019, 60, 1362, 164, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1362, 164, 1496, 391, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1496, 391, 1431, 600, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1431, 600, 1231, 724, width=1, batch=self.batch))
		self.lines.append(shapes.Line(1231, 724, 936, 774, width=1, batch=self.batch))
		self.lines.append(shapes.Line(936, 774, 542, 820, width=1, batch=self.batch))


		self.reset_car()


	def reset_car(self):

		self.angle = 0
		self.x = 770
		self.y = 135
		self.resist = 0.01
		self.acc = 0.05
		self.stop_acc = 2 * self.acc
		self.speed = 0
		self.velocity = 7
		self.rot_acc = 0.05
		self.rot_speed = 0
		self.rot_velocity = 0.3
		self.left_rotating = False
		self.right_rotating = False
		self.moving = False
		self.stoping = False


		self.dir_points = []
		self.dir_points.append([self.x + 3000 * math.cos(math.radians(self.angle)), self.y + 3000 * math.sin(math.radians(self.angle))])
		self.dir_points.append([self.x + 3000 * math.cos(math.radians(self.angle) - math.pi / 2), self.y + 3000 * math.sin(math.radians(self.angle) - math.pi / 2)])
		self.dir_points.append([self.x + 3000 * math.cos(math.radians(self.angle) + math.pi / 2), self.y + 3000 * math.sin(math.radians(self.angle) + math.pi / 2)])
		self.dir_points.append([self.x + 3000 * math.cos(math.radians(self.angle) - math.pi / 3), self.y + 3000 * math.sin(math.radians(self.angle) - math.pi / 3)])
		self.dir_points.append([self.x + 3000 * math.cos(math.radians(self.angle) + math.pi / 3), self.y + 3000 * math.sin(math.radians(self.angle) + math.pi / 3)])
		self.dir_points.append([self.x + 3000 * math.cos(math.radians(self.angle) - math.pi / 8), self.y + 3000 * math.sin(math.radians(self.angle) - math.pi / 8)])
		self.dir_points.append([self.x + 3000 * math.cos(math.radians(self.angle) + math.pi / 8), self.y + 3000 * math.sin(math.radians(self.angle) + math.pi / 8)])

		self.lengthes = [3000, 3000, 3000, 3000, 3000, 3000, 3000]



		for i in range(len(self.dir_points)):
			dir_len = dist(self.x, self.y, self.dir_points[i][0], self.dir_points[i][1])
			for j in self.lines:
				tmp_p = getCollisionPoint(self.x, self.y, self.dir_points[i][0], self.dir_points[i][1], j.x, j.y, j.x2, j.y2)
				if tmp_p:
					tmp_l = dist(self.x, self.y, tmp_p[0], tmp_p[1])
				else:
					tmp_l = 4000
				if tmp_l < dir_len:
					dir_len = tmp_l
					self.dir_points[i][0] = tmp_p[0]
					self.dir_points[i][1] = tmp_p[1]
			self.lengthes[i] = dir_len


		self.directions = []
		self.directions.append(shapes.Line(self.x, self.y, self.dir_points[0][0], self.dir_points[0][1], width=1, batch=self.batch))
		self.directions.append(shapes.Line(self.x, self.y, self.dir_points[1][0], self.dir_points[1][1], width=1, batch=self.batch))
		self.directions.append(shapes.Line(self.x, self.y, self.dir_points[2][0], self.dir_points[2][1], width=1, batch=self.batch))
		self.directions.append(shapes.Line(self.x, self.y, self.dir_points[3][0], self.dir_points[3][1], width=1, batch=self.batch))
		self.directions.append(shapes.Line(self.x, self.y, self.dir_points[4][0], self.dir_points[4][1], width=1, batch=self.batch))
		self.directions.append(shapes.Line(self.x, self.y, self.dir_points[5][0], self.dir_points[5][1], width=1, batch=self.batch))
		self.directions.append(shapes.Line(self.x, self.y, self.dir_points[6][0], self.dir_points[6][1], width=1, batch=self.batch))


	def update_dir_points(self):
		self.dir_points[0] = [self.x + 3000 * math.cos(math.radians(self.angle)), self.y + 3000 * math.sin(math.radians(self.angle))]
		self.dir_points[1] = [self.x + 3000 * math.cos(math.radians(self.angle) - math.pi / 2), self.y + 3000 * math.sin(math.radians(self.angle) - math.pi / 2)]
		self.dir_points[2] = [self.x + 3000 * math.cos(math.radians(self.angle) + math.pi / 2), self.y + 3000 * math.sin(math.radians(self.angle) + math.pi / 2)]
		self.dir_points[3] = [self.x + 3000 * math.cos(math.radians(self.angle) - math.pi / 3), self.y + 3000 * math.sin(math.radians(self.angle) - math.pi / 3)]
		self.dir_points[4] = [self.x + 3000 * math.cos(math.radians(self.angle) + math.pi / 3), self.y + 3000 * math.sin(math.radians(self.angle) + math.pi / 3)]
		self.dir_points[5] = [self.x + 3000 * math.cos(math.radians(self.angle) - math.pi / 8), self.y + 3000 * math.sin(math.radians(self.angle) - math.pi / 8)]
		self.dir_points[6] = [self.x + 3000 * math.cos(math.radians(self.angle) + math.pi / 8), self.y + 3000 * math.sin(math.radians(self.angle) + math.pi / 8)]
		for i in range(len(self.dir_points)):
			dir_len = dist(self.x, self.y, self.dir_points[i][0], self.dir_points[i][1])
			for j in self.lines:
				tmp_p = getCollisionPoint(self.x, self.y, self.dir_points[i][0], self.dir_points[i][1], j.x, j.y, j.x2, j.y2)
				if tmp_p:
					tmp_l = dist(self.x, self.y, tmp_p[0], tmp_p[1])
				else:
					tmp_l = 4000
				if tmp_l < dir_len:
					dir_len = tmp_l
					self.dir_points[i][0] = tmp_p[0]
					self.dir_points[i][1] = tmp_p[1]
			self.lengthes[i] = dir_len

	def update_directions(self):
		self.directions[0] = (shapes.Line(self.x, self.y, self.dir_points[0][0], self.dir_points[0][1], width=1, batch=self.batch))
		self.directions[1] = (shapes.Line(self.x, self.y, self.dir_points[1][0], self.dir_points[1][1], width=1, batch=self.batch))
		self.directions[2] = (shapes.Line(self.x, self.y, self.dir_points[2][0], self.dir_points[2][1], width=1, batch=self.batch))
		self.directions[3] = (shapes.Line(self.x, self.y, self.dir_points[3][0], self.dir_points[3][1], width=1, batch=self.batch))
		self.directions[4] = (shapes.Line(self.x, self.y, self.dir_points[4][0], self.dir_points[4][1], width=1, batch=self.batch))
		self.directions[5] = (shapes.Line(self.x, self.y, self.dir_points[5][0], self.dir_points[5][1], width=1, batch=self.batch))
		self.directions[6] = (shapes.Line(self.x, self.y, self.dir_points[6][0], self.dir_points[6][1], width=1, batch=self.batch))


	def check_collisions(self):
		if self.lengthes[0] < 73 or self.lengthes[1] < 25 or self.lengthes[2] < 25 or self.lengthes[3] < 27 or self.lengthes[4] < 27 or self.lengthes[5] < 60 or self.lengthes[6] < 60:
			self.reset_car()


	def apply_acc(self):

		self.speed += self.acc
		if self.speed > self.velocity:
			self.speed = self.velocity


	def apply_resist(self):

		self.speed -= self.resist + self.stoping * self.stop_acc
		if self.speed < 0:
			self.speed = 0


	def apply_left_rot(self):

		self.rot_speed += self.rot_acc
		if self.rot_speed > self.rot_velocity:
			self.rot_speed = self.rot_velocity


	def apply_right_rot(self):

		self.rot_speed -= self.rot_acc
		if self.rot_speed < self.rot_velocity:
			self.rot_speed = self.rot_velocity


	def apply_no_rot(self):

		if self.rot_speed < 0:
			self.rot_speed += self.rot_acc
			if self.rot_speed > 0:
				self.rot_speed = 0
		elif self.rot_speed > 0:
			self.rot_speed -= self.rot_acc
			if self.rot_speed < 0:
				self.rot_speed = 0




	def on_key_press(self, symbol, modifiers):

		if symbol == key.SPACE:
			self.moving = True

		if symbol == key.W:
			self.stoping = True
		
		if symbol == key.ESCAPE:
			self.close()

		if symbol == key.LEFT:
			self.left_rotating = True
			self.right_rotating = False

		if symbol == key.RIGHT:
			self.left_rotating = False
			self.right_rotating = True

		if symbol == key.L:
			for i in self.lines:
				print("self.lines.append(shapes.Line(%d, %d, %d, %d, width=1, batch=self.batch))"%(i.x, i.y, i.x2, i.y2))


	def on_close(self):
		self.close()


	def on_key_release(self, symbol, modifiers):

		if symbol == key.W:
			self.stoping = False

		if symbol == key.RIGHT:
			self.right_rotating = False

		if symbol == key.LEFT:
			self.left_rotating = False

		if symbol == key.SPACE:
			self.moving = False


	def on_mouse_press(self, x, y, button, modifiers):

		if button == mouse.RIGHT:
			self.tmp_x = -1
			self.tmp_y = -1

		if button == mouse.LEFT:
			if self.tmp_x == -1:
				self.tmp_x = x
				self.tmp_y = y
			else:
				self.lines.append(shapes.Line(self.tmp_x , self.tmp_y, x, y, width=1, batch=self.batch))
				self.tmp_x = x
				self.tmp_y = y
		
		if button == mouse.MIDDLE:
			self.x = x
			self.y = y
			print("x:", x, "y", y)



	def on_draw(self):

		window.clear()
		self.car.draw()
		self.batch.draw()


	def update(self, dt):
		self.check_collisions()
		self.update_dir_points()
		self.update_directions()

		if self.moving:
			self.apply_acc()

		if self.left_rotating:
			self.apply_left_rot()
		elif self.right_rotating:
			self.apply_right_rot()
		else:
			self.apply_no_rot()

		if self.speed > 0:
			if self.left_rotating:
				self.angle += self.rot_speed * self.speed

			if self.right_rotating:
				self.angle -= self.rot_speed  * self.speed
			self.x += math.cos(math.radians(self.angle)) * self.speed
			self.y += math.sin(math.radians(self.angle)) * self.speed

		self.apply_resist()

		self.car.update(x=self.x, y=self.y, rotation=-self.angle)



window = MyWindow(1600, 900, "AI Learns to Drive", resizable=False)
pyglet.clock.schedule_interval(window.update, 1 / 60.)
pyglet.app.run()