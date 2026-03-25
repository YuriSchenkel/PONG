import pygame
import random
import sys
import os

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
    _CORES_FAKE = [
        (255, 80, 80), (80, 255, 80), (80, 180, 255),
        (255, 220, 50), (255, 100, 255), (100, 255, 220),
    ]

    def __init__(self, x=None, y=None, vx=None, vy=None, real=True):
        self.size = 7
        self.speed_x = 5
        self.max_vertical_speed = 8
        self.reset()
        self.real = real
        self.cor = BRANCO if real else random.choice(Ball._CORES_FAKE)
        if x is not None:
            self.x, self.y, self.vx, self.vy = x, y, vx, vy
        else:
            self.reset()

    def reset(self):
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        self.vx = random.choice((-self.speed_x, self.speed_x))
        self.vy = random.choice((-4, -3, 3, 4))

    def aplicar_variacao_vertical(self):
        self.vy += random.randint(-2, 2)

        if abs(self.vy) < 2:
            self.vy = random.choice((-2, 2))

        self.vy = max(-self.max_vertical_speed, min(self.vy, self.max_vertical_speed))

    def rebater_parede(self):
        self.vy *= -1
        self.aplicar_variacao_vertical()
        self.vx += random.choice((-1, 0, 1))

        if abs(self.vx) < self.speed_x:
            self.vx = self.speed_x if self.vx >= 0 else -self.speed_x

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.y - self.size <= 0:
            self.y = self.size
            self.rebater_parede()

        if self.y + self.size >= ALTURA:
            self.y = ALTURA - self.size
            self.rebater_parede()

    def rebater_raquete(self, paddle):
        offset = (self.y - paddle.rect.centery) / (paddle.rect.height / 2)
        offset = max(-1.0, min(1.0, offset))
        self.vy = offset * self.max_vertical_speed
        if abs(self.vy) < 1.5:
            self.vy = random.choice((-1.5, 1.5))
        self.vy += random.uniform(-1.0, 1.0)
        self.vy = max(-self.max_vertical_speed, min(self.vy, self.max_vertical_speed))

    def collide(self, p1, p2, som_bate=None):
        rect = pygame.Rect(
            self.x - self.size,
            self.y - self.size,
            self.size * 2,
            self.size * 2,
        )
        colidiu = False

        if rect.colliderect(p1.rect) and self.vx < 0:
            self.x = p1.rect.right + self.size
            self.vx = abs(self.vx)
            self.rebater_raquete(p1)
            colidiu = True

        if rect.colliderect(p2.rect) and self.vx > 0:
            self.x = p2.rect.left - self.size
            self.vx = -abs(self.vx)
            self.rebater_raquete(p2)
            colidiu = True

        if colidiu and som_bate:
            som_bate.play()

        return colidiu

    def draw(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.size)


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
        self.win_score = 10

        self.p1 = Paddle(15, ALTURA // 2 - 30)
        self.p2 = Paddle(LARGURA - 25, ALTURA // 2 - 30)

        self.bolas = [Ball()]
        self.score = Score()
        self.ultimo_fragmento = 0

        base_path = os.path.dirname(__file__)
        try:
            self.som_bate = pygame.mixer.Sound(
                os.path.join(base_path, "sounds", "batida.mp3")
            )
            self.som_gol = pygame.mixer.Sound(
                os.path.join(base_path, "sounds", "gol.mp3")
            )
            self.som_bate.set_volume(0.3)
            self.som_gol.set_volume(0.5)
        except:
            self.som_bate = None
            self.som_gol = None

        try:
            pygame.mixer.music.load(
                os.path.join(base_path, "sounds", "musica.mp3")
            )
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass

    def resetar_partida(self):
        self.p1.rect.y = ALTURA // 2 - 30
        self.p2.rect.y = ALTURA // 2 - 30
        self.bolas = [Ball()]
        self.score = Score()
        self.ultimo_fragmento = 0

    def fragmentar(self, bola_real):
        cores = random.sample(Ball._CORES_FAKE, 3)
        for i, dvy in enumerate([-3, 3, -5]):
            fake = Ball(bola_real.x, bola_real.y, bola_real.vx, bola_real.vy + dvy, real=False)
            fake.cor = cores[i]
            self.bolas.append(fake)
        self.ultimo_fragmento = pygame.time.get_ticks()

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
        agora = pygame.time.get_ticks()
        pode_fragmentar = (agora - self.ultimo_fragmento) >= 5000
        deve_fragmentar = False
        bola_real = None
        remover = []

        for bola in self.bolas:
            bola.move()
            colidiu = bola.collide(self.p1, self.p2, self.som_bate)

            if bola.real:
                bola_real = bola
                if colidiu and pode_fragmentar:
                    deve_fragmentar = True

                if bola.x <= 0:
                    self.score.point(2)
                    if self.som_gol:
                        self.som_gol.play()
                    bola.reset()
                    remover = [b for b in self.bolas if not b.real]
                    self.ultimo_fragmento = agora
                elif bola.x >= LARGURA:
                    self.score.point(1)
                    if self.som_gol:
                        self.som_gol.play()
                    bola.reset()
                    remover = [b for b in self.bolas if not b.real]
                    self.ultimo_fragmento = agora
            else:
                if bola.x < -20 or bola.x > LARGURA + 20:
                    remover.append(bola)

        for b in remover:
            if b in self.bolas:
                self.bolas.remove(b)

        if deve_fragmentar and bola_real:
            self.fragmentar(bola_real)

        if bola_real:
            if self.p2.rect.centery < bola_real.y:
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
        for bola in self.bolas:
            bola.draw(self.tela)
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