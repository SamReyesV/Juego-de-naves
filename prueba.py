import pygame, sys
from nave import Nave
from bala import Bullet
from Aliens import Alien


# clase de pantalla
class GalagaPirata:
    def __init__(self):
        pygame.init()
        self.ancho = 800
        self.alto = 500
        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Galaga Pirata")
        self.color = (230, 230, 230)
        self.nave = Nave(self)
        self.velocidad = 1
        self.anchobala = 3
        self.altobala = 15
        self.colorbala = (255, 0, 0)
        self.nave = Nave(self)
        self.bullets = pygame.sprite.Group()
        self.balas_totales = 3
        self.aliens = pygame.sprite.Group()
        self.velocidad_Alien = 1.0
        self.flota_velocidad = 10
        self.flota_direccion = 1
        self._create_fleet()

    # Funcion del loop
    def corre_juego(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = True
                    if event.key == pygame.K_LEFT:
                        self.nave.mover_izquieda = True
                    if event.key == pygame.K_SPACE:
                        self._fire_bullet()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = False
                    if event.key == pygame.K_LEFT:
                        self.nave.mover_izquieda = False

            self.nave.mover()
            self.screen.fill(self.color)
            self.nave.corre()
            self.bullets.update()
            self.update_Alien()

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            pygame.display.flip()

    def _fire_bullet(self):
        if self.balas_totales != 0:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.balas_totales = self.balas_totales - 1

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        availableSpace = self.ancho - ( 2 * alien_width)
        numerodeAliens = availableSpace // ( 2* alien_width)
        nave_heigth = self.nave.rect.height
        availableSpacey = self.alto - (3* alien_height) - nave_heigth
        numerodeFilas = availableSpacey // (2 * alien_height)

        for fila in range(numerodeFilas):
            for numeroAlien in range(numerodeAliens):
                self._create_alien(numeroAlien, fila)

    def _create_alien(self, numeroAlien, fila):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * numeroAlien
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * fila
        self.aliens.add(alien)

    def update_Alien(self):
        self.checa_bordesFlota()
        self.aliens.update()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def checa_bordesFlota(self):
        for Alien in self.aliens.sprites():
            if Alien.checa_bordes():
                self.cambia_direccion()
                break

    def cambia_direccion(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.flota_velocidad
        self.flota_direccion *= -1


if __name__ == "__main__":
    a = GalagaPirata()
    a.corre_juego()
