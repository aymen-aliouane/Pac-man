from mazegenerator.mazegenerator import MazeGenerator
import pygame
import time


def initialise() -> pygame.Surface:
	pygame.init()
	w, h = 500, 500

	screen = pygame.display.set_mode((w,h))
	pygame.display.set_caption("Pac-man")

	return screen


def game():
	screen = initialise()
	gen = MazeGenerator()
	run = True
	move = 5
	clock = pygame.time.Clock()
	past_time = time.time()
	FPS = 60

	rec = pygame.rect.Rect(0,250, 50, 50)

	while run:
		screen.fill((0,0,0))
		clock.tick(FPS)

		actual_time = time.time()
		dt = actual_time - past_time
		past_time = actual_time

		if move:
			# the dt normalise the speed
			# the 60 let us use the normal velocity by canceling dt
			rec.x += move * dt * 60

		pygame.draw.rect(screen, (255, 255, 255), rec)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					move = 5
				elif event.key == pygame.K_LEFT:
					move = -5
				elif event.key == pygame.K_ESCAPE:
					run = False


		pygame.display.flip()
		# replace it later with pygame.display.update() for optimisation
	pygame.quit()


if __name__ == "__main__":
	game()