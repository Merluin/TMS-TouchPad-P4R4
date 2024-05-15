# TMS-TouchPad-P4R4

Welcome to the TMS-TouchPad-P4R4 repository, the home of an advanced interface designed to enhance Transcranial Magnetic Stimulation (TMS) sessions. This repository includes code and documentation for interfacing TMS equipment with an Arduino-powered control system and a Python-driven GUI application running on a Raspberry Pi.

## Safety and Disclaimer
The TMS-TouchPad-P4R4 is currently an in-progress project. As such, the creators do not assume responsibility for any damages, injuries, or liabilities that may arise from its use. Users must accept all responsibility for outcomes when utilizing this device. We emphasize the importance of this device being operated by individuals who are properly trained and competent in handling TMS and EEG/EMG systems.

## Open to Collaboration
We are keen on collaborating with other researchers and developers. If you are interested in contributing to the project, improving functionalities, or testing its applications in new research settings, please feel free to reach out.

## Overview

The TMS-TouchPad-P4R4 is a versatile device that allows for precise control over TMS parameters via a graphical user interface. It supports connections with EEG and EMG systems and can be utilized in various TMS protocols, including ccPAS. This tool is designed for research environments to streamline the management of TMS sessions.

## Features

- **Arduino Integration**: Manages direct hardware interface for real-time control of TMS protocols.
- **Python GUI**: Offers a user-friendly interface on a Raspberry Pi for easy adjustment of stimulation parameters and session control.
- **Modular Connection**: Compatible with EEG/EMG systems that receive TTL markers.

## Repository Contents

- `R4_ppTMS.ino`: Contains the Arduino script for managing the BNC connectors and real-time TMS serial communication with GUI.
- `ppTMS.py`: Python script for the GUI application facilitating user interaction and parameter configuration.
- `User Manual for TMS TouchPad P4R4.pdf`: Comprehensive guide on setting up and using the device safely and effectively.

## Hardware Setup

- **Serial Communication**: Uses `Serial1.available()` for communication with the R4 board from RX/TX pins. Uses `Serial.available()` for communication with the R4 board from usb cable.

## Support

For issues, queries, or additional support, please contact:

- Email: thomas.quettier2@unibo.it


## Contributing

For collaborators contributing to this repository, please prefix your commit messages with appropriate tags for efficient tracking and management:
- **BF**: Bug Fix - for resolving errors or issues in existing code.
- **FF**: Feature Fix - for fixes to unreleased code features.
- **RF**: Refactoring - for code structure or design modifications.
- **NF**: New Feature - for introducing new functionalities.
- **ENH**: Enhancement - for improvements to existing features or code.
- **DOC**: Documentation - for updates or additions to project documentation.
- **TEST**: Testing - for adding new tests or modifying existing ones. 

Your cooperation and adherence to these guidelines help maintain the quality and integrity of our project. 
