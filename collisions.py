from turtle import distance
import pygame as pg
from math import atan2, pi, exp
import random
import copy 
from vehicle import Vehicle
from vehicle import Vector3
import sys

FREQUENCY_OF_UPDATE = 60
SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 600
SCREEN_SIZE = (SCREEN_SIZE_X, SCREEN_SIZE_Y)
NUM_PARTICLES = 30
LINES = False

class Screen():
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
        # resizable window set mode
        self.screen_size = SCREEN_SIZE

        pg.display.set_caption("Collision Avoidance")

        pg.display.flip()

        self.clock = pg.time.Clock()
        self.vehicles = []

        for i in range(NUM_PARTICLES):
            name = "vehicle" + str(i+1)
            position = Vector3(random.randint(0,SCREEN_SIZE_X),random.randint(0,SCREEN_SIZE_Y), 0)
            self.vehicles.append(Vehicle(name, position))
            print(self.vehicles[i].node_name, self.vehicles[i].position)

        # create a collision avoidance object
        self.collision = Collision(self.vehicles)

    def run(self) -> None:
        while True:
            self.update()
            self.draw()
            self.clock.tick(FREQUENCY_OF_UPDATE)

                            # read input 
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
                if event.type == pg.VIDEORESIZE:
                    self.screen = pg.display.set_mode(event.dict['size'], pg.RESIZABLE)
                    # get new size
                    self.screen_size = event.dict['size']

    def update(self) -> None:
        self.memory_collisions = []
        for vehicle in self.vehicles:
            self.check_vehicle_collision(vehicle)

        for i in range(len(self.vehicles)):
            self.vehicles[i].update(1)


        for i in range(len(self.vehicles)):
            self.check_vehicle_inside_screen(self.vehicles[i])

    def draw(self) -> None:
        self.screen.fill((100,100,100))

        # draw line between vehicles
        if LINES:
            for i in range(len(self.vehicles)):
                for j in range(i+1, len(self.vehicles)):
                    ini_pos = (self.vehicles[i].position.x, self.vehicles[i].position.y)
                    end_pos = (self.vehicles[j].position.x, self.vehicles[j].position.y )
                    pg.draw.line(self.screen, self.vehicles[i].color , ini_pos, end_pos, 1)

        for i in range(len(self.vehicles)):
            self.vehicles[i].draw(self.screen)

        pg.display.flip()

    def check_vehicle_collision(self, vehicle):
        for other_vehicle in self.vehicles:
            if vehicle.node_name != other_vehicle.node_name:
                distance = vehicle.position.distance(other_vehicle.position)
                # print positions and distance
                if distance <= (vehicle.radius + other_vehicle.radius) and vehicle.node_name not in self.memory_collisions:
                    #print(f"collision: {vehicle.node_name} and {other_vehicle.node_name}")
                    # invert velocity
                    v1, v2 = self.collision.elastic_collision(vehicle, other_vehicle)
                    vehicle.velocity = v1
                    other_vehicle.velocity = v2
                    # add to memory
                    self.memory_collisions.append(vehicle.node_name)
                    self.memory_collisions.append(other_vehicle.node_name)

    def check_vehicle_inside_screen(self, vehicle):
        if vehicle.position.x > self.screen_size[0] - vehicle.radius:
            vehicle.position.x = self.screen_size[0] - vehicle.radius
            vehicle.velocity.x = -vehicle.velocity.x
        if vehicle.position.x < 0 + vehicle.radius:
            vehicle.position.x = 0  + vehicle.radius
            vehicle.velocity.x = -vehicle.velocity.x
        if vehicle.position.y > self.screen_size[1]  - vehicle.radius:
            vehicle.position.y = self.screen_size[1]  - vehicle.radius
            vehicle.velocity.y = -vehicle.velocity.y
        if vehicle.position.y < 0 + vehicle.radius:
            vehicle.position.y = 0 + vehicle.radius
            vehicle.velocity.y = -vehicle.velocity.y

class Collision():
    def __init__(self, list_vehicles = None ) -> None:
        self.vehicles = list_vehicles
        # parameters
        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.radius = 3

    def calculate_velocity(self, vehicle, other_vehicle, dt = FREQUENCY_OF_UPDATE) -> Vector3:
        # calculate the position of the collision
        new_velocity = other_vehicle.velocity - vehicle.velocity
        new_velocity.normalize()
        new_velocity *= other_vehicle.velocity.length()

        other_vehicle.velocity = new_velocity
        vehicle.velocity = -new_velocity

        # update the position of the vehicles
        other_vehicle.position += other_vehicle.velocity * dt
        vehicle.position += vehicle.velocity * dt

        return other_vehicle.velocity

    def elastic_collision(self, vehicle1, vehicle2):
        # calculate the position of the collision
        # m1.v1 + m2.v2 ini = m1.v1 + m2.v2 end
        m1 = vehicle1.mass
        m2 = vehicle2.mass
        v1 = vehicle1.velocity
        v2 = vehicle2.velocity

        # calculate the new velocity of the vehicles
        v1_ = v1*(m1 - m2)/(m1+m2) + v2*(2*m2)/(m1+m2)
        v2_ = v1*(2*m1)/(m1+m2) + v2*(m2 - m1)/(m1+m2)


        return v1_, v2_



if __name__ == "__main__":
    pg.init()
    screen = Screen()
    screen.run()




