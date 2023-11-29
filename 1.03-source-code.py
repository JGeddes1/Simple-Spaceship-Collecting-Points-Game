import pygame
import random


class Collectible:

    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.sprite = sprite

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))

    def randomize_position(self) -> None:
        self.x = random.randint(50, 1250)
        self.y = random.randint(50, 670)


class Player:
    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.sprite = sprite

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprites = self.load_sprites()
        self.player = Player(200, 200, self.sprites["spaceship"])
        self.collectible = Collectible(500, 500, self.sprites["collectible"])
        self.collectible.randomize_position()

    def poll_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.player.update()

    def render(self) -> None:
        self.screen.fill('black')

        self.screen.blit(self.sprites["background"], (0, 0))
        self.player.render(self.screen)
        self.collectible.render(self.screen)
        pygame.display.update()

    def run(self) -> None:
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

        # Donwscale
        sprites["spaceship"] = pygame.transform.scale(
            sprites["spaceship"], (50, 50))

        return sprites


g = Game()
g.run()
