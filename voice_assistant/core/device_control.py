import logging

# Configure logging for this module (optional, but good practice)
# If main.py already configures root logger, this might not be strictly necessary
# but won't hurt.
logger = logging.getLogger(__name__)
if not logger.handlers: # Avoid adding multiple handlers if already configured
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO) # Or whatever level is appropriate

class SimulatedLight:
    """
    A class to simulate a controllable light.
    """
    def __init__(self, device_name: str):
        """
        Initializes the simulated light.

        Args:
            device_name (str): The name of the light device.
        """
        self.device_name = device_name
        self.is_on = False
        logger.info(f"[SimulatedLight {self.device_name}] initialized. Currently OFF.")

    def turn_on(self):
        """
        Turns the light on.
        """
        if not self.is_on:
            self.is_on = True
            logger.info(f"[SimulatedLight {self.device_name}] is now ON.")
        else:
            logger.info(f"[SimulatedLight {self.device_name}] is already ON.")

    def turn_off(self):
        """
        Turns the light off.
        """
        if self.is_on:
            self.is_on = False
            logger.info(f"[SimulatedLight {self.device_name}] is now OFF.")
        else:
            logger.info(f"[SimulatedLight {self.device_name}] is already OFF.")

    def get_status(self) -> bool:
        """
        Returns the current state of the light.

        Returns:
            bool: True if the light is on, False otherwise.
        """
        return self.is_on

class SimulatedFan:
    """
    A class to simulate a controllable fan.
    """
    def __init__(self, device_name: str):
        """
        Initializes the simulated fan.

        Args:
            device_name (str): The name of the fan device.
        """
        self.device_name = device_name
        self.is_on = False
        logger.info(f"[SimulatedFan {self.device_name}] initialized. Currently OFF.")

    def turn_on(self):
        """
        Turns the fan on.
        """
        if not self.is_on:
            self.is_on = True
            logger.info(f"[SimulatedFan {self.device_name}] is now ON.")
        else:
            logger.info(f"[SimulatedFan {self.device_name}] is already ON.")

    def turn_off(self):
        """
        Turns the fan off.
        """
        if self.is_on:
            self.is_on = False
            logger.info(f"[SimulatedFan {self.device_name}] is now OFF.")
        else:
            logger.info(f"[SimulatedFan {self.device_name}] is already OFF.")

    def get_status(self) -> bool:
        """
        Returns the current state of the fan.

        Returns:
            bool: True if the fan is on, False otherwise.
        """
        return self.is_on

class SimulatedThermostat:
    """
    A class to simulate a controllable thermostat.
    """
    def __init__(self, device_name: str, initial_temp: int = 20):
        """
        Initializes the simulated thermostat.

        Args:
            device_name (str): The name of the thermostat device.
            initial_temp (int): The initial temperature in Celsius.
        """
        self.device_name = device_name
        self.current_temperature = initial_temp
        logger.info(f"[SimulatedThermostat {self.device_name}] initialized. Temperature set to {self.current_temperature}°C.")

    def set_temperature(self, degrees: int):
        """
        Sets the thermostat's target temperature.

        Args:
            degrees (int): The target temperature in Celsius.
        """
        self.current_temperature = degrees
        logger.info(f"[SimulatedThermostat {self.device_name}] temperature set to {self.current_temperature}°C.")

    def get_temperature(self) -> int:
        """
        Returns the current target temperature of the thermostat.

        Returns:
            int: The current temperature in Celsius.
        """
        return self.current_temperature

    def get_status(self) -> str:
        """
        Returns a descriptive status of the thermostat.

        Returns:
            str: A string describing the thermostat's current temperature.
        """
        return f"[SimulatedThermostat {self.device_name}] is set to {self.current_temperature}°C."


if __name__ == '__main__':
    # Re-configure logger for testing if it's not picked up from module level
    # This ensures test output is visible
    if not logger.handlers or not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        # If adding a new handler, make sure not to duplicate if root is already configured
        if not logging.getLogger().handlers: # Check root logger
             logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    logger.info("--- Testing SimulatedLight ---")
    lamp = SimulatedLight("Bedroom Lamp")
    logger.info(f"Initial status: {'ON' if lamp.get_status() else 'OFF'}")
    lamp.turn_on()
    logger.info(f"Status after turning on: {'ON' if lamp.get_status() else 'OFF'}")
    lamp.turn_on() # Try turning on again
    lamp.turn_off()
    logger.info(f"Status after turning off: {'ON' if lamp.get_status() else 'OFF'}")
    lamp.turn_off() # Try turning off again
    logger.info(f"Final status: {'ON' if lamp.get_status() else 'OFF'}")
    print("-" * 30)

    logger.info("--- Testing SimulatedFan ---")
    fan = SimulatedFan("Living Room Fan")
    logger.info(f"Initial status: {'ON' if fan.get_status() else 'OFF'}")
    fan.turn_on()
    logger.info(f"Status after turning on: {'ON' if fan.get_status() else 'OFF'}")
    fan.turn_on()
    fan.turn_off()
    logger.info(f"Status after turning off: {'ON' if fan.get_status() else 'OFF'}")
    fan.turn_off()
    logger.info(f"Final status: {'ON' if fan.get_status() else 'OFF'}")
    print("-" * 30)

    logger.info("--- Testing SimulatedThermostat ---")
    thermostat = SimulatedThermostat("Hallway Thermostat", initial_temp=22)
    logger.info(f"Initial status: {thermostat.get_status()}")
    logger.info(f"Current temperature: {thermostat.get_temperature()}°C")
    thermostat.set_temperature(25)
    logger.info(f"Status after setting temp: {thermostat.get_status()}")
    logger.info(f"Current temperature: {thermostat.get_temperature()}°C")
    thermostat.set_temperature(18)
    logger.info(f"Status after setting temp again: {thermostat.get_status()}")
    logger.info(f"Current temperature: {thermostat.get_temperature()}°C")
    print("-" * 30)
