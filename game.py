import pygame
import sys

LARGURA = 800
ALTURA = 600
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
FPS = 60


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 60)
        self.vel = 5

    def up(self):
        if self.rect.top > 0:
            self.rect.y -= self.vel

    def down(self):
        if self.rect.bottom < ALTURA:
            self.rect.y += self.vel

    def draw(self, tela):
        pygame.draw.rect(tela, BRANCO, self.rect)


class Ball:
    def __init__(self):
        self.size = 7
        self.reset()

    def reset(self):
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        self.vx = 5
        self.vy = 5

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.y <= 0 or self.y >= ALTURA:
            self.vy *= -1

    def collide(self, p1, p2):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)

        if rect.colliderect(p1.rect) or rect.colliderect(p2.rect):
            self.vx *= -1

    def draw(self, tela):
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), self.size)


class Score:
    def __init__(self):
        self.p1 = 0
        self.p2 = 0

    def point(self, player):
        if player == 1:
            self.p1 += 1
        else:
            self.p2 += 1

    def draw(self, tela):
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"{self.p1} - {self.p2}", True, BRANCO)
        tela.blit(text, text.get_rect(center=(LARGURA // 2, 30)))


class PongGame:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()

        self.p1 = Paddle(15, ALTURA // 2 - 30)
        self.p2 = Paddle(LARGURA - 25, ALTURA // 2 - 30)

        self.ball = Ball()
        self.score = Score()

    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit()

    def update(self):
        self.ball.move()
        self.ball.collide(self.p1, self.p2)

        if self.ball.x <= 0:
            self.score.point(2)
            self.ball.reset()

        if self.ball.x >= LARGURA:
            self.score.point(1)
            self.ball.reset()

        if self.p2.rect.centery < self.ball.y:
            self.p2.down()
        else:
            self.p2.up()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.p1.up()
        if keys[pygame.K_DOWN]:
            self.p1.down()

    def draw(self):
        self.tela.fill(PRETO)

        self.p1.draw(self.tela)
        self.p2.draw(self.tela)
        self.ball.draw(self.tela)
        self.score.draw(self.tela)

        pygame.display.flip()

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def quit(self):
        pygame.quit()
        sys.exit()