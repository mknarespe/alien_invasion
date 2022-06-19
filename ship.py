import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""Клас для керування кораблем"""

	def __init__(self, ai_game):
		"""Ініціалізувати корабель та задати його початкову позицію"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#Завантажити зображення корабля та отримати його rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		#Створювати кожен новий корабель внизу екрана, по центру
		self.rect.midbottom = self.screen_rect.midbottom

		#Зберегти десяткове значення для позиції корабля по горизонталі
		self.x = float(self.rect.x)

		#Індикатор руху
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""
		Оновити поточку позицію корабля на основі індикатора руху
		"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		#Оновити об'єкт ect з self.x
		self.rect.x = self.x

	def blitme(self):
		"""Намалювати корабель у його поточному розташуванні"""	
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Відцентрувати корабель на екрані"""	
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)