import pygame


pygame.init()
screen = pygame.display.set_mode((900, 600))
done = False

clock = pygame.time.Clock()

master_alarm = pygame.mixer.Sound('stage_1_ignition.ogg')
#master_alarm = pygame.mixer.Sound('alarm_master.ogg')

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            master_alarm.play()

    pygame.display.flip()
