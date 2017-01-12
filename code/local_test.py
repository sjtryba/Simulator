import pygame
import time


pygame.mixer.init()

master_alarm = pygame.mixer.Sound('stage_1_ignition.ogg')
# master_alarm = pygame.mixer.Sound('alarm_master.ogg')

master_alarm.play()
time.sleep(30)

