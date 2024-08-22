import os
from ursina import *
from random import randint

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.parent = field                 # 사과 먹기 게임
        self.model = "cube"
        self.color = color.black
        self.scale = .05
        self.position = (0, 0,-0.03)
        self.collider = "box"
        self.dx = 0
        self.dy = 0
        self.eaten = 0
    def update(self):
        global body, text
        self.x += time.dt * self.dx
        self.y += time.dt * self.dy

        hit_info = self.intersects()

        if hit_info.hit:
            self.eaten +=1
            text.y = -1
            text = Text(text = f'Apple eaten: {self.eaten}', position = (0, 0.3, 3), origin = (0, 0), scale = 1.5, color = color.red, background = True)

            apple.x = randint(-4, 4) * 0.1
            apple.y = randint(-4, 4) * 0.1
            new_body = Entity(parent=field, model="cube", z=-0.29, color=color.green, scale=0.05)
            body.append(new_body)

        for i in range(len(body) - 1, 0, -1):
            body[i].position = body[i - 1].position
        if len(body) > 0:
            body[0].x = self.x
            body[0].y = self.y

        if abs(self.x) > 0.47 or abs(self.y) > 0.47:
            for segment in body:
                segment.position = (10, 10)
            body = []

            print_on_screen("You crashed !!", position = (0, 0), origin = (0, 0), scale = 2, duration = 2)
            self.position = (0, 0)
            self.dx = 0
            self.dy = 0
            self.eaten = 0
            text.y = -1
            text = Text(text=f'Apple eaten: {self.eaten}', position=(0, 0.3, 3), origin=(0, 0), scale=1.5,
                        color=color.red, background=True)

    def input(self, key):
        if key == "right arrow":
            self.dx = 0.3
            self.dy = 0
        if key == "left arrow":
            self.dx = -0.3
            self.dy = 0
        if key == "up arrow":
            self.dx = 0
            self.dy = 0.3
        if key == "down arrow":
            self.dx = 0
            self.dy = -0.3

app = Ursina()

Entity(model = "quad", scale = 60, texture = None)
field_size = 19

field = Entity(model = "quad", scale = (12, 12), color = color.gray, position = (field_size // 2, field_size // 2, -.01))
camera.position = (field_size //2 , -18, -18)
camera.rotation_x = -56
apple = Entity(parent = field, model = "sphere", color = color.red, scale = 0.05, position = (.1, .1, -.03), collider = "box")
player = Player()
body = []
text = Text(text= "")

app.run()
