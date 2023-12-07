import random

import pygame

"""
Ajustar para quando está big e small
"""


class Particle(pygame.sprite.Sprite):
    def __init__(self, color):
        self.particles = []
        self.color = color

    def emit(self, screen):
        # moves and draws the particles
        if self.particles:
            # before updating all the particles, delete all the particle we aren´t using
            self.delete_particles()
            # Ir buscar cada uma das particles
            for particle in self.particles:
                # move down
                particle[0][1] += particle[2][0]  # takes y position and adds direction (+1, move down)
                # move to the sides
                particle[0][0] += particle[2][1]
                # shrink
                particle[1] -= 0.2
                # draw circle arrownd the particle
                pygame.draw.circle(screen, self.color, particle[0], int(particle[1]))

    def add_particles(self, particle_x, particle_y):
        # add particles
        particle_x = particle_x + 25
        particle_y = particle_y + 100
        radius = 5
        direction_y = 3  # -1, particle go upwards
        direction_x = random.uniform(-1, 1)
        particle_circle = [[particle_x, particle_y], radius, [direction_y, direction_x]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        # removes particles after certain time
        # cycle to all particles list, but only copy particles with radius greater than zero
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        # get rid of all the particles that are getting o zero
        self.particles = particle_copy


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        # Loads  + scales + adds to list explosion images 1 by 1
        for num in range(1, 6):
            img = pygame.image.load(f"Images/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100)) # Change size of explosion here
            self.images.append(img)
        # access the first picture of image everytime we create an instance of list
        self.index = 0
        # image displaying on the screen
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        # define image center location
        self.rect.center = [x + 25, y]
        self.counter = 0

    # All changes to the image and to the animation happen here
    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.counter += 1

        # Look for what image we should be accessing
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            # moves the animation over by 1 point
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            # deletes animation instance
            self.kill()
