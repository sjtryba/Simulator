import pygame


class Alarm:
    def __init__(self, tier, trigger_probability, damage_constant, resolution, sound_file_name, activate=False, silence=False):
        self.tier = tier
        self.trigger_probability = trigger_probability
        self.damage_constant = damage_constant
        self.resolution = resolution
        self.sound = pygame.mixer.Sound(sound_file_name)
        self.activate = activate
        self.silence = silence

    def trigger(self):
        # Trigger the alarm
        self.activate = True

        # If the alarm is not silenced, play the alarm sound
        if self.silence is False:
            self.sound.play()

    def mute(self):
        # Mute the alarm
        self.silence = True

    def update(self):
        if self.activate:
            if pygame.mixer.get_busy():
                if self.silence:
                    pygame.mixer.stop()
            else:
                if self.silence is False:
                    self.sound.play()
