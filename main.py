from voice_assistant.core.voice_input import listen_for_command
from voice_assistant.core.command_parser import parse_command
from voice_assistant.core.device_control import SimulatedLight, SimulatedFan, SimulatedThermostat
from voice_assistant.core.voice_output import speak
import time
import logging

# --- Logging Setup ---
LOG_FILE = "voice_assistant.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
# --- End Logging Setup ---

def check_for_updates():
    logging.info("User requested to check for updates.")
    speak("Checking for updates...")
    try:
        time.sleep(2)
        logging.info("Update check complete. No new updates available.")
        speak("No new updates available at the moment.")
    except Exception as e:
        logging.error(f"Error during simulated update check: {e}")
        speak("Sorry, I encountered an error while checking for updates.")

# --- Command Handler Functions ---
def handle_exit(parsed_command, devices, shared_state):
    speak("Goodbye!")
    logging.info("Exit command received. Shutting down.")
    shared_state['running'] = False

def handle_check_updates(parsed_command, devices, shared_state):
    check_for_updates()

def handle_turn_on(parsed_command, devices, shared_state):
    target_name = parsed_command.get('target')
    if not target_name or target_name not in devices:
        logging.warning(f"Target '{target_name}' not found or not specified for turn_on.")
        speak(f"Sorry, I don't know how to turn on '{target_name if target_name else 'that'}'.")
        return

    device = devices[target_name]
    # Assuming device_name attribute exists on all device objects
    device_display_name = getattr(device, 'device_name', target_name)
    logging.info(f"Action: turn_on, Target: {device_display_name}")

    # Assumes get_status() returns True if on, False if off for on/off devices
    if hasattr(device, 'get_status') and not device.get_status():
        speak(f"Okay, turning the {device_display_name} on.")
        if hasattr(device, 'turn_on'):
            device.turn_on()
        else:
            logging.error(f"Device {device_display_name} does not have a turn_on method.")
            speak(f"Sorry, I can't turn on the {device_display_name}.")
    elif hasattr(device, 'get_status') and device.get_status():
        speak(f"The {device_display_name} is already on.")
    elif not hasattr(device, 'get_status'): # For devices without on/off status like thermostat for this action
        logging.warning(f"Device {device_display_name} cannot be 'turned on' in the typical sense.")
        speak(f"Sorry, I can't 'turn on' the {device_display_name} like that.")


def handle_turn_off(parsed_command, devices, shared_state):
    target_name = parsed_command.get('target')
    if not target_name or target_name not in devices:
        logging.warning(f"Target '{target_name}' not found or not specified for turn_off.")
        speak(f"Sorry, I don't know how to turn off '{target_name if target_name else 'that'}'.")
        return

    device = devices[target_name]
    device_display_name = getattr(device, 'device_name', target_name)
    logging.info(f"Action: turn_off, Target: {device_display_name}")

    if hasattr(device, 'get_status') and device.get_status():
        speak(f"Okay, turning the {device_display_name} off.")
        if hasattr(device, 'turn_off'):
            device.turn_off()
        else:
            logging.error(f"Device {device_display_name} does not have a turn_off method.")
            speak(f"Sorry, I can't turn off the {device_display_name}.")
    elif hasattr(device, 'get_status') and not device.get_status():
        speak(f"The {device_display_name} is already off.")
    elif not hasattr(device, 'get_status'):
        logging.warning(f"Device {device_display_name} cannot be 'turned off' in the typical sense.")
        speak(f"Sorry, I can't 'turn off' the {device_display_name} like that.")


def handle_set_temperature(parsed_command, devices, shared_state):
    target_name = parsed_command.get('target')
    if target_name != 'thermostat' or target_name not in devices:
        logging.warning(f"Target '{target_name}' is not a thermostat or not found for set_temperature.")
        speak("Sorry, I can only set temperature for a thermostat.")
        return

    thermostat = devices[target_name]
    device_display_name = getattr(thermostat, 'device_name', target_name)
    temp_value = parsed_command.get('value')

    if temp_value is None:
        logging.warning("Temperature value not provided for set_temperature.")
        speak("Sorry, you need to specify a temperature.")
        return

    logging.info(f"Action: set_temperature, Target: {device_display_name}, Value: {temp_value}")
    if hasattr(thermostat, 'set_temperature'):
        thermostat.set_temperature(temp_value)
        speak(f"Okay, setting the {device_display_name} to {temp_value} degrees.")
    else:
        logging.error(f"Device {device_display_name} does not have a set_temperature method.")
        speak(f"Sorry, I can't set the temperature for the {device_display_name}.")


# --- Main Application ---
if __name__ == "__main__":
    logging.info("Voice assistant application started.")

    my_light = SimulatedLight("desk lamp")
    my_fan = SimulatedFan("living room fan")
    my_thermostat = SimulatedThermostat("hallway thermostat")

    devices = {
        "lights": my_light,
        "fan": my_fan,
        "thermostat": my_thermostat
    }

    command_handlers = {
        "exit": handle_exit,
        "check_updates": handle_check_updates,
        "turn_on": handle_turn_on,
        "turn_off": handle_turn_off,
        "set_temperature": handle_set_temperature,
    }

    speak("Voice assistant activated. How can I help you?")
    logging.info("Voice assistant activated. How can I help you?")

    shared_state = {'running': True}
    while shared_state['running']:
        command_text = None
        try:
            try:
                command_text = listen_for_command()
            except OSError as e:
                logging.warning(f"Audio input error (OSError): {e} - Likely no microphone in sandbox.")
            except Exception as e:
                logging.error(f"An unexpected error occurred during voice input: {e}", exc_info=True)

            if command_text:
                logging.info(f"Heard: \"{command_text}\"")
                parsed_command = parse_command(command_text)

                if parsed_command:
                    logging.info(f"Parsed: {parsed_command}")
                    action = parsed_command.get('action')

                    if action in command_handlers:
                        handler = command_handlers[action]
                        handler(parsed_command, devices, shared_state)
                    else:
                        # This case handles when action is not None but not in command_handlers
                        # or if parsed_command has an action that's recognized but target might be missing/invalid for some handlers
                        logging.warning(f"No specific handler for action: '{action}' or unhandled command structure: {parsed_command}")
                        speak("Sorry, I'm not sure how to handle that specific request. I can control lights, fan, thermostat, or check for updates.")
                else:
                    logging.warning(f"Command not understood by parser: \"{command_text}\"")
                    speak("Sorry, I didn't understand that. Please try again.")
            else:
                if shared_state['running']: # Avoid speaking if already exiting
                    logging.info("No command received or error in listening.")
                    # Potentially reduce frequency of this message or make it less intrusive
                    # speak("I didn't catch that. Could you please repeat?") # This can be annoying if mic is off

            if shared_state['running']:
                logging.debug(f"Current {my_light.device_name} status: {'ON' if my_light.get_status() else 'OFF'}")
                logging.debug(f"Current {my_fan.device_name} status: {'ON' if my_fan.get_status() else 'OFF'}")
                # Assuming SimulatedThermostat has a get_status() that returns its state string
                thermostat_status_method = getattr(my_thermostat, 'get_status', None)
                if callable(thermostat_status_method):
                    logging.debug(f"Current {my_thermostat.device_name} status: {my_thermostat.get_status()}")


        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}", exc_info=True)
            speak("An unexpected error occurred. Please try again.")
            # time.sleep(1) # Prevent rapid-fire error messages

    logging.info("Voice assistant application stopped.")
