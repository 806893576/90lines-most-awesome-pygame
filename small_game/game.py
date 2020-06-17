import time, sys, pygame, random
from pygame.sprite import Sprite
BULLETS_SHOOT_FPS = pygame.USEREVENT
class Hero(Sprite):
	def __init__(self, screen, img, loc):
		super().__init__(); self.loc = loc; self.HERO_TYPE = img; self.image = pygame.image.load(self.HERO_TYPE); self.rect, self.screen, self.rect.centerx, self.rect.bottom, self.speed, self.moving_right, self.moving_left, self.moving_up, self.moving_down =  self.image.get_rect(), screen, 40, 300, 11, False, False, False, False; self.bullets_group = pygame.sprite.Group()
	def update(self):
		if self.moving_right:
			self.rect.centerx += self.speed
			if self.rect.centerx >= 770: self.moving_right = False
		if self.moving_left:
			self.rect.centerx -= self.speed
			if self.rect.centerx <= 30: self.moving_left = False
		if self.moving_up:
			self.rect.y -= self.speed
			if self.rect.y <= 0: self.moving_up = False
		if self.moving_down:
			self.rect.y += self.speed
			if self.rect.y >= 340: self.moving_down = False
	def shoot(self):
		bullet, bullet.rect.centery, bullet.rect.x = Bullet(self.loc), self.rect.centery, self.rect.x + 5; self.bullets_group.add(bullet)
class Bullet(Sprite):
	def __init__(self, loc):
		super().__init__(); self.BULLET_TYPE = "./img/bullet{}.png".format(loc); self.image = pygame.image.load(self.BULLET_TYPE); self.rect, self.y_speed, self.x_speed = self.image.get_rect(), 0, 16
	def update(self):
		self.rect.x += self.x_speed
		if self.rect.x >= 800: self.kill()
class EnemyBullet(Sprite):
	def __init__(self, loc):
		super().__init__(); self.loc = loc; self.BULLET_TYPE = "./img/boss{}.png".format(self.loc); self.image = pygame.image.load(self.BULLET_TYPE); self.rect, self.x_speed, self.y_speed = self.image.get_rect(), random.randint(-10, -5), random.randint(-3, 3)
	def update(self):
		self.rect.x, self.rect.y = self.rect.x + self.x_speed, self.rect.y + self.y_speed
		if self.rect.bottom >= 400 or self.rect.x < 0 or self.rect.y < 0: self.kill()
class Enemy(Sprite):
	def __init__(self, loc):
		super().__init__(); self.ENEMY_TYPE = "./img/small{}1.png".format(loc); self.image = pygame.image.load(self.ENEMY_TYPE); self.rect, self.rect.x, self.rect.y, self.y_speed, self.x_speed = self.image.get_rect(), 800, random.randint(10, 380), random.randint(-3, 3), random.randint(-8, -4)
	def update(self):
		self.rect.x, self.rect.y = self.rect.x + self.x_speed, self.rect.y + self.y_speed
		if self.rect.y < 0 or self.rect.bottom > 400: self.y_speed = -self.y_speed
		if self.rect.x <= 0: self.rect.x = 800
class Enemys(Sprite):
	def __init__(self, loc):
		super().__init__(); self.loc = loc; self.enemys_group, self.bullet_enemy_group, self.hited, self.n, self.enemy = pygame.sprite.Group(), pygame.sprite.Group(), False, 0, Enemy(self.loc)
	def add_enmey_and_shoot(self):
		if self.n % 50 == 0:
			self.enemys_group.add(self.enemy); bullet_enemy, bullet_enemy.rect.centerx, bullet_enemy.rect.bottom, self.n = EnemyBullet(self.loc), self.enemy.rect.centerx, self.enemy.rect.bottom + 5, 0; self.bullet_enemy_group.add(bullet_enemy)
		if self.hited: enemy_hited, self.enemy = EenemyHited(), Enemy(self.loc)
		self.n += 1
		return self.enemy.rect.x, self.enemy.rect.y
class EenemyHited(Sprite):
	def update(self): self.kill()
class MainGame(object):
	def __init__(self):
		self.loc = 1; pygame.init(); self.screen, self.BG_IMAGE = pygame.display.set_mode((800, 400)), pygame.image.load("./img/back1.jpeg"); self.rect, self.hero, self.enemy = self.BG_IMAGE.get_rect(), Hero(self.screen, "./img/hero{}1.png".format(self.loc), self.loc), Enemy(self.loc); self.screen.blit(self.BG_IMAGE, (0, 0)); pygame.time.set_timer(BULLETS_SHOOT_FPS , 280); self.heros_group, self.enemy_group, self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5, self.num =  pygame.sprite.Group(self.hero), pygame.sprite.Group(self.enemy), Enemys(self.loc), Enemys(self.loc), Enemys(self.loc), Enemys(self.loc), Enemys(self.loc), 0
	def __event_handle(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.hero.moving_left = True
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.hero.moving_right = True
				if event.key == pygame.K_w or event.key == pygame.K_UP: self.hero.moving_up = True
				if event.key == pygame.K_s or event.key == pygame.K_DOWN: self.hero.moving_down = True		
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.hero.moving_left = False
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.hero.moving_right = False
				if event.key == pygame.K_w or event.key == pygame.K_UP: self.hero.moving_up = False
				if event.key == pygame.K_s or event.key == pygame.K_DOWN: self.hero.moving_down = False
			if event.type == BULLETS_SHOOT_FPS: self.hero.shoot()
	def __collide(self):
		for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5]:
			bullet_enemy_collide = pygame.sprite.groupcollide(enemy_num.enemys_group, self.hero.bullets_group, True, True)
			hero_enemy_collide = pygame.sprite.groupcollide(self.heros_group, enemy_num.enemys_group, False, True)
			bullet_hero_collide = pygame.sprite.groupcollide(self.heros_group, enemy_num.bullet_enemy_group, False, True)
			if bullet_enemy_collide: enemy_num.hited = True;  self.num = self.num + 1;  print(self.num) 
			if bullet_enemy_collide: 
				if self.num % 10 == 0: self.loc += 1; pygame.init(); self.screen, self.BG_IMAGE = pygame.display.set_mode((800, 400)), pygame.image.load("./img/back{}.jpeg".format(self.loc)); self.hero = Hero(self.screen, "./img/hero{}1.png".format(self.loc), self.loc); self.heros_group = pygame.sprite.Group(self.hero); self.enemy = Enemy(self.loc); self.enemy_group = pygame.sprite.Group(self.enemy); self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5 = Enemys(self.loc), Enemys(self.loc), Enemys(self.loc), Enemys(self.loc), Enemys(self.loc)
				if self.loc >=3: self.loc = 0
	def __update_elements(self):
		self.screen.blit(self.BG_IMAGE, (0, self.rect.y))
		for i in [self.heros_group, self.hero.bullets_group]: i.update(), i.draw(self.screen)
		for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5]:
			enemy_num.enemys_group.update(), enemy_num.enemys_group.draw(self.screen), enemy_num.bullet_enemy_group.update(), enemy_num.bullet_enemy_group.draw(self.screen)
		pygame.display.update()
	def run_game(self): 
		while True:
			for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5]: enemy_num.add_enmey_and_shoot()
			self.__collide(); self.__event_handle(); self.__update_elements()
if __name__ == '__main__':
	main_game = MainGame()
	main_game.run_game()