import pygame
import random
import time
import math


class Collectible:
    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = self.sprite.get_rect()

        self.velocity = [0.7, 0.7]  # Initial velocity for x and y directions
        # self.acceleration = 0.001  # Adjust this value to control acceleration

    def update(self) -> None:

        # Introduce a chance to change direction
        if random.random() < 0.002:  # Adjust this value to control the chance of direction change
            self.velocity[0] *= random.choice([-1, 1])
            self.velocity[1] *= random.choice([-1, 1])

        self.x += self.velocity[0]
        self.y += self.velocity[1]

        self.x = max(0, min(1280 - self.sprite.get_width(), self.x))
        self.y = max(0, min(720 - self.sprite.get_height(), self.y))

        # Reverse velocity when approaching edges
        if self.x <= 0 or self.x >= 1280 - self.sprite.get_width():
            self.velocity[0] *= -1
        if self.y <= 0 or self.y >= 720 - self.sprite.get_height():
            self.velocity[1] *= -1

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


# Speed collectibles up as more picked up
        # self.velocity[0] += random.uniform(-self.acceleration,
        #                                    self.acceleration)
        # self.velocity[1] += random.uniform(-self.acceleration,
        #                                    self.acceleration)

        # # Limit the velocity to prevent excessive speed
        # max_velocity = 2.0
        # self.velocity[0] = min(
        #     max_velocity, max(-max_velocity, self.velocity[0]))
        # self.velocity[1] = min(
        #     max_velocity, max(-max_velocity, self.velocity[1]))

        # self.x += self.velocity[0]
        # self.y += self.velocity[1]

        # self.x = max(0, min(1280 - self.sprite.get_width(), self.x))
        # self.y = max(0, min(720 - self.sprite.get_height(), self.y))

        # # Reverse velocity when approaching edges
        # if self.x <= 0 or self.x >= 1280 - self.sprite.get_width():
        #     self.velocity[0] *= -1
        # if self.y <= 0 or self.y >= 720 - self.sprite.get_height():
        #     self.velocity[1] *= -1

        # self.rect.x = int(self.x)
        # self.rect.y = int(self.y)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))

    def randomize_position(self) -> None:
        self.x = random.randint(50, 1250)
        self.y = random.randint(50, 670)
        self.rect.x = self.x
        self.rect.y = self.y


class Player:
    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.sprite = sprite
        self.velocity = 300
        self.angle = 0
        self.direction = "up"
        self.moving = False
        self.rect = self.sprite.get_rect()
        self.shooting = False
        self.shoot_cooldown = 0.1  # Adjust the cooldown time as needed
        self.last_shot_time = 0
        self.bullets = []
        print(self.bullets)

    def update(self, dt) -> None:
        if self.moving:
            self.move(dt)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.shooting and time.time() - self.last_shot_time > self.shoot_cooldown:
            self.shoot()
            self.last_shot_time = time.time()

        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.x < 0 or bullet.x > 1280 or bullet.y < 0 or bullet.y > 720:
                self.bullets.remove(bullet)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))

    def set_angle(self, new_angle: int) -> None:
        rotation = new_angle - self.angle
        self.sprite = pygame.transform.rotate(self.sprite, rotation)
        self.angle = new_angle

    def move(self, dt) -> None:
        if self.direction == "up":
            self.y -= self.velocity * dt
        elif self.direction == "down":
            self.y += self.velocity * dt
        elif self.direction == "left":
            self.x -= self.velocity * dt
        elif self.direction == "right":
            self.x += self.velocity * dt

        self.x = min((1236, self.x))
        self.x = max((0, self.x))

        self.y = min((680, self.y))
        self.y = max((0, self.y))

    def shoot(self) -> None:
        bullet_offset = 30
        ship_center_x = self.x + self.sprite.get_width() / 2.5
        ship_center_y = self.y + self.sprite.get_height() / 2.5

        # Adjust bullet offset for different directions
        if self.angle == 0:  # Up
            bullet_x = ship_center_x
            bullet_y = ship_center_y - bullet_offset
        elif self.angle == 90:  # Left
            bullet_x = ship_center_x - bullet_offset
            bullet_y = ship_center_y
        elif self.angle == 180:  # Down
            bullet_x = ship_center_x
            bullet_y = ship_center_y + bullet_offset
        elif self.angle == 270:  # Right
            bullet_x = ship_center_x + bullet_offset
            bullet_y = ship_center_y
        else:  # Other angles
            angle_radians = math.radians(self.angle)
            bullet_x = ship_center_x + bullet_offset * math.cos(angle_radians)
            bullet_y = ship_center_y - bullet_offset * math.sin(angle_radians)

        bullet = Bullet(bullet_x, bullet_y, self.angle)
        self.bullets.append(bullet)


class Bullet:
    def __init__(self, x: float, y: float, angle: float) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 500  # Adjust the bullet speed as needed
        self.sprite = pygame.Surface((8, 8))
        self.rect = self.sprite.get_rect()
        self.sprite.fill((255, 255, 0))  # Yellow color
        self.damage = 1  # Adjust damage as needed

    def update(self, dt) -> None:
        self.x += self.speed * math.cos(math.radians(self.angle + 90)) * dt
        self.y -= self.speed * math.sin(math.radians(self.angle + 90)) * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))


class Text:
    def __init__(self, x, y, text: str) -> None:
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont("Calibri", 36)

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        self.rendered = self.font.render(self.text, True, "white")
        screen.blit(self.rendered, (self.x, self.y))


class Asteroid:
    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:
        self.sprite = sprite
        self.x = random.choice([-self.sprite.get_width(), 1280])
        self.y = random.uniform(0, 720 - self.sprite.get_height())
        self.velocity = [random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)]
        self.rect = self.sprite.get_rect()
        self.hits = 0

    def destroyed(self) -> bool:
        return self.hits >= 1

    def update(self) -> None:
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        self.x = max(0, min(1280 - self.sprite.get_width(), self.x))
        self.y = max(0, min(720 - self.sprite.get_height(), self.y))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.x <= 0 or self.x >= 1280 - self.sprite.get_width():
            self.velocity[0] *= -1
        if self.y <= 0 or self.y >= 720 - self.sprite.get_height():
            self.velocity[1] *= -1

    def reset(self) -> None:
        self.x = random.randint(0, 1280 - self.sprite.get_width())
        self.y = random.randint(0, 720 - self.sprite.get_height())
        self.velocity = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))


class GameOverScreen:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.restart_button = pygame.Rect(500, 400, 200, 50)
        self.font = pygame.font.SysFont("Calibri", 48)

    def render(self):
        self.screen.fill("black")
        score_text = self.font.render(f"Score: {self.score}", True, "white")
        restart_text = self.font.render("Restart", True, "white")
        self.screen.blit(score_text, (500, 300))
        pygame.draw.rect(self.screen, "green", self.restart_button)
        self.screen.blit(restart_text, (530, 405))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.collidepoint(event.pos):
                    return True
        return False


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.lives = 3  # Initial lives count
        self.collided_this_frame = False
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprites = self.load_sprites()
        self.lives_sprites = [self.sprites["life"] for _ in range(self.lives)]
        self.score = 0
        self.asteroids = []
        self.asteroid_spawn_timer = 0
        self.asteroid_spawn_interval = 3  # Adjust the interval as needed

        self.player = Player(200, 200, self.sprites["spaceship"])

        self.collectible = Collectible(500, 500, self.sprites["collectible"])
        self.collectible.randomize_position()
        self.text = Text(600, 50, str(self.score))

        self.keybinds = {pygame.K_w: (0, "up"),
                         pygame.K_d: (270, "right"),
                         pygame.K_s: (180, "down"),
                         pygame.K_a: (90, "left")}

        pygame.mixer.music.load("sfx/music.ogg")
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play()

        self.collect_sound = pygame.mixer.Sound("sfx/collect.wav")
        self.collect_sound.set_volume(0.5)

        self.create_initial_asteroids()

    def create_initial_asteroids(self) -> None:
        for _ in range(5):  # Create 5 initial asteroids
            asteroid = Asteroid(random.randint(100, 500 - self.sprites["asteroid"].get_width()),
                                random.randint(
                                    0, 720 - self.sprites["asteroid"].get_height()),
                                self.sprites["asteroid"])
            self.asteroids.append(asteroid)

    def poll_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key in self.keybinds:
                self.player.set_angle(self.keybinds[event.key][0])
                self.player.direction = self.keybinds[event.key][1]
                self.player.moving = True

            if event.type == pygame.KEYUP and event.key in self.keybinds:
                if self.keybinds[event.key][1] == self.player.direction:
                    self.player.moving = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.shooting = True

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.player.shooting = False

    def update(self) -> None:
        # Compute delta time
        now = time.time()
        dt = now - self.previous_time
        self.previous_time = now
        self.collided_this_frame = False  # Reset the flag
        self.player.update(dt)
        self.collectible.update()

        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.randomize_position()
            self.player.velocity += 100
            self.collect_sound.play()
            self.score += 1
            # Adjust the asteroid spawn interval based on the score
            self.asteroid_spawn_interval -= 0.2  # Decrease the interval
            self.asteroid_spawn_interval = max(
                0.5, self.asteroid_spawn_interval)  # Cap the intervals

        for bullet in self.player.bullets:
            if bullet.rect.colliderect(self.collectible.rect):
                self.collectible.randomize_position()
                self.player.bullets.remove(bullet)
                self.collect_sound.play()
                self.score += 1

        # Use a copy to iterate and remove safely
        for bullet in self.player.bullets[:]:
            # Use a copy to iterate and remove safely
            for asteroid in self.asteroids[:]:
                if bullet.rect.colliderect(asteroid.rect):
                    asteroid.hits += bullet.damage
                    self.player.bullets.remove(bullet)
                    if asteroid.destroyed():
                        self.asteroids.remove(asteroid)
                    break  # Break the inner loop as the bullet hit an asteroid

        # for asteroid in self.asteroids:
        #     asteroid.update()

        #     # Check collision with asteroids
        #     if self.player.rect.colliderect(asteroid.rect):
        #         self.lives -= 1
        #         if self.lives == 0:
        #             self.running = False
        #         else:
        #             self.player.x = 200
        #             self.player.y = 200
        #             self.lives_sprites.pop()  # Remove a life sprite

        #         # Check bullet-asteroid collisions

        # Use a copy to iterate and remove safely
        for asteroid in self.asteroids[:]:
            asteroid.update()

            # Check collision with asteroids
            if self.player.rect.colliderect(asteroid.rect) and not self.collided_this_frame:
                self.lives -= 1
                if self.lives == 0:
                    self.running = False
                else:
                    self.player.x = 200
                    self.player.y = 200
                    self.lives_sprites.pop()  # Remove a life sprite
                self.collided_this_frame = True  # Set the flag

            if asteroid.destroyed():
                self.asteroids.remove(asteroid)
                new_asteroid = Asteroid(
                    random.randint(0, 1280 - asteroid.sprite.get_width()),
                    random.randint(0, 720 - asteroid.sprite.get_height()),
                    self.sprites["asteroid"]
                )
                self.asteroids.append(new_asteroid)

        self.asteroid_spawn_timer += dt
        if self.asteroid_spawn_timer >= self.asteroid_spawn_interval:
            new_asteroid = Asteroid(
                random.randint(0, 1280 - self.sprites["asteroid"].get_width()),
                random.randint(0, 720 - self.sprites["asteroid"].get_height()),
                self.sprites["asteroid"]
            )
            self.asteroids.append(new_asteroid)
            self.asteroid_spawn_timer = 0
        self.text.update()
        self.text.text = str(self.score)

    def render(self) -> None:
        self.screen.fill("black")

        self.screen.blit(self.sprites["background"], (0, 0))
        self.player.render(self.screen)
        self.collectible.render(self.screen)

        for bullet in self.player.bullets:
            bullet.render(self.screen)

        for asteroid in self.asteroids:  # Render the asteroids here
            asteroid.render(self.screen)

        # Render lives sprites
        lives_x = 3
        for life_sprite in self.lives_sprites:
            self.screen.blit(life_sprite, (lives_x, 3))
            lives_x += life_sprite.get_width() + 5

        self.text.render(self.screen)

        pygame.display.update()

    def run(self) -> None:
        self.previous_time = time.time()
        while self.running:
            self.poll_events()
            self.update()
            self.render()
        pygame.quit()

    def load_sprites(self) -> dict:
        sprites = {}

        sprites["spaceship"] = pygame.image.load(
            "gfx/ship.png").convert_alpha()
        sprites["background"] = pygame.image.load(
            "gfx/simple_game_bg.png").convert_alpha()
        sprites["collectible"] = pygame.image.load(
            "gfx/collectible.png").convert_alpha()
        sprites["asteroid"] = pygame.image.load(
            "gfx/asteroid.png").convert_alpha()
        sprites["asteroid"] = pygame.transform.scale(
            sprites["asteroid"], (48, 48))
        # Downscale
        sprites["spaceship"] = pygame.transform.scale(
            sprites["spaceship"], (48, 48))

        sprites["life"] = pygame.image.load("gfx/life.png").convert_alpha()
        sprites["life"] = pygame.transform.scale(
            sprites["life"], (32, 32))  # Adjust size as needed

        return sprites


g = Game()
g.run()
