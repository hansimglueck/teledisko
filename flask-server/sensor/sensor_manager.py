from gpiozero import Button
import configparser

class SensorManager:
    def __init__(self, config_file, logger):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        gpio_pin = self.config.getint('GPIO', 'door_switch_pin')
        self.button = Button(gpio_pin)
        self.logger = logger

    def wait_for_door_openening(self):
        self.button.wait_for_press()
        self.logger.debug("door closed")
        self.button.wait_for_release()
        self.logger.debug("door open")

    def wait_for_door_closing(self):
        self.button.wait_for_release()
        self.logger.debug("door open")
        self.button.wait_for_press()
        self.logger.debug("door closed")
