import sys
sys.path.append('../')  # Hinzufügen des übergeordneten Verzeichnisses zum Python-Pfad

from sensor_manager import SensorManager
from logger import setup_logger

config_file = '../config.ini'

logger = setup_logger("flaskserver")

sensor_manager = SensorManager(config_file, logger)
logger.debug("Warte auf Trigger...")
sensor_manager.wait_for_door_openening()  # Warte auf das Öffnen der Tür - Blocking
logger.debug("Trigger wurde ausgelöst!")

