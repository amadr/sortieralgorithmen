import pygame
import random
pygame.init()

# Klasse DrawInformation fuer Deklarierung der Farben, der Schriftart und den Koordinaten fuer das Zeichnen.
class DrawInformation:
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = 50, 50, 50

	GRAY_GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('arial', 30)
	LARGE_FONT = pygame.font.SysFont('arial', 40, 'bold')
	SMALL_FONT = pygame.font.SysFont('arial', 15)

    #freier Platz an den Seiten
	SIDE_PAD = 100
	TOP_PAD = 150

	# Konstruktor
	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		# Erstellen des Fesnters
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sortieralgorithmen Visualisierung")
		
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

        # Flaeche die an den Seiten frei gehalten werden soll
		# Breite eines Elements der Liste
		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = int((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2

# Methode fuer das Zeichnen des Hintergrunds und des Textes 
def draw(draw_info, algo_name, ascending, n, sort_speed):
	# Zeichnen des Hintergrunds
	draw_info.screen.fill(draw_info.BACKGROUND_COLOR)

	# Ein Bild/ Oberflaeche des Textes kreieren
	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Aufsteigend' if ascending else 'Absteigend'}", 1, draw_info.WHITE)
	# Zeichnen des Bildes in dem Fenster (auf dem Hintergrund)
	draw_info.screen.blit(title, (draw_info.width/2 - title.get_width()/2, 0))

	controls = draw_info.FONT.render("R - Reset | SPACE - Starten | A - Aufsteigend | D - Absteigend", 1, draw_info.GRAY_GRADIENTS[2])
	draw_info.screen.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

	sorting = draw_info.FONT.render("B - Bubble Sort | I - Insertion Sort | S - Selection Sort", 1, draw_info.GRAY_GRADIENTS[2])
	draw_info.screen.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 80))

	third_row = draw_info.FONT.render(f"{'N - Anzahl Elem.:'} {n} {' | P - Geschwindigkeit:'} {sort_speed}", 1, draw_info.GRAY_GRADIENTS[2])
	draw_info.screen.blit(third_row, (draw_info.width/2 - third_row.get_width()/2, 110))
	
	draw_list(draw_info)
	pygame.display.update()

# Methode fuer das Zeichen der Liste
def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	# Neuzeichnen des Hintergrunds in dem Bereich, wo die Liste gezeichnet wird
	if clear_bg:
		# rect(x_0, y_0, w, h)
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		# Rect(surface, color, rect)
		pygame.draw.rect(draw_info.screen, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		# x und y Koordinaten des zu zeichnenden Elements der Liste ermitteln
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
		
		# Wechseln der Grautoene
		color = draw_info.GRAY_GRADIENTS[i % 3]
		
		# Fuer die zu vertauschenden Elemente die Farben rot bzw. gruen einstellen
		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.screen, color, (x, y, draw_info.block_width, draw_info.height))
		num = draw_info.SMALL_FONT.render(str(val), 1, color)
		draw_info.screen.blit(num, (x, y-20))

	if clear_bg:
		pygame.display.update()

# Methode fuer das Generieren einer zufaelligen Liste mit n Elementen
def generate_list(n, min_val, max_val):
	lst = []
	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)
	return lst

# Bubble Sort
# - vergleicht immer zwei nebeneinanderliegende Elemente und tauscht diese aus, falls noetig
# 1. Vergleiche aktuelles Element mit dem rechten Nachbarn
# 2. Falls das Sortierkriterium verletzt wird, werden sie getauscht
# 3. Widerholen, bis der rechte Nachbar des aktuellen Elements bereits zum sortierten Teil gehoert
# 4. So oft wiederholen, bis ganze Liste sortiert ist
def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst
	# Durch alle Elemente iterieren
	for i in range(len(lst) - 1):
		# das letzte Element ist schon auf der richtigen Stelle, deshalb -i, 
		# damit nur bis zum letzten unsortiertem Element iteriert wird
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]
			
			# Falls das linke Elemet groesser bzw. kleiner bei absteigend als das rechte ist, dann vertauschen 
			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True
	return lst

# Insertion Sort
# - das 1. Element gilt als sortiert
# - das erste Element der unsrtierten Liste wird mit der breits sortierten Liste verglichen und an der richtigen Stelle eingefuegt
def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst
	# Iterieren von 2. bis zum letzten Element (1. Element bereits sortiert)
	# i zeigt immer auf das erste Element der rechten unsortierten Liste
	for i in range(1, len(lst)):
		current = lst[i]
		# Elemente der Liste[1..i-1], die groesser als das aktuelle Element (am Anfang 1. Element der unsortierten Liste, dann rutscht immer eins weiter nach links) 
		# sind, eine Position nach recthts verschieben und das aktuelle Element nach links
		# bzw. andersherum bei absteigend
		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i -= 1
			lst[i] = current
			draw_list(draw_info, {i: draw_info.GREEN, i-1: draw_info.RED}, True)
			yield True
	return lst

# Selection Sort
# - kleinstes Element in unsortierten Teil suchen
# - kleinstes Element mit erstem Element der unsortierten Liste tauschen
def selection_sort(draw_info, ascending):
	lst = draw_info.lst
	# Laenge des aktuellen sortieren Teils
	sorted_len = 0
	while sorted_len < len(lst):
		# Index vom kleinsten/ groessten gefundenen Element
		idx = None
		# Iteration durch den unsortierten Teil der Liste
		for i, elem in enumerate(lst[sorted_len:]):
			# Ueberpruefen ob elem das kleinste/ groesste ist
			if (idx == None) or (elem < lst[idx] and ascending) or (elem > lst[idx] and not ascending):
				#Index des kleinsten/ groessten Elements aktualisieren
				idx = i + sorted_len
		# Vertauschen des kleinsten/ groessten Elements der unsortieren Liste mit dem ersten Element der unsortierten Liste
		lst[idx], lst[sorted_len] = lst[sorted_len], lst[idx]
		draw_list(draw_info, {sorted_len: draw_info.GREEN, idx: draw_info.RED}, True)
		# Erhoehen der Laenge des sortierten Teils um 1 bzw. erniedrigen der Laenge des unsortierten Teils
		sorted_len += 1
		yield True
	return lst
	
# Main
def main():
	run = True
	clock = pygame.time.Clock()

	n = 50
	min_val = 0
	max_val = 100
	
	# Zufaellige Liste fuer den Anfang
	lst = generate_list(n, min_val, max_val)
	draw_info = DrawInformation(800, 600, lst)
	sorting = False
	ascending = True

	sorting_algorithm = selection_sort
	sorting_algo_name = "Selection Sort"
	sorting_algorithm_generator = None

	sort_speed = 10

	while run:
		clock.tick(sort_speed)
		
		# Wenn das sortieren fertig ist, soll nicht mehr sortiert werden
		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		# Falls nicht sortiert wird, soll das Fenster (immer wieder) neugezeichnet werden
		else:
			draw(draw_info, sorting_algo_name, ascending, n, sort_speed)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				
			# Falls eine Taste gedrueckt wird
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					lst = generate_list(n, min_val, max_val)
					draw_info.set_list(lst)
					sorting = False
				elif event.key == pygame.K_SPACE and sorting == False:
					sorting = True
					sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
				elif event.key == pygame.K_a and not sorting:
					ascending = True
				elif event.key == pygame.K_d and not sorting:
					ascending = False
				elif event.key == pygame.K_i and not sorting:
					sorting_algorithm = insertion_sort
					sorting_algo_name = "Insertion Sort"
				elif event.key == pygame.K_b and not sorting:
					sorting_algorithm = bubble_sort
					sorting_algo_name = "Bubble Sort"
				elif event.key == pygame.K_s and not sorting:
					sorting_algorithm = selection_sort
					sorting_algo_name = "Selection Sort"
				elif event.key == pygame.K_n and not sorting:
					n = n%100 + 10
					lst = generate_list(n, min_val, max_val)
					draw_info.set_list(lst)
				elif event.key == pygame.K_p and not sorting:
					sort_speed = sort_speed%100 + 10
					
	pygame.quit()

if __name__ == "__main__":
	main()