import time, sys, pygame, random
from pygame.sprite import Sprite

# 创建常量
BULLETS_SHOOT_FPS, BOSS_BULLETS_SHOOT_FPS = pygame.USEREVENT, pygame.USEREVENT + 1

class Hero(Sprite):
	def __init__(self, screen):
		super().__init__()	
		self.HERO_TYPE = "./img/hero11.png"
		self.image = pygame.image.load(self.HERO_TYPE)
		self.rect, self.screen, self.rect.centerx, self.rect.bottom, self.speed, self.moving_right, self.moving_left, self.moving_up, self.moving_down =  self.image.get_rect(), screen, 40, 300, 11, False, False, False, False
		self.bullets_group = pygame.sprite.Group()

	def update(self):
		if self.moving_right:
			self.rect.centerx += self.speed
			if self.rect.centerx >= 770:
				self.moving_right = False
		if self.moving_left:
			self.rect.centerx -= self.speed
			if self.rect.centerx <= 30:
				self.moving_left = False
		if self.moving_up:
			self.rect.y -= self.speed
			if self.rect.y <= 0:
				self.moving_up = False
		if self.moving_down:
			self.rect.y += self.speed
			if self.rect.y >= 340:
				self.moving_down = False

	def shoot(self):
		bullet, bullet.rect.centery, bullet.rect.x = Bullet(), self.rect.centery, self.rect.x + 5
		self.bullets_group.add(bullet)


# 这里是英雄子弹
class Bullet(Sprite):
	def __init__(self):
		super().__init__()
		self.BULLET_TYPE = "./img/bullet1.png"
		self.image = pygame.image.load(self.BULLET_TYPE)
		self.rect, self.y_speed, self.x_speed = self.image.get_rect(), 0, 16

	def update(self):
		self.rect.y -= self.y_speed
		self.rect.x += self.x_speed
		if self.rect.x >= 800:
			self.kill()

class EnemyBullet(Bullet):
	def __init__(self):
		super().__init__()
		self.BULLET_TYPE = "./img/small_bullet1.png"
		self.image = pygame.image.load(self.BULLET_TYPE)
		self.rect, self.x_speed, self.y_speed = self.image.get_rect(), random.randint(-10, -5), random.randint(-3, 3)

	def update(self):
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed
		if self.rect.bottom >= 400 or self.rect.x < 0 or self.rect.y < 0:
			self.kill()


class BossBullet(Sprite):
	def __init__(self):
		super().__init__()
		self.BULLET_TYPE = "./img/bb1.png"
		self.image = pygame.image.load(self.BULLET_TYPE)
		self.rect, self.x_speed, self.y_speed = self.image.get_rect(), random.randint(-15, -10), random.randint(-5, 5)

	def update(self):
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed
		if self.rect.bottom >= 400 or self.rect.x < 0 or self.rect.y < 0:
			self.kill()

		
class Enemy(Sprite):
	def __init__(self):
		super().__init__()
		self.ENEMY_TYPE = "./img/small11.png"
		self.image = pygame.image.load(self.ENEMY_TYPE)
		self.rect, self.rect.x, self.rect.y, self.y_speed, self.x_speed = self.image.get_rect(), 800, random.randint(10, 380), random.randint(-3, 3), random.randint(-8, -4)

	def update(self):
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed
		if self.rect.y < 0 or self.rect.bottom > 400:
			# 通过把速度值取反，获得飞机碰壁反弹效果
			self.y_speed = -self.y_speed
		if self.rect.x <= 0:
			self.rect.x = 800


class Enemys(Sprite):
	def __init__(self):
		super().__init__()
		self.enemys_group, self.bullet_enemy_group, self.hited, self.n, self.enemy = pygame.sprite.Group(), pygame.sprite.Group(), False, 0, Enemy()

	def add_enmey_and_shoot(self):
		if self.n % 50 == 0:
			self.enemys_group.add(self.enemy)
			bullet_enemy, bullet_enemy.rect.centerx, bullet_enemy.rect.bottom, self.n = EnemyBullet(), self.enemy.rect.centerx, self.enemy.rect.bottom + 5, 0
			self.bullet_enemy_group.add(bullet_enemy)
		if self.hited:
			enemy_hited, self.enemy = EenemyHited(), Enemy()
		self.n += 1
		return self.enemy.rect.x, self.enemy.rect.y


class EenemyHited(Sprite):
	def update(self):
		self.kill()


class Boss(Sprite):
	"""docsring for Boss"""
	def __init__(self, screen):
		super().__init__()
		self.image = pygame.image.load("./img/boss11.png")
		self.rect, self.rect.x, self.rect.y , self.speed_x, self.speed_y, self.boss_bullets_group, self.boss_big_shoot_group, self.screen, self.boss_on_off, self.blood = self.image.get_rect(), 750, 10, random.randint(-5, -1), random.randint(5, 5), pygame.sprite.Group(), pygame.sprite.Group(), screen, True, 15

	def update(self):
		self.rect.centerx += self.speed_x
		self.rect.y += self.speed_y
		if self.rect.x <= 300 or self.rect.x >= 800:
			self.speed_x = -self.speed_x
		if self.rect.y <= 0 or self.rect.y >=280:
			self.speed_y = -self.speed_y
		
		self.hit_box = (self.rect.x + 8, self.rect.y + 11, 29, 52)
		pygame.draw.rect(self.screen, (0, 128, 0), (self.hit_box[0], self.hit_box[1] - 10, 150, 8))
		pygame.draw.rect(self.screen, (255, 0, 0), (self.hit_box[0] + self.blood * 10, self.hit_box[1] - 10, 150 - self.blood * 10, 8))

	def boss_shoot(self):
		boss_bullet0, boss_bullet0.rect.centery, boss_bullet0.rect.x = BossBullet(), self.rect.centery, self.rect.x - 5
		self.boss_bullets_group.add(boss_bullet0)


class MainGame(object):
	def __init__(self):
		pygame.init()
		self.SCREEN_SIZE = (800, 400)
		self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
		self.BG_IMAGE = pygame.image.load("./img/back1.jpeg")
		self.rect = self.BG_IMAGE.get_rect()
		self.screen.blit(self.BG_IMAGE, (0, 0))
		self.fps = 100
		self.fps_clock = pygame.time.Clock()
		self.geme_fps = self.fps_clock.tick(self.fps)
		pygame.time.set_timer(BULLETS_SHOOT_FPS , 280)
		pygame.time.set_timer(BOSS_BULLETS_SHOOT_FPS , 800)
		self.hero, self.enemy, self.boss = Hero(self.screen), Enemy(), Boss(self.screen)
		self.heros_group, self.enemy_group =  pygame.sprite.Group(self.hero), pygame.sprite.Group(self.enemy)
		self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5, self.boss_show_num, self.enmeys_die_before_boss, self.boss_group = Enemys(), Enemys(), Enemys(), Enemys(), Enemys(), 0, 10, pygame.sprite.Group(self.boss)


	def __event_handle(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					self.hero.moving_left = True
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					self.hero.moving_right = True
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					self.hero.moving_up = True
				if event.key == pygame.K_s or event.key == pygame.K_DOWN:
					self.hero.moving_down = True
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					self.hero.moving_left = False
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					self.hero.moving_right = False
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					self.hero.moving_up = False
				if event.key == pygame.K_s or event.key == pygame.K_DOWN:
					self.hero.moving_down = False

			if event.type == BULLETS_SHOOT_FPS:
				self.hero.shoot()

			if event.type == BOSS_BULLETS_SHOOT_FPS:
				if self.boss_show_num >= self.enmeys_die_before_boss:
					if self.boss.boss_on_off:
						self.boss.boss_shoot()
					else:
						pass

	def __collide(self):
		for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5]:
			bullet_enemy_collide = pygame.sprite.groupcollide(enemy_num.enemys_group, self.hero.bullets_group, True, True)
			hero_enemy_collide = pygame.sprite.groupcollide(self.heros_group, enemy_num.enemys_group, False, True)
			bullet_hero_collide = pygame.sprite.groupcollide(self.heros_group, enemy_num.bullet_enemy_group, False, True)
			if bullet_enemy_collide:
				enemy_num.hited = True
				self.boss_show_num += 1

		if self.boss_show_num >= self.enmeys_die_before_boss:
			if self.boss.blood > 0:
				boss_hero_bullets_collide = pygame.sprite.groupcollide(self.boss_group, self.hero.bullets_group, False, True)
				if boss_hero_bullets_collide: self.boss.blood -= 1
					
			else:
				boss_hero_bullets_collide = pygame.sprite.groupcollide(self.boss_group, self.hero.bullets_group, True, True)
				if boss_hero_bullets_collide: self.boss.boss_on_off = False
			boss_bullet_hero_collide = pygame.sprite.groupcollide(self.heros_group, self.boss.boss_bullets_group, False, True)


	def __update_elements(self):
		self.screen.blit(self.BG_IMAGE, (0, self.rect.y))
		for i in [self.heros_group, self.hero.bullets_group]: i.update(), i.draw(self.screen)
		if self.boss_show_num <= self.enmeys_die_before_boss + 1:
			for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5]:
				enemy_num.enemys_group.update(), enemy_num.enemys_group.draw(self.screen), enemy_num.bullet_enemy_group.update(), enemy_num.bullet_enemy_group.draw(self.screen)
		if self.boss_show_num >= self.enmeys_die_before_boss:
			for i in [self.boss_group, self.boss.boss_bullets_group, self.boss.boss_big_shoot_group]: i.update(), i.draw(self.screen)
		pygame.display.update()

	def run_game(self): 
		while True:
			if self.boss_show_num < self.enmeys_die_before_boss:
				for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4, self.enemys5]:
					enemy_num.add_enmey_and_shoot()
			self.__collide()
			self.__event_handle()
			self.__update_elements()
	

if __name__ == '__main__':
	main_game = MainGame()
	main_game.run_game()