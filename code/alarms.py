import pygame


class Alarm:
    def __init__(self, tier, trigger_probability, damage_constant, resolution, sound_file_name, activated=False, silence=False):
        self.tier = tier
        self.trigger_probability = trigger_probability
        self.damage_constant = damage_constant
        self.resolution = resolution
        self.sound = pygame.mixer.Sound(sound_file_name)
        self.activated = activated
        self.silence = silence

    def trigger(self):
        # Trigger the alarm
        self.activated = True

        # If the alarm is not silenced, play the alarm sound
        if self.silence is False:
            self.sound.play()

    def mute(self):
        # Silence the alarm
        self.silence = True
