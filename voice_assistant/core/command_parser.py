import re

def parse_command(command_text: str) -> dict | None:
    if not command_text:
        return None

    command_text_lower = command_text.lower()

    # 1. Exact match commands (highest priority)
    exact_commands = {
        "exit": {'action': 'exit'},
        "goodbye": {'action': 'exit'},
        "quit": {'action': 'exit'},
        "stop listening": {'action': 'exit'},
    }
    if command_text_lower in exact_commands:
        return exact_commands[command_text_lower]

    # 2. Regex-based commands (for parameterized commands)
    # Thermostat: "set (the) thermostat to XX (degrees)"
    thermostat_match = re.search(r"set (?:the )?thermostat to (\d+)(?: degrees)?", command_text_lower)
    if thermostat_match:
        temperature = int(thermostat_match.group(1))
        return {'action': 'set_temperature', 'target': 'thermostat', 'value': temperature}

    # 3. Substring-based commands (general commands)
    # Order matters here if there's potential overlap; more specific phrases first.
    substring_commands = {
        # Lights
        "turn on the lights": {'action': 'turn_on', 'target': 'lights'},
        "lights on": {'action': 'turn_on', 'target': 'lights'},
        "turn off the lights": {'action': 'turn_off', 'target': 'lights'},
        "lights off": {'action': 'turn_off', 'target': 'lights'},
        # Fan
        "turn on fan": {'action': 'turn_on', 'target': 'fan'},
        "fan on": {'action': 'turn_on', 'target': 'fan'},
        "turn off fan": {'action': 'turn_off', 'target': 'fan'},
        "fan off": {'action': 'turn_off', 'target': 'fan'},
        # Updates
        "check for updates": {'action': 'check_updates'},
        "are there any updates": {'action': 'check_updates'}, # "are there any updates?" - remove question mark for simpler matching
        "update check": {'action': 'check_updates'},
    }

    # Check for substring commands (iterate to allow multiple phrases for one command pair)
    # To make it more robust, we could sort keys by length descending if needed,
    # but for this set, simple iteration should be fine.
    for phrase, result in substring_commands.items():
        if phrase in command_text_lower:
            return result

    return None

if __name__ == '__main__':
    tests = [
        "turn on the lights",
        "lights on",
        "please turn on the lights", # substring match
        "turn off the lights",
        "lights off",
        "exit",
        "goodbye",
        "quit",
        "stop listening",
        "turn the fan on", # should match "fan on" or "turn on fan"
        "fan on please",   # substring match
        "turn off fan",
        "fan off",
        "set thermostat to 22 degrees",
        "set the thermostat to 20",
        "set thermostat to 70",
        "could you set thermostat to 18 degrees for me?", # substring match
        "check for updates",
        "please check for updates",
        "are there any updates available?", # substring match for "are there any updates"
        "perform an update check", # substring match for "update check"
        "what's the weather?", # No match
        "",
        None,
        "please exit the program", # No match (exact for exit)
        "turn off the lights then exit" # Should match lights off
    ]

    for test_input in tests:
        output = parse_command(test_input)
        print(f"Input: \"{test_input}\", Output: {output}")

    print("\nTesting edge cases and priorities:")
    print(f"Input: \"exit please\", Output: {parse_command('exit please')}") # None
    print(f"Input: \"exit\", Output: {parse_command('exit')}") # Exit
    # Test thermostat vs. other general commands if there was an overlap
    # (not an issue with current keywords)
    print(f"Input: \"set the thermostat to 25 degrees and turn on fan\", Output: {parse_command('set the thermostat to 25 degrees and turn on fan')}") # Should match thermostat
    print(f"Input: \"turn on fan and set the thermostat to 25 degrees\", Output: {parse_command('turn on fan and set the thermostat to 25 degrees')}") # Should match fan on (due to order of check if regex was in the same loop)
                                                                                                                                                    # With current structure, it should be fine as regex is checked first.
                                                                                                                                                    # Actually, with the new structure, it will match "set thermostat..." first.
                                                                                                                                                    # If it was "turn on fan and set the lights to blue", it would match "turn on fan".
