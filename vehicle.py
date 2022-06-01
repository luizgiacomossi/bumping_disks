import pygame as pg
import random
import math

class Vector3():
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def length(self) -> float:
            return math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))
    
    def normalize(self) -> 'Node':
        if self.length() == 0:
            return Vector3(0, 0, 0)
        else:
            return Vector3(self.x / self.length(), self.y / self.length(), self.z / self.length())

    def dot(self, other: 'Node') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Node') -> 'Node':
        return Vector3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def __mul__(self, other: 'Node') -> 'Node':
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __mul__(self, other: float) -> 'Node':
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __neg__(self) -> 'Node':
        return Vector3(-self.x, -self.y, -self.z)

    def __truediv__(self, other: 'Node') -> 'Node':
        return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __truediv__(self, other: float) -> 'Node':
        return Vector3(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other: 'Node') -> 'Node':
        return Vector3(self.x // other.x, self.y // other.y, self.z // other.z)

    def __mod__(self, other: 'Node') -> 'Node':
        return Vector3(self.x % other.x, self.y % other.y, self.z % other.z)

    def __pow__(self, other: 'Node') -> 'Node':
        return Vector3(self.x ** other.x, self.y ** other.y, self.z ** other.z)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def __eq__(self, other: 'Node') -> bool:
        return self.node_name == other.node_name and self.position == other.position
    
    def __hash__(self) -> int:
        return hash((self.node_name, self.position))    
    
    def __lt__(self, other: 'Node') -> bool:
        return self.node_name < other.node_name
    
    def __gt__(self, other: 'Node') -> bool:
        return self.node_name > other.node_name

    def __eq__(self, other: 'Node') -> bool:
        return self.node_name == other.node_name and self.position == other.position

    def distance(self, other: 'Node') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
    # summation handler 
    def __add__(self, other: 'Node') -> 'Node':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Node') -> 'Node':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

class Vehicle():
    def __init__(self, node_name: str, position: Vector3) -> None:
        self.node_name = node_name
        self.position = position
        self.attitude = Vector3(0,0,0)
        # randomize the velocity FLOAT
        self.velocity = Vector3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector3(0,0,0)
        self.force = Vector3(0,0,0)
        self.mass = random.randint(1, 50)
        self.radius = random.randint(10, 25)
        self.max_speed = 1
        self.max_force = 1

        # random color
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def update(self, dt: float) -> None:
        
        # f = m * a
        self.acceleration = self.force / self.mass
        # v = u + at
        self.velocity += self.acceleration * dt
        #self.velocity -= self.velocity * 0.005
        # x = ut + 1/2at^2
        self.position += self.velocity * dt + self.acceleration * dt ** 2 / 2
        self.position.z = 0
        # reset force
        self.force = Vector3(0,0,0)

    def apply_force(self, force: Vector3) -> None:
        self.force += force

    def draw(self, canvas: 'Canvas') -> None:
        pg.draw.circle(canvas, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        # draw the attitude as a line
        ini = (int(self.position.x), int(self.position.y))
        # proporcional to velocity
        end = (int(self.position.x + self.velocity.x * 10), int(self.position.y + self.velocity.y * 10))
        pg.draw.line(canvas, (0, 0, 0), ini , end , 1)

    def __str__(self) -> str:
        return f'{self.node_name} at {self.position}'
    
    def __repr__(self) -> str:
        return f'{self.node_name} at {self.position}'

    def __eq__(self, other: 'Vehicle') -> bool:
        return self.node_name == other.node_name 