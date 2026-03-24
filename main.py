import pygame

from game import ALTURA, LARGURA, PongGame


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pong")

    game = PongGame(tela)
    game.run()


if __name__ == "__main__":
    main()