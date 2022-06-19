class GameStats:
	"""Відстежування статистики гри"""

	def __init__(self, ai_game):
		"""Ініціалізація статистики"""
		self.settings = ai_game.settings
		self.reset_stats()

		self.game_active = False

		self.high_score = 0

	def reset_stats(self):
		"""ніціалізація статистики, що може змінюватися впродовж гри"""	
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1