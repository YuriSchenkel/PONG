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
        self.win_score = 2

        self.p1 = Paddle(15, ALTURA // 2 - 30)
        self.p2 = Paddle(LARGURA - 25, ALTURA // 2 - 30)

        self.ball = Ball()
        self.score = Score()

    def resetar_partida(self):
        self.p1.rect.y = ALTURA // 2 - 30
        self.p2.rect.y = ALTURA // 2 - 30
        self.ball.reset()
        self.score = Score()

    def menu_principal(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.quit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    return

            self.tela.fill(PRETO)

            font_titulo = pygame.font.SysFont(None, 72)
            titulo = font_titulo.render("Pong", True, BRANCO)
            titulo_rect = titulo.get_rect(center=(LARGURA // 2, ALTURA // 3))
            self.tela.blit(titulo, titulo_rect)

            font_info = pygame.font.SysFont(None, 30)
            tempo = pygame.time.get_ticks()
            if tempo % 2000 < 1000:
                info = font_info.render("Pressione ESPACO para jogar", True, BRANCO)
                info_rect = info.get_rect(center=(LARGURA // 2, ALTURA // 2))
                self.tela.blit(info, info_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    def mostrar_vencedor(self, vencedor):
        fonte = pygame.font.SysFont(None, 52)
        texto = fonte.render(f"Player {vencedor} venceu!", True, BRANCO)
        texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))

        self.tela.fill(PRETO)
        self.tela.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

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

        if self.score.p1 >= self.win_score:
            self.mostrar_vencedor(1)
            self.resetar_partida()
            return True

        if self.score.p2 >= self.win_score:
            self.mostrar_vencedor(2)
            self.resetar_partida()
            return True

        return False

    def draw(self):
        self.tela.fill(PRETO)

        self.p1.draw(self.tela)
        self.p2.draw(self.tela)
        self.ball.draw(self.tela)
        self.score.draw(self.tela)

        pygame.display.flip()

    def run(self):
        while True:
            self.menu_principal()
            self.resetar_partida()

            while True:
                self.events()
                if self.update():
                    break
                self.draw()
                self.clock.tick(FPS)

    def quit(self):
        pygame.quit()
        sys.exit()