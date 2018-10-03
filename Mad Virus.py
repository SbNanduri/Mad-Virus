import pygame
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

mouse_1 = False
cell_gap_y = 40
cell_gap_x = cell_gap_y

# eyes = pygame.image.load('Virus Eyes.png')

number_viruses_row = 20
number_viruses_column = number_viruses_row
main_virus_index = random.randint(0, number_viruses_row * number_viruses_column - 1)
main_indexes = set()
main_indexes.add(main_virus_index)

# Colours

off_white = (230, 230, 230)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (60, 60, 60)
light_grey = (135, 135, 135)
red = (245, 0, 0)
green = (0, 215, 0)
blue = (0, 0, 245)
purple = (150, 0, 175)
pink = (245, 105, 180)
turquoise = (0, 206, 209)
ochre = (204, 119, 34)

virus_colours = [red, green, blue, purple]

# The coords of each colour is ((x%num_row)-1, x//num_row), x = index of colour + 1
colour_list = random.choices(virus_colours, k=(number_viruses_row * number_viruses_column))
# colour_list = (number_viruses_row * number_viruses_column) * [blue]

colour_list[main_virus_index] = light_grey

display_width = 800
display_height = 600
resolution = (display_width, display_height)

Display = pygame.display.set_mode(resolution)

pygame.display.set_caption('Mad Virus')

clock = pygame.time.Clock()

# Fonts
small_font_size = display_width // 25
med_font_size = display_width // 12
large_font_size = display_width // 5

small_font = pygame.font.SysFont('Roboto', small_font_size)
med_font = pygame.font.SysFont('Roboto', med_font_size)
large_font = pygame.font.SysFont('Roboto', large_font_size)

# Options
res_change = resolution
row_change = number_viruses_row
col_change = number_viruses_column


class Virus:
	def __init__(self,
	             colour=black,
	             top_left=((display_width / 4) + 15, 15),
	             width_height=(3 * display_width / 100, 3 * display_height / 100),
	             main=False):
		self.colour = colour
		self.x = top_left[0]
		self.y = top_left[1]
		self.width = width_height[0]
		self.height = width_height[1]
		self.main = main  # Use a sprite of eyes to indicate the main ones

	def draw_to_screen(self):
		Display.fill(self.colour, rect=[self.x, self.y, self.width, self.height])

		if self.main:
			small_width = self.width / 4
			small_height = self.height / 4
			Display.fill(black, rect=[self.x + 0.5 * self.width - small_width * 0.5,
			                          self.y + 0.5 * self.height - small_height * 0.5,
			                          small_width,
			                          small_height])


def generate_viruses(colours, number_row, number_column):
	# Gap between edge of screen and viruses:
	global cell_gap_y
	global cell_gap_x

	# Keeps track of which colour from colour list to use:
	colour_count = 0

	if number_column is None:
		number_column = number_row

	corner_rows = []
	corner_columns = []
	virus_list = []

	total_width = (3 * display_width / 4) - (2 * cell_gap_x)
	total_height = display_height - (2 * cell_gap_y)  # This was display_width. Maybe change it back later

	virus_width = total_width / number_row
	virus_height = total_height / number_column

	if virus_width > virus_height:
		cell_gap_x += (virus_width - virus_height)
		virus_width = virus_height
	else:
		cell_gap_y += (virus_height - virus_width)
		virus_height = virus_width

	for virus_column in range(number_column):
		for virus_row in range(number_row):
			x1 = virus_row * virus_width + cell_gap_x + display_width / 4
			corner_rows.append(x1)
			y1 = virus_column * virus_height + cell_gap_y
			corner_columns.append(y1)

			virus = Virus(black, (x1, y1), (virus_width, virus_height))
			virus.colour = colours[colour_count]
			virus_list.append(virus)
			colour_count += 1

	for virus_index in range(len(virus_list)):
		if virus_index in main_indexes:
			virus_list[virus_index].main = True
		virus_list[virus_index].draw_to_screen()
	return virus_list


def paused():
	global mouse_1
	global cell_gap_y
	global cell_gap_x
	global number_viruses_row
	global number_viruses_column
	global main_virus_index
	global main_indexes
	global colour_list
	global display_width
	global display_height
	global resolution
	global Display
	global small_font_size
	global med_font_size
	global large_font_size
	global small_font
	global med_font
	global large_font

	tracker = 1
	num_of_buttons = 4
	key_pressed = False
	resume = False
	restart = False

	gap = display_height / 27

	options_data = message_box_data('Options',
	                                black,
	                                size='medium')

	text_width = options_data['Right'] - options_data['Left']

	# Checks the longest word in the menu and figures out how long the text boxes need to be
	title_box_data = message_box_data('Paused',
	                                  black,
	                                  y_displace=gap,
	                                  x_displace=0,
	                                  size='large',
	                                  side='top')

	title_box_bottom = title_box_data['Bottom']

	width = text_width + 40  # (display_width / 3.6)
	top_left_x = (display_width / 2) - (width / 2)
	height = ((display_height - title_box_bottom) - gap * (1 + num_of_buttons)) / num_of_buttons

	while not (resume or restart):
		mouse_1 = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					tracker += 1
				if event.key == pygame.K_UP:
					tracker -= 1

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
						key_pressed = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mouse_1 = True

		hover_list = []
		tracker -= 1
		tracker %= num_of_buttons
		tracker += 1

		Display.fill(off_white)

		message_to_screen('Paused',
		                  black,
		                  y_displace=gap,
		                  x_displace=0,
		                  size='large',
		                  side='top')

		resume, hover = menu_button('Resume',
		                            black,
		                            red,
		                            (top_left_x, title_box_bottom + gap),
		                            (top_left_x + width, title_box_bottom + gap + height),
		                            size='medium',
		                            tracker=tracker,
		                            intended_tracker_pos=1,
		                            key_pressed=key_pressed)
		hover_list.append(hover)

		restart, hover = menu_button('Restart',
		                             black,
		                             red,
		                             (top_left_x, title_box_bottom + 2 * gap + height),
		                             (top_left_x + width, title_box_bottom + 2 * gap + 2 * height),
		                             size='medium',
		                             tracker=tracker,
		                             intended_tracker_pos=2,
		                             key_pressed=key_pressed)
		hover_list.append(hover)

		option_select, hover = menu_button('Options',
		                                   black,
		                                   red,
		                                   (top_left_x, title_box_bottom + 3 * gap + 2 * height),
		                                   (top_left_x + width, title_box_bottom + 3 * gap + 3 * height),
		                                   size='medium',
		                                   tracker=tracker,
		                                   intended_tracker_pos=3,
		                                   key_pressed=key_pressed)
		hover_list.append(hover)

		game_exit, hover = menu_button('Quit',
		                               black,
		                               red,
		                               (top_left_x, title_box_bottom + 4 * gap + 3 * height),
		                               (top_left_x + width, title_box_bottom + 4 * gap + 4 * height),
		                               size='medium',
		                               tracker=tracker,
		                               intended_tracker_pos=4,
		                               key_pressed=key_pressed)
		hover_list.append(hover)

		hover = max(hover_list)
		if hover:
			tracker = hover

		if restart:
			cell_gap_y = 40
			cell_gap_x = cell_gap_y
			# number_viruses_row = 20
			number_viruses_column = number_viruses_row
			main_virus_index = random.randint(0, number_viruses_row * number_viruses_column - 1)
			main_indexes = set()
			main_indexes.add(main_virus_index)
			colour_list = random.choices(virus_colours, k=(number_viruses_row * number_viruses_column))
			# display_width = 800
			# display_height = 600
			# resolution = (display_width, display_height)
			# Display = pygame.display.set_mode(resolution)
			# small_font_size = display_width // 25
			# med_font_size = display_width // 12
			# large_font_size = display_width // 5
			# small_font = pygame.font.SysFont('Roboto', small_font_size)
			# med_font = pygame.font.SysFont('Roboto', med_font_size)
			# large_font = pygame.font.SysFont('Roboto', large_font_size)

			game_loop()

		if option_select:
			options()

		elif game_exit:
			pygame.quit()
			quit()

		pygame.display.update()
		clock.tick(30)


def options():
	global mouse_1
	tracker = 1
	num_of_buttons = 5
	key_pressed = False
	back = False
	gap = display_height / 27

	# Checks the longest word in the menu and figures out how long the text boxes need to be
	longest_data = message_box_data('Viruses in column',
	                                black,
	                                size='medium')

	text_width = longest_data['Right'] - longest_data['Left']

	title_box_data = message_box_data('Options',
	                                  black,
	                                  y_displace=gap,
	                                  x_displace=0,
	                                  size='large',
	                                  side='top')
	title_box_bottom = title_box_data['Bottom']

	width = text_width + 40  # (display_width / 3.6)
	top_left_x = (display_width / 2) - (width / 2)
	height = ((display_height - title_box_bottom) - gap * (1 + num_of_buttons)) / num_of_buttons

	while not (back):
		mouse_1 = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					tracker += 1
				if event.key == pygame.K_UP:
					tracker -= 1

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
						key_pressed = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mouse_1 = True

		hover_list = []
		tracker -= 1
		tracker %= num_of_buttons
		tracker += 1

		Display.fill(off_white)

		message_to_screen('Options',
		                  black,
		                  y_displace=gap,
		                  x_displace=0,
		                  size='large',
		                  side='top')

		resolution_settings, hover = menu_button('Resolution',
		                                         black,
		                                         red,
		                                         (top_left_x, title_box_bottom + gap),
		                                         (top_left_x + width, title_box_bottom + gap + height),
		                                         size='medium',
		                                         tracker=tracker,
		                                         intended_tracker_pos=1,
		                                         key_pressed=key_pressed)
		hover_list.append(hover)

		row_settings, hover = menu_button('Viruses in row',
		                                  black,
		                                  red,
		                                  (top_left_x, title_box_bottom + 2 * gap + height),
		                                  (top_left_x + width, title_box_bottom + 2 * gap + 2 * height),
		                                  size='medium',
		                                  tracker=tracker,
		                                  intended_tracker_pos=2,
		                                  key_pressed=key_pressed)
		hover_list.append(hover)

		column_settings, hover = menu_button('Viruses in column',
		                                     black,
		                                     red,
		                                     (top_left_x, title_box_bottom + 3 * gap + 2 * height),
		                                     (top_left_x + width, title_box_bottom + 3 * gap + 3 * height),
		                                     size='medium',
		                                     tracker=tracker,
		                                     intended_tracker_pos=3,
		                                     key_pressed=key_pressed)
		hover_list.append(hover)

		back, hover = menu_button('Back',
		                          black,
		                          red,
		                          (top_left_x, title_box_bottom + 4 * gap + 3 * height),
		                          (top_left_x + width, title_box_bottom + 4 * gap + 4 * height),
		                          size='medium',
		                          tracker=tracker,
		                          intended_tracker_pos=4,
		                          key_pressed=key_pressed)
		hover_list.append(hover)

		game_exit, hover = menu_button('Quit',
		                               black,
		                               red,
		                               (top_left_x, title_box_bottom + 5 * gap + 4 * height),
		                               (top_left_x + width, title_box_bottom + 5 * gap + 5 * height),
		                               size='medium',
		                               tracker=tracker,
		                               intended_tracker_pos=5,
		                               key_pressed=key_pressed)
		hover_list.append(hover)

		hover = max(hover_list)

		if hover:
			tracker = hover

		if resolution_settings:
			pass
			# resolutions()
		elif row_settings:
			pass
			# row_viruses()
		elif column_settings:
			pass
			# col_viruses()
		elif back:
			pass
			# keep_changes()
		elif game_exit:
			pygame.quit()
			quit()

		pygame.display.update()
		clock.tick(30)


def keep_changes():
	global mouse_1
	global display_width
	global display_height
	global resolution
	global number_viruses_row
	global number_viruses_column
	tracker = 1
	num_of_buttons = 2
	key_pressed = False
	back = False

	gap = display_height / 27

	# Checks the longest word in the menu and figures out how long the text boxes need to be
	longest_data = message_box_data('Yes',
	                                black,
	                                size='medium')

	text_width = longest_data['Right'] - longest_data['Left']

	title_box_data = message_box_data('Keep Changes?',
	                                  black,
	                                  y_displace=gap,
	                                  x_displace=0,
	                                  size='large',
	                                  side='top')
	title_box_bottom = title_box_data['Bottom']

	width = text_width + 40  # (display_width / 3.6)
	top_left_x = (display_width / 2) - (width / 2)
	height = ((display_height - title_box_bottom) - gap * (1 + num_of_buttons)) / num_of_buttons

	while not back:
		mouse_1 = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					tracker += 1
				if event.key == pygame.K_UP:
					tracker -= 1

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
						key_pressed = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mouse_1 = True

		hover_list = []
		tracker -= 1
		tracker %= num_of_buttons
		tracker += 1

		Display.fill(off_white)

		message_to_screen('Keep Changes?',
		                  black,
		                  y_displace=gap,
		                  x_displace=0,
		                  size='large',
		                  side='top')

		yes, hover = menu_button('Yes',
		                           black,
		                           red,
		                           (top_left_x, title_box_bottom + gap),
		                           (top_left_x + width, title_box_bottom + gap + height),
		                           size='medium',
		                           tracker=tracker,
		                           intended_tracker_pos=1,
		                           key_pressed=key_pressed)
		hover_list.append(hover)

		no, hover = menu_button('No',
		                           black,
		                           red,
		                           (top_left_x, title_box_bottom + 2 * gap + height),
		                           (top_left_x + width, title_box_bottom + 2 * gap + 2 * height),
		                           size='medium',
		                           tracker=tracker,
		                           intended_tracker_pos=2,
		                           key_pressed=key_pressed)
		hover_list.append(hover)

		hover = max(hover_list)

		if hover:
			tracker = hover

		if yes:
			display_width = res_change[0]
			display_height = res_change[1]
			resolution = res_change
			number_viruses_column = row_change
			number_viruses_column = col_change

			small_font_size = display_width // 25
			med_font_size = display_width // 12
			large_font_size = display_width // 5

			small_font = pygame.font.SysFont('Roboto', small_font_size)
			med_font = pygame.font.SysFont('Roboto', med_font_size)
			large_font = pygame.font.SysFont('Roboto', large_font_size)

			# Have to add more variables here, still not done

			game_loop()
		elif no:
			back = True

		pygame.display.update()
		clock.tick(30)


def resolutions():
	global mouse_1
	global res_change
	tracker = 1
	num_of_buttons = 5
	key_pressed = False
	back = False

	gap = display_height / 27

	# Checks the longest word in the menu and figures out how long the text boxes need to be
	longest_data = message_box_data('1000 x 800',
	                                black,
	                                size='medium')

	text_width = longest_data['Right'] - longest_data['Left']

	title_box_data = message_box_data('Resolution',
	                                  black,
	                                  y_displace=gap,
	                                  x_displace=0,
	                                  size='large',
	                                  side='top')
	title_box_bottom = title_box_data['Bottom']

	width = text_width + 40  # (display_width / 3.6)
	top_left_x = (display_width / 2) - (width / 2)
	height = ((display_height - title_box_bottom) - gap * (1 + num_of_buttons)) / num_of_buttons

	while not back:
		mouse_1 = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					tracker += 1
				if event.key == pygame.K_UP:
					tracker -= 1

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
						key_pressed = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mouse_1 = True

		hover_list = []
		tracker -= 1
		tracker %= num_of_buttons
		tracker += 1

		Display.fill(off_white)

		message_to_screen('Resolution',
		                  black,
		                  y_displace=gap,
		                  x_displace=0,
		                  size='large',
		                  side='top')

		res_1, hover = menu_button('800 x 600',
		                           black,
		                           red,
		                           (top_left_x, title_box_bottom + gap),
		                           (top_left_x + width, title_box_bottom + gap + height),
		                           size='medium',
		                           tracker=tracker,
		                           intended_tracker_pos=1,
		                           key_pressed=key_pressed)
		hover_list.append(hover)

		res_2, hover = menu_button('800 x 800',
		                           black,
		                           red,
		                           (top_left_x, title_box_bottom + 2 * gap + height),
		                           (top_left_x + width, title_box_bottom + 2 * gap + 2 * height),
		                           size='medium',
		                           tracker=tracker,
		                           intended_tracker_pos=2,
		                           key_pressed=key_pressed)
		hover_list.append(hover)

		res_3, hover = menu_button('1000 x 800',
		                           black,
		                           red,
		                           (top_left_x, title_box_bottom + 3 * gap + 2 * height),
		                           (top_left_x + width, title_box_bottom + 3 * gap + 3 * height),
		                           size='medium',
		                           tracker=tracker,
		                           intended_tracker_pos=3,
		                           key_pressed=key_pressed)
		hover_list.append(hover)

		back, hover = menu_button('Back',
		                          black,
		                          red,
		                          (top_left_x, title_box_bottom + 4 * gap + 3 * height),
		                          (top_left_x + width, title_box_bottom + 4 * gap + 4 * height),
		                          size='medium',
		                          tracker=tracker,
		                          intended_tracker_pos=4,
		                          key_pressed=key_pressed)
		hover_list.append(hover)

		game_exit, hover = menu_button('Quit',
		                               black,
		                               red,
		                               (top_left_x, title_box_bottom + 5 * gap + 4 * height),
		                               (top_left_x + width, title_box_bottom + 5 * gap + 5 * height),
		                               size='medium',
		                               tracker=tracker,
		                               intended_tracker_pos=5,
		                               key_pressed=key_pressed)
		hover_list.append(hover)

		hover = max(hover_list)

		if hover:
			tracker = hover

		if res_1:
			res_change = 800, 600
		elif res_2:
			res_change = 800, 800
		elif res_3:
			res_change = 1000, 800
		elif game_exit:
			pygame.quit()
			quit()

		pygame.display.update()
		clock.tick(30)


def row_viruses():
	pass


def col_viruses():
	pass


def colour_selection(colours_click, virus_list, colour_selected=None):
	if not colours_click:
		return False
	elif (True in colours_click) or colour_selected in colour_list:
		if colour_selected not in colour_list:
			colour_index = colours_click.index(True)
			colour_selected = virus_colours[colour_index]

		for virus_index in range(len(virus_list)):
			if virus_index in main_indexes:
				# The coords of each colour is ((x%num_row)-1, x//num_row), x = index of colour + 1
				colour_list[virus_index] = colour_selected
				virus_coords = [((virus_index + 1) % number_viruses_row) - 1,
				                (virus_index + 1) // number_viruses_column]
				if virus_coords[0] < 0:
					virus_coords = number_viruses_row - 1, virus_coords[1] - 1

				# Checks the neighbouring cells to see if they are the selected colour
				next_virus_coords = [[virus_coords[0] - 1, virus_coords[1]],
				                     [virus_coords[0], virus_coords[1] - 1],
				                     [virus_coords[0] + 1, virus_coords[1]],
				                     [virus_coords[0], virus_coords[1] + 1]]
				for coords in next_virus_coords:
					if 0 <= coords[0] < number_viruses_row and 0 <= coords[1] < number_viruses_column:
						# Converts the coordinates to the corresponding index value
						next_virus_index = number_viruses_row * coords[1] + coords[0]
						if virus_list[
							next_virus_index].colour == colour_selected and next_virus_index not in main_indexes:
							main_indexes.add(next_virus_index)
							colour_selection([1], virus_list, colour_selected)


def game_menu(virus_list):
	num_of_buttons = 4

	gap = display_height / 15

	width = (display_width / 4) * (3 / 4)
	height = (display_height - gap * (1 + num_of_buttons)) / num_of_buttons

	clicks = list()

	clicks.append(button("",
	                     red,
	                     red,
	                     ((display_width - 4 * width) / 8, gap),
	                     ((display_width + 4 * width) / 8, gap + height),
	                     size='medium'))

	clicks.append(button("",
	                     green,
	                     green,
	                     ((display_width - 4 * width) / 8, 2 * gap + height),
	                     ((display_width + 4 * width) / 8, 2 * gap + 2 * height),
	                     size='medium'))

	clicks.append(button("",
	                     blue,
	                     blue,
	                     ((display_width - 4 * width) / 8, 3 * gap + 2 * height),
	                     ((display_width + 4 * width) / 8, 3 * gap + 3 * height),
	                     size='medium'))

	clicks.append(button("",
	                     purple,
	                     purple,
	                     ((display_width - 4 * width) / 8, 4 * gap + 3 * height),
	                     ((display_width + 4 * width) / 8, 4 * gap + 4 * height),
	                     size='medium'))
	colour_selection(clicks, virus_list)


# colour_selection(clicks, virus_list)


def highlight(colour,
              brighter,
              outline=(),
              outline_thickness=5,
              colour_msg=black):
	if outline:  # places the outline
		x1 = outline[0] - outline_thickness
		y1 = outline[1] - outline_thickness
		x2 = outline[2] + outline_thickness
		y2 = outline[3] + outline_thickness
		Display.fill(colour_msg, rect=[x1,
		                               y1,
		                               x2 - x1,
		                               y2 - y1])

	colour = list(colour)
	# Makes the colours a little brighter when hovered over
	colour[0] += brighter
	colour[1] += brighter
	colour[2] += brighter
	for value in range(len(colour)):
		if colour[value] > 255:
			# So the value doesn't exceed 255
			colour[value] = 255
	colour = tuple(colour)
	return colour


def menu_button(msg,
                colour_msg,
                colour_button,
                button_top_left,
                button_bottom_right,
                y_displace=0,
                x_displace=0,
                size='small',
                brighter=15,
                tracker=0,
                intended_tracker_pos=1,
                key_pressed=False):
	if tracker == intended_tracker_pos:

		action, hover = button(msg,
		                       colour_msg,
		                       colour_button,
		                       button_top_left,
		                       button_bottom_right,
		                       y_displace,
		                       x_displace,
		                       size,
		                       brighter,
		                       key_cursor=True,
		                       menu=True)
		if key_pressed:
			action = True
	else:
		action, hover = button(msg,
		                       colour_msg,
		                       colour_button,
		                       button_top_left,
		                       button_bottom_right,
		                       y_displace,
		                       x_displace,
		                       size,
		                       brighter,
		                       key_cursor=False,
		                       menu=True)
	if hover:
		hover = intended_tracker_pos
	else:
		hover = 0
	return action, hover


def button(msg,
           colour_msg,
           colour_button,
           button_top_left,
           button_bottom_right,
           y_displace=0,
           x_displace=0,
           size='small',
           brighter=15,
           outline_thickness=5,
           key_cursor=False,
           menu=False):
	text_surf, text_rect = text_object(msg, colour_msg, size)
	hover = False
	clicked = False

	x1, y1 = button_top_left
	x2, y2 = button_bottom_right

	mouse_x, mouse_y = pygame.mouse.get_pos()

	# Ensures that the button highlights when hovered over
	if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
		colour_button = highlight(colour_button,
		                          brighter,
		                          outline=(x1, y1, x2, y2),
		                          outline_thickness=outline_thickness,
		                          colour_msg=colour_msg)

		if mouse_1:
			clicked = True
		if menu:
			hover = True

	# Tracking the cursor being moved by the arrow keys
	elif key_cursor:
		colour_button = highlight(colour_button,
		                          brighter,
		                          outline=(x1, y1, x2, y2),
		                          outline_thickness=outline_thickness,
		                          colour_msg=colour_msg)

	Display.fill(colour_button, rect=[x1,
	                                  y1,
	                                  x2 - x1,
	                                  y2 - y1])

	text_rect.center = (x2 + x1) / 2 + x_displace, \
	                   (y2 + y1) / 2 + y_displace
	Display.blit(text_surf, text_rect)

	if menu:
		return clicked, hover
	else:
		return clicked


def text_object(text, colour, size):
	if size == 'small':
		text_surface = small_font.render(text, True, colour)
	elif size == 'medium':
		text_surface = med_font.render(text, True, colour)
	else:
		text_surface = large_font.render(text, True, colour)
	return text_surface, text_surface.get_rect()


def message_to_screen(msg,
                      colour,
                      y_displace=0,
                      x_displace=0,
                      size='small',
                      side='center'):
	"""
	Each 'side' differs in their starting positions,
	point of the text box being controlled and
	in the direction of the displacements

	The name od the 'side' indicates the starting position as well as
	the point of the text box being controlled

	Center: Pygame directions
	Top: Pygame directions
	Bottom Left: Negative y
	Bottom Right: Negative y and Negative x
	:param msg:
	:param colour:
	:param y_displace:
	:param x_displace:
	:param size:
	:param side:
	:return:
	"""
	text_surf, text_rect = text_object(msg, colour, size)
	if side == 'center':
		text_rect.center = (display_width / 2) + x_displace, \
		                   (display_height / 2) + y_displace
	elif side == 'top':
		text_rect.midtop = (display_width / 2) + x_displace, y_displace
	elif side == 'bottom_left':
		text_rect.bottomleft = (x_displace,
		                        display_height - y_displace)
	elif side == 'bottom_right':
		text_rect.bottomright = (display_width - x_displace,
		                         display_height - y_displace)
	Display.blit(text_surf, text_rect)


def message_box_data(msg,
                     colour,
                     y_displace=0,
                     x_displace=0,
                     size='small',
                     side='center'):
	"""
	Each 'side' differs in their starting positions,
	point of the text box being controlled and
	in the direction of the displacements

	The name od the 'side' indicates the starting position as well as
	the point of the text box being controlled

	Center: Pygame directions
	Top: Pygame directions
	Bottom Left: Negative y
	Bottom Right: Negative y and Negative x

	This function does not draw to the screen
	:param msg:
	:param colour:
	:param y_displace:
	:param x_displace:
	:param size:
	:param side:
	:return:
	"""
	text_surf, text_rect = text_object(msg, colour, size)
	if side == 'center':
		text_rect.center = (display_width / 2) + x_displace, \
		                   (display_height / 2) + y_displace
	elif side == 'top':
		text_rect.midtop = (display_width / 2) + x_displace, y_displace
	elif side == 'bottom_left':
		text_rect.bottomleft = (x_displace,
		                        display_height - y_displace)
	elif side == 'bottom_right':
		text_rect.bottomright = (display_width - x_displace,
		                         display_height - y_displace)

	answer_dict = {'Top': text_rect.top, 'Bottom': text_rect.bottom, 'Left': text_rect.left,
	               'Right': text_rect.right, 'Center': text_rect.center}
	return answer_dict


def instructions():
	message_to_screen("Press P to pause",
	                  white,
	                  y_displace=cell_gap_y / 4,
	                  x_displace=(display_width / 4) + (cell_gap_x / 4),
	                  side='bottom_left')
	message_to_screen("Resolution: {}, {}".format(display_width, display_height),
	                  white,
	                  y_displace=cell_gap_y / 4,
	                  x_displace=cell_gap_x / 4,
	                  side='bottom_right')
	message_to_screen("Number of Moves Left: {}".format('infinite'),
	                  white,
	                  x_displace=display_width / 8,
	                  y_displace=cell_gap_y / 4,
	                  side='top')


def game_loop():
	global mouse_1
	global main_indexes
	game_exit = False

	while not game_exit:

		mouse_1 = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_exit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					paused()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mouse_1 = True

		Display.fill(grey)

		Display.fill(ochre, rect=[0, 0, display_width / 4, display_height])

		virus_list = generate_viruses(colour_list, number_viruses_row, number_viruses_column)

		game_menu(virus_list)

		instructions()

		pygame.display.update()
		clock.tick(30)

	pygame.quit()
	quit()


game_loop()
