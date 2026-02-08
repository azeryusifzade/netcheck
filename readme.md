# NetCheck - Terminal Network Diagnostic Tool

A cross-platform command-line network diagnostic tool for Linux and Windows. NetCheck provides clear, human-readable reports of network status, connectivity, and basic troubleshooting advice.

## Features

- **Network Status Detection**: Check if your device is connected to the internet
- **Interface Information**: Show active network interfaces (Ethernet, Wi-Fi, VPN)
- **IP Address Display**: View local and external/public IP addresses
- **Gateway Detection**: Display default gateway information
- **Connectivity Testing**: Ping external IPs and domains to verify connectivity
- **DNS Verification**: Test DNS resolution functionality
- **Auto-Diagnosis**: Get intelligent troubleshooting advice based on test results
- **Real-Time Monitoring**: Continuously monitor network status with automatic alerts
- **Cross-Platform**: Works on Linux and Windows

## Requirements

- Python 3.7 or higher
- Internet connection (for external IP lookup)

## Installation


1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt #pip3 for Linux or MacOs
```

3. Run NetCheck:
```bash
python netcheck.py status #python3 for Linux or MacOs
```


### Linux Quick Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Make executable (optional)
chmod +x netcheck.py

# Run
python3 netcheck.py status
```

### Windows Quick Setup

```cmd
# Install dependencies
pip install -r requirements.txt

# Run
python netcheck.py status
```

## Usage

NetCheck provides four main commands:

### 1. Status - Basic Network Information

Shows basic network status including IP addresses and connectivity.

```bash
python netcheck.py status
```

**Example Output:**
```
============================================================
                    NETCHECK STATUS
============================================================

[Local IP] 192.168.1.12
[External IP] 84.22.55.66

[OVERALL] Internet is working normally [OK]

============================================================
```

### 2. Ping - Connectivity Tests

Runs ping tests to verify connectivity and DNS functionality.

```bash
python netcheck.py ping
```

**Example Output:**
```
============================================================
                 CONNECTIVITY TEST
============================================================
[PING] 8.8.8.8: avg=12ms [OK]
[PING] google.com: avg=14ms [OK]
[DNS] google.com: working [OK]

[STATUS] Connectivity tests passed [OK]
```

### 3. Full - Complete Diagnostic Report

Runs a comprehensive diagnostic and provides detailed troubleshooting advice.

```bash
python netcheck.py full
```

**Example Output:**
```
============================================================
                    NETCHECK REPORT
============================================================

============================================================
NETWORK STATUS
============================================================
[Local IP] 192.168.1.12
[External IP] 84.22.55.66
[Gateway] 192.168.1.1

[Network Interfaces]
  - Ethernet 2 (Ethernet): 192.168.1.12

============================================================
CONNECTIVITY TEST
============================================================
[PING] 8.8.8.8: avg=12ms [OK]
[PING] google.com: avg=14ms [OK]
[DNS] google.com: working [OK]

============================================================
DIAGNOSIS
============================================================
[STATUS] Internet is working normally [OK]

============================================================
```

### 4. Monitor - Real-Time Network Monitoring

Continuously monitors your network connection and alerts on status changes.

```bash
# Monitor with default 10-second interval
python netcheck.py monitor

# Monitor with custom interval (30 seconds)
python netcheck.py monitor -i 30
```

**Example Output:**
```
Starting network monitor (checking every 10 seconds)
Press Ctrl+C to stop

[2025-02-08 14:23:10] [OK] Initial check: Internet is UP
[2025-02-08 14:23:20] [OK] Connection status: UP
[2025-02-08 14:23:30] [OK] Connection status: UP

============================================================
[2025-02-08 14:23:40] [ALERT] Internet connection LOST [FAIL]

Reason:
  - No internet connectivity detected
  - Connected to router but no internet access

Advice:
  - Check if your router has internet access
  - Contact your ISP if router is online but no internet
============================================================
```

## Command Reference

| Command | Description | Options |
|---------|-------------|---------|
| `status` | Show basic network status | None |
| `ping` | Run connectivity and DNS tests | None |
| `full` | Complete diagnostic report | None |
| `monitor` | Continuous monitoring mode | `-i, --interval` (seconds) |



### Permission Issues (Linux)

Some network commands may require elevated permissions:

```bash
sudo python3 netcheck.py full
```

### Firewall Blocking

If ping tests fail but internet works, your firewall may be blocking ICMP:
- Windows: Check Windows Firewall settings
- Linux: Check iptables/ufw configuration



## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Support

For issues, questions, or suggestions, please open an issue in the project repository.