import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
	"""Клас, що виводить рахунок"""

	def __init__(self, ai_game):
		"""Ініціалізація атрибутів, пов'язаних із рахунком"""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		#Налаштування шрифту для відображення рахунку
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		#Підготувати зображення з початковим рахунком
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		"""Перетворити рахунок на зображення"""	
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True,
							self.text_color, self.settings.bg_color)

		#Показати рахунок у верхньому правому куті екрана
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Згенерувати рекорд у зображення"""	
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
							self.text_color, self.settings.bg_color)

		#Відцентрувати рекорд по горизонталі
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx - 20
		self.high_score_rect.top = self.score_rect.top

	def show_score(self):	
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def check_high_score(self):
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_level(self):
		"""Перетворити рівень у зображення"""		
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True,
							self.text_color, self.settings.bg_color)

		#Розташувати рівень під рахунком
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""Показує скільки лишилося кораблів"""	
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)