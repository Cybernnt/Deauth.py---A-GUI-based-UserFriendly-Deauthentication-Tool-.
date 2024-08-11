About This Tool

DeAuth.py

Description:
DeAuth.py is a Python-based graphical user interface (GUI) tool designed to perform deauthentication attacks on Wi-Fi networks. It utilizes airmon-ng, airodump-ng, and aireplay-ng tools to scan for nearby networks and perform attacks. This tool provides an easy-to-use interface to start, stop, and monitor these activities.

Features:

    Network Scanning: Scans and lists available Wi-Fi networks within range.
    Deauthentication Attack: Performs deauthentication attacks on selected networks.
    Status Monitoring: Displays real-time status updates and logs.
    GUI Elements: Includes buttons for checking Wi-Fi monitor mode, starting/stopping scans, and deauth attacks.

Requirements:

    Linux operating system (preferred for compatibility with airmon-ng, airodump-ng, and aireplay-ng).
    Python 3.x.
    airmon-ng, airodump-ng, and aireplay-ng tools installed.
    tkinter library for the GUI.

Installation Process

    System Preparation:
        Ensure you are using a Linux-based system with appropriate privileges to install and run networking tools.
        Install Python 3.x if it’s not already installed on your system.

    Install Dependencies:
        Open a terminal and install the required tool:

    sudo apt update
    sudo apt install aircrack-ng python3-tk

Download the Tool:

    Obtain the DeAuth.py script from your source (e.g., repository, shared link).

Verify Script Permissions:

    Make sure the script has execute permissions:

    chmod +x DeAuth.py

Run the Tool:

    Launch the tool using Python:

    python3 DeAuth.py

Initial Setup:

    The tool will automatically start the wlan0mon interface. If it is not active or if there are errors, ensure that your Wi-Fi adapter supports monitor mode and troubleshoot as needed.

Usage:

    Use the GUI to:
        Check if wlan0mon is active.
        Start/stop network scanning.
        Start/stop deauthentication attacks.
        View real-time logs and network information.

Troubleshooting:

    If you encounter issues, ensure:
        You have the necessary permissions (e.g., running with sudo if required).
        Your network interface supports monitor mode.
        All dependencies and tools are properly installed.

Uninstallation:

    To remove the tool, simply delete the DeAuth.py script. The installed packages (aircrack-ng, python3-tk) can be removed using:


        sudo apt remove aircrack-ng python3-tk

By following these steps, you should be able to install and use the DeAuth.py tool effectively.
