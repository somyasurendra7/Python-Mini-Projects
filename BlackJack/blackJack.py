try:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
except ImportError:
    import simplegui
import random


board = (740, 650)
img_cards = simplegui.load_image('cards.jpeg')
img_back = simplegui.load_image('back.jpeg')
c_width = 73
c_height = 98
ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
colors = ('Club', 'Spade', 'Heart', 'Diamond')
values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
font = 2
loc = (board[0] - 200, board[1] - 120)
dealer_score = 0
player_score = 0
upper_msg = ''
lower_msg = ''
# Game state : started and stopped
state = 'stop'
deck = None
dealer_hand = None
player_hand = None


class Card:
	def __init__(self, rank, color, exposed=True):
		self.rank = rank
		self.color = color
		self.exposed = exposed

	def __str__(self):
		return "Rank: " + self.rank + ", Color: " + self.color + ", Exposed: " + self.exposed

	def get_rank(self):
		return self.rank

	def get_color(self):
		return self.color

	def get_exposed(self):
		return self.exposed

	def expose_it(self):
		self.exposed = True

	def hide_expose(self):
		self.exposed = False


class Deck:
	def __init__(self):
		self.cards = []
		for color in colors:
			for rank in ranks:
				self.cards.append(Card(rank, color))
		random.shuffle(self.cards)

	def __str__(self):
		for card in self.cards:
			print(card)
		return ""

	def get_one_card(self):
		return self.cards.pop()

	def get_all_cards(self):
		return self.cards


class Hand:
	def __init__(self):
		self.cards = []

	def __str__(self):
		for card in self.cards:
			print(card)
		return ""

	def get_sum(self):
		sum_cards = 0
		has_ace = False
		for card in self.cards:
			sum_cards += values[card.get_rank()]
			if card.get_rank() == 'A':
				has_ace = True
			sum_max = sum_cards
			sum_min = sum_cards
		if has_ace == True:
			if sum_cards + 10 <= 21:
				sum_max += 10
		return sum_max, sum_min

	def add_one_card(self, deck):
		self.cards.append(deck.get_one_card())

	def hide_one_card(self, index):
		self.cards[index].hide_expose()

	def expose_one_card(self, index):
		self.cards[index].expose_it()

	def get_all_cards(self):
		return self.cards


# creating a new game

def new_game():
	upper_msg = 'This is a new round.'
	lower_msg = 'Hit or stand?'
	state = 'started'

	# initialising
	deck = Deck()
	dealer_hand = Hand()
	player_hand = Hand()

	for i in range(2):
		dealer_hand.add_one_card(deck)
		player_hand.add_one_card(deck)

	# hide the dealer's hand first card
	dealer_hand.hide_one_card(0)


# creating draw handler

def draw_handler(screen):
	screen.draw_text('BlackJack', (225, 80), 80, 'Black')
	screen.draw_text('BlackJack', (225 - font, 80 - font), 80, 'Blue')

	screen.draw_polygon([[TABLE_UPPER_LEFT_CORNER[0] + 200, TABLE_UPPER_LEFT_CORNER[1] + 120],
						 [TABLE_UPPER_LEFT_CORNER[0], TABLE_UPPER_LEFT_CORNER[1] + 120], TABLE_UPPER_LEFT_CORNER,
						 [TABLE_UPPER_LEFT_CORNER[0] + 200, TABLE_UPPER_LEFT_CORNER[1]]], 2, 'Yellow')

	screen.draw_line((TABLE_UPPER_LEFT_CORNER[0], TABLE_UPPER_LEFT_CORNER[1] + 80),
					 (TABLE_UPPER_LEFT_CORNER[0] + 200, TABLE_UPPER_LEFT_CORNER[1] + 80), 2, 'Yellow')

	screen.draw_line((TABLE_UPPER_LEFT_CORNER[0], TABLE_UPPER_LEFT_CORNER[1] + 40),
					 (TABLE_UPPER_LEFT_CORNER[0] + 200, TABLE_UPPER_LEFT_CORNER[1] + 40), 2, 'Yellow')

	screen.draw_line((TABLE_UPPER_LEFT_CORNER[0] + 130, TABLE_UPPER_LEFT_CORNER[1] + 40),
					 TABLE_UPPER_LEFT_CORNER[0] + 130, (TABLE_UPPER_LEFT_CORNER[1] + 120), 2, 'Yellow')

	# adding scores

	screen.draw_text(str(dealer_score), (TABLE_UPPER_LEFT_CORNER[0] + 150, TABLE_UPPER_LEFT_CORNER[1] + 75), 35,
					 'Black')

	screen.draw_line(str(dealer_score),
					 (TABLE_UPPER_LEFT_CORNER[0] + 150 - font, TABLE_UPPER_LEFT_CORNER[1] + 75 - font), 35, 'Red')

	screen.draw_text(str(player_score), (TABLE_UPPER_LEFT_CORNER[0] + 150, TABLE_UPPER_LEFT_CORNER[1] + 115), 35,
					 'Black')

	screen.draw_line(str(player_score), TABLE_UPPER_LEFT_CORNER[0] + 150 - font,
					 (TABLE_UPPER_LEFT_CORNER[1] + 115 - font), 35, 'Orange')

	# adding message

	screen.draw_text(upper_msg, (150, 350), 50, 'Black')

	screen.draw_text(upper_msg, (150 - font, 350 - font), 50, 'Yellow')

	screen.draw_text(lower_msg, (30, 550), 35, 'Black')

	screen.draw_text(lower_msg, (30 - font, 550 - font), 35, 'Orange')

	# settings

	cards_margin = 30
	dealer_card_line = 210
	player_card_line = 460
	index_of_dealer_cards = 0
	index_of_player_cards = 0
	center_in_png = (c_width / 2.0, c_height / 2.0)

	# draw dealer's card

	for card in player_hand.get_all_cards():
		index_rank = ranks.index(card.get_rank())
		index_color = colors.index(card.get_color())
		if card.is_exposed() == True:
			screen.draw_image(img_cards,
							  (center_in_png[0] + index_rank * c_width, center_in_png[1] + index_color * c_height),
							  (c_width, c_height), (cards_margin * (index_of_player_cards + 1) + center_in_png[
					0] + c_width * index_of_dealer_cards, dealer_cards_line), (c_width, c_height))
		else:
			screen.draw_image(img_back, (35.5, 48), (71, 96), (center_in_png[0] + cards_margin, dealer_cards_line),
							  (c_width, c_height))

		index_of_dealer_cards += 1

	# draw player's card

	for card in player_hand.get_all_cards():
		index_rank = ranks.index(card.get_rank())
		index_color - colors.index(card.get_color())
		screen.draw_image(img_cards,
						  (center_in_png[0] + index_rank * c_width, center_in_png[1] + index_color * c_height),
						  (c_width, c_height), (cards_margin * (index_of_player_cards + 1) + center_in_png[
				0] + c_width * index_of_player_cards, player_cards_line), (c_weight, c_height))
		index_of_player_cards += 1


# creating buttons

def btn_deal():
	if state == 'started':
		dealer_score += 1
	new_game()


def btn_hit():
	if state != 'stop':
		upper_msg = ''
		player_hand.add_one_card(deck)
		sum_max, sum_min = player_hand.get_sum()
		if sum_min > 21:
			dealer_hand.expose_one_card(0)
			dealer_score += 1
			upper_msg = 'You went bust and lose.'
			lower_msg = 'New deal?'
			state = 'stop'


def btn_stand():
	if state != 'stop':
		player_max, player_min = player_hand.get_sum()
		play_sum = 0
		if player_max <= 21:
			play_sum = player_max
		else:
			play_sum = player_min
		dealer_sum = 0

		while True:
			if dealer_max <= 21:
				dealer_sum = dealer_max
			else:
				dealer_sum = dealer_min
			if dealer_sum >= 17:
				break
			else:
				dealer_hand.add_one_card(deck)

			dealer_hand.expose_one_card(0)

			if dealer_sum > 21:
				player_score += 1
				upper_msg = 'Dealer went bust and lose.'
				lower_msg = 'You win! New deal?'
				state = 'stop'
			else:
				if dealer_sum < play_sum:
					player_score += 1
					upper_msg = 'You win!'
					lower_msg = 'New deal?'
					state = 'stop'
				else:
					dealer_score += 1
					upper_msg = 'You lose!'
					lower_msg = 'New deal?'
					state = 'stop'


frame = simplegui.create_frame('Blackjack', board[0], board[1], 150)
frame.set_canvas_background('Green')

frame.set_draw_handler(draw_handler)
frame.add_button('Deal', btn_deal, 150)
frame.add_button('Hit', btn_hit, 150)
frame.add_button('Stand', btn_stand, 150)

new_game()

frame.start()
