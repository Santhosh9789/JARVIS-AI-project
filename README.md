# Jarvis AI - A Voice-Controlled Assistant

This project aims to develop Jarvis AI, an intelligent voice-controlled assistant. Inspired by the concept of a comprehensive AI that can manage and control various aspects of a smart environment, this project will incrementally build towards that vision.

## Features

### Current Capabilities
- **Voice Command Recognition**: Understands and processes spoken commands.
- **Simulated Device Control**: Can control basic simulated devices (e.g., a light).
- **Voice Feedback**: Provides spoken responses and confirmations.
- **Exit Command**: Allows for graceful shutdown of the assistant.

### Planned Enhancements (Short-Term)
- **Expanded Device Control**: Adding more simulated devices like a fan and a thermostat.
- **Richer Command Set**: Increasing the vocabulary of understood commands for new devices.
- **Basic Self-Update Check**: A command to simulate checking for software updates, laying the groundwork for future automated updates.
- **Modular Codebase**: Refactoring for easier expansion.

## Future Vision

The long-term goal for Jarvis AI is to become a more sophisticated assistant with:
- **Advanced AI learning**: Potential for self-improvement and adaptation.
- **Wider Device Ecosystem**: Control over a broader range of (simulated or real) electronic products.
- **Enhanced Conversational Abilities**: More natural and context-aware interactions.

## Logging
The application logs key events and errors to `voice_assistant.log`.
This includes:
- Application start and stop.
- Received voice commands.
- Parsed command actions.
- Device interactions.
- Errors encountered during speech recognition, command parsing, or TTS.
- Unhandled exceptions within the main loop.

This log file is useful for debugging and tracing the application's behavior.
