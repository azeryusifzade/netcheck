"""
NetCheck - Network Diagnostic Module
Provides core network diagnostic functionality
"""

import socket
import subprocess
import platform
import requests
from typing import Dict, List, Tuple, Optional
import re


class NetworkChecker:
    """Main class for network diagnostics"""
    
    def __init__(self):
        self.system = platform.system()
        self.is_windows = self.system == "Windows"
        self.is_linux = self.system == "Linux"
        
    def get_local_ip(self) -> Optional[str]:
        """Get local IP address"""
        try:
            # Create a socket connection to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return None
    
    def get_external_ip(self) -> Optional[str]:
        """Get external/public IP address"""
        try:
            response = requests.get("https://api.ipify.org", timeout=5)
            if response.status_code == 200:
                return response.text.strip()
        except Exception:
            pass
        return None
    
    def get_network_interfaces(self) -> List[Dict[str, str]]:
        """Get network interfaces and their status"""
        interfaces = []
        
        try:
            if self.is_windows:
                result = subprocess.run(
                    ["ipconfig", "/all"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Parse Windows ipconfig output
                interfaces = self._parse_ipconfig(result.stdout)
            else:
                # Linux/Unix
                result = subprocess.run(
                    ["ip", "addr", "show"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                interfaces = self._parse_ip_addr(result.stdout)
        except Exception:
            pass
        
        return interfaces
    
    def _parse_ipconfig(self, output: str) -> List[Dict[str, str]]:
        """Parse Windows ipconfig output"""
        interfaces = []
        current_interface = None
        
        for line in output.split('\n'):
            line = line.strip()
            
            # Check for adapter name
            if 'adapter' in line.lower() and ':' in line:
                if current_interface:
                    interfaces.append(current_interface)
                current_interface = {
                    'name': line.split(':')[0].strip(),
                    'type': 'Unknown',
                    'ip': None
                }
                # Determine type
                if 'Ethernet' in line:
                    current_interface['type'] = 'Ethernet'
                elif 'Wi-Fi' in line or 'Wireless' in line:
                    current_interface['type'] = 'Wi-Fi'
                elif 'VPN' in line:
                    current_interface['type'] = 'VPN'
            
            # Check for IPv4 address
            if current_interface and 'IPv4 Address' in line:
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    current_interface['ip'] = ip_match.group(1)
        
        if current_interface:
            interfaces.append(current_interface)
        
        return [i for i in interfaces if i.get('ip')]
    
    def _parse_ip_addr(self, output: str) -> List[Dict[str, str]]:
        """Parse Linux ip addr output"""
        interfaces = []
        current_interface = None
        
        for line in output.split('\n'):
            line = line.strip()
            
            # Check for interface name
            if line and line[0].isdigit() and ':' in line:
                if current_interface:
                    interfaces.append(current_interface)
                
                parts = line.split(':')
                if len(parts) >= 2:
                    name = parts[1].strip()
                    current_interface = {
                        'name': name,
                        'type': self._determine_interface_type(name),
                        'ip': None
                    }
            
            # Check for IPv4 address
            if current_interface and 'inet ' in line:
                ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    ip = ip_match.group(1)
                    # Skip loopback
                    if not ip.startswith('127.'):
                        current_interface['ip'] = ip
        
        if current_interface:
            interfaces.append(current_interface)
        
        return [i for i in interfaces if i.get('ip')]
    
    def _determine_interface_type(self, name: str) -> str:
        """Determine interface type from name"""
        name_lower = name.lower()
        if 'eth' in name_lower or 'enp' in name_lower:
            return 'Ethernet'
        elif 'wl' in name_lower or 'wlan' in name_lower:
            return 'Wi-Fi'
        elif 'tun' in name_lower or 'vpn' in name_lower:
            return 'VPN'
        else:
            return 'Unknown'
    
    def get_gateway(self) -> Optional[str]:
        """Get default gateway"""
        try:
            if self.is_windows:
                result = subprocess.run(
                    ["ipconfig"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Look for Default Gateway
                for line in result.stdout.split('\n'):
                    if 'Default Gateway' in line:
                        gateway_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                        if gateway_match:
                            return gateway_match.group(1)
            else:
                result = subprocess.run(
                    ["ip", "route"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Look for default route
                for line in result.stdout.split('\n'):
                    if 'default' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2]
        except Exception:
            pass
        return None
    
    def ping_host(self, host: str, count: int = 4) -> Tuple[bool, Optional[float], Optional[float]]:
        """
        Ping a host and return success status, average time, and packet loss
        Returns: (success, avg_time_ms, packet_loss_percent)
        """
        try:
            param = "-n" if self.is_windows else "-c"
            
            result = subprocess.run(
                ["ping", param, str(count), host],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            output = result.stdout + result.stderr
            
            # Check if ping was successful
            success = result.returncode == 0
            
            # Extract average time
            avg_time = None
            if self.is_windows:
                avg_match = re.search(r'Average = (\d+)ms', output)
                if avg_match:
                    avg_time = float(avg_match.group(1))
            else:
                # Linux format: rtt min/avg/max/mdev = 12.345/23.456/34.567/1.234 ms
                avg_match = re.search(r'rtt \S+ = [\d.]+/([\d.]+)/', output)
                if avg_match:
                    avg_time = float(avg_match.group(1))
            
            # Extract packet loss
            packet_loss = None
            loss_match = re.search(r'(\d+)%\s+(?:packet\s+)?loss', output, re.IGNORECASE)
            if loss_match:
                packet_loss = float(loss_match.group(1))
            
            return success, avg_time, packet_loss
            
        except Exception:
            return False, None, None
    
    def check_dns(self, domain: str = "google.com") -> bool:
        """Check if DNS resolution works"""
        try:
            socket.gethostbyname(domain)
            return True
        except socket.gaierror:
            return False
    
    def is_connected(self) -> bool:
        """Quick check if device has internet connectivity"""
        # Try to ping a reliable DNS server
        success, _, _ = self.ping_host("8.8.8.8", count=1)
        return success
