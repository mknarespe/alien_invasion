import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
	"""Загальний клас, що керує ресурсами та поведінкою гри"""

	def __init__(self):
		"""Ініціалізувати гру, створити ресурси гри"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		
		self._create_fleet()

		self.play_button = Button(self, "Play")

		#Задати колір фону
		self.bg_color = (230, 230, 230)

	def run_game(self):
		"""Позпочати головний цикл гри"""
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

			
	def _check_events(self):
			"""Реагувати на натискання клавіш та події миші"""
			#Слідкувати за подіями миші та клавіатури
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Розпочати нову гру, коли користувач натисне кнопку Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)	
		if button_clicked and not self.stats.game_active:
			#Анулювати ігрову статистику
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#Позбавитися надлишку прибульців та куль
			self.aliens.empty()
			self.bullets.empty()

			#Створити новий флот та відцентрувати корабель
			self._create_fleet()
			self.ship.center_ship()

			#Приховати курсор миші
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			#Перемістити корабель праворуч
			self.ship.moving_right = True
		if event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		if event.key == pygame.K_q:
			sys.exit()
		if event.key == pygame.K_SPACE:
			self._fire_bullet()		

	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		if event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)					

	def _update_screen(self):
			"""Оновити зображення на екрані та перемкнутися на новий екран"""			
			#Наново перемалювати екран на кожній ітерації циклу
			self.screen.fill(self.settings.bg_color)		
			self.ship.blitme()
			for bullet in self.bullets.sprites():
				bullet.draw_bullet()
			self.aliens.draw(self.screen)

			#Відобразити інформацію про рахунок
			self.sb.show_score()

			#Намалювати кнопку Play, якщо гра неактивна
			if not self.stats.game_active:
				self.play_button.draw_button()	

			#Показати останній намальований екран
			pygame.display.flip()

	def _update_bullets(self):
		"""Оновити позицію куль та позбавитися старих куль"""		
		self.bullets.update()

		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)	

		self._check_bullet_alien_collitions()		

	def _check_bullet_alien_collitions(self):
		"""Реакція на зіткнення куль з прибульцями"""
		#Перевірити зіткнення кулі і прибульця
		#Якщо куля влучила, позбавитись від неї та прибульця
		#Видалити всі кулі та прибульців, що зіткнулися
		collisions = pygame.sprite.groupcollide(
				self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
		self.sb.prep_score()
		self.sb.check_high_score()

		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#Збільшити рівень
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""Оновити позиції всіх прибульців у флоті"""		
		self._check_fleet_edges()	
		self.aliens.update()

		#Шукати зіткнення корабля з прибульцями
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		self._check_aliens_bottom()	

	def _check_fleet_edges(self):
		"""Реагує відповідно до того, 
		чи  досяг котрийсь із прибульців краю екрана"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Спуск всього флоту та зміна його напрямку"""			
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1	

	def _create_fleet(self):
		"""Створити флот прибульців"""				
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height -
							(10 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)	

	def _ship_hit(self):
		if self.stats.ships_left > 0:
			"""Реагувати на зіткнення прибульця з кораблем"""	
			self.stats.ships_left -=1
			self.sb.prep_ships()

			self.aliens.empty()
			self.bullets.empty()
	
			self._create_fleet()
			self.ship.center_ship()
	
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""Перевірити чи не досяг якийсь прибулець нижнього краю екрана"""	
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break


if __name__ == '__main__':
	#Створити екземпляр гри та запустити гру
	ai = AlienInvasion()		
	ai.run_game()