"""
NetCheck - Diagnostics Module
Provides auto-diagnosis and troubleshooting advice
"""

from typing import Dict, List, Optional
from .network_checker import NetworkChecker


class NetworkDiagnostics:
    """Provides network diagnostics and advice"""
    
    def __init__(self, checker: NetworkChecker):
        self.checker = checker
        self.results = {}
    
    def run_full_diagnostic(self) -> Dict:
        """Run complete diagnostic check"""
        results = {
            'local_ip': None,
            'external_ip': None,
            'gateway': None,
            'interfaces': [],
            'ping_google_dns': {'success': False, 'avg': None, 'loss': None},
            'ping_domain': {'success': False, 'avg': None, 'loss': None},
            'dns_working': False,
            'internet_connected': False
        }
        
        # Get IP addresses
        results['local_ip'] = self.checker.get_local_ip()
        results['external_ip'] = self.checker.get_external_ip()
        results['gateway'] = self.checker.get_gateway()
        
        # Get network interfaces
        results['interfaces'] = self.checker.get_network_interfaces()
        
        # Ping Google DNS
        success, avg, loss = self.checker.ping_host("8.8.8.8", count=4)
        results['ping_google_dns'] = {
            'success': success,
            'avg': avg,
            'loss': loss
        }
        
        # Ping domain
        success, avg, loss = self.checker.ping_host("google.com", count=4)
        results['ping_domain'] = {
            'success': success,
            'avg': avg,
            'loss': loss
        }
        
        # Check DNS
        results['dns_working'] = self.checker.check_dns("google.com")
        
        # Overall connectivity
        results['internet_connected'] = results['ping_google_dns']['success']
        
        self.results = results
        return results
    
    def get_diagnosis(self, results: Optional[Dict] = None) -> Dict:
        """
        Analyze results and provide diagnosis
        Returns: {'status': str, 'issues': List[str], 'advice': List[str]}
        """
        if results is None:
            results = self.results
        
        diagnosis = {
            'status': 'unknown',
            'issues': [],
            'advice': []
        }
        
        # Check for complete failure
        if not results['internet_connected']:
            diagnosis['status'] = 'no_connection'
            diagnosis['issues'].append('No internet connectivity detected')
            
            # No local IP
            if not results['local_ip']:
                diagnosis['issues'].append('No network connection (no local IP)')
                diagnosis['advice'].append('Check your network cable or Wi-Fi connection')
                diagnosis['advice'].append('Restart your network adapter')
            else:
                # Has local IP but no internet
                if not results['gateway']:
                    diagnosis['issues'].append('No default gateway detected')
                    diagnosis['advice'].append('Check router connection')
                    diagnosis['advice'].append('Restart your router')
                else:
                    diagnosis['issues'].append('Connected to router but no internet access')
                    diagnosis['advice'].append('Check if your router has internet access')
                    diagnosis['advice'].append('Contact your ISP if router is online but no internet')
            
            return diagnosis
        
        # Has basic connectivity, check DNS
        if not results['dns_working']:
            diagnosis['status'] = 'dns_issue'
            diagnosis['issues'].append('DNS not responding properly')
            diagnosis['advice'].append('Try changing DNS server to 8.8.8.8 or 1.1.1.1')
            diagnosis['advice'].append('Flush DNS cache')
            if self.checker.is_windows:
                diagnosis['advice'].append('Run: ipconfig /flushdns')
            else:
                diagnosis['advice'].append('Restart network service or reboot')
            return diagnosis
        
        # Check for high packet loss
        if results['ping_google_dns']['loss'] and results['ping_google_dns']['loss'] > 20:
            diagnosis['status'] = 'unstable_connection'
            diagnosis['issues'].append(f"High packet loss ({results['ping_google_dns']['loss']}%)")
            diagnosis['advice'].append('Network connection is unstable')
            diagnosis['advice'].append('Check Wi-Fi signal strength if using wireless')
            diagnosis['advice'].append('Check network cables if using Ethernet')
            diagnosis['advice'].append('Restart router if problem persists')
            return diagnosis
        
        # Check for slow connection
        if results['ping_google_dns']['avg'] and results['ping_google_dns']['avg'] > 100:
            diagnosis['status'] = 'slow_connection'
            diagnosis['issues'].append(f"High latency ({results['ping_google_dns']['avg']:.1f}ms)")
            diagnosis['advice'].append('Network latency is high')
            diagnosis['advice'].append('Close bandwidth-intensive applications')
            diagnosis['advice'].append('Check if others are using network heavily')
            return diagnosis
        
        # Everything looks good
        diagnosis['status'] = 'healthy'
        diagnosis['issues'] = []
        diagnosis['advice'] = ['Internet is working normally']
        
        return diagnosis
    
    def get_quick_status(self) -> str:
        """Get quick one-line status"""
        if not self.results:
            return "Unknown - Run diagnostic first"
        
        diagnosis = self.get_diagnosis()
        
        if diagnosis['status'] == 'healthy':
            return "Internet is working normally [OK]"
        elif diagnosis['status'] == 'no_connection':
            return "No internet connection [FAIL]"
        elif diagnosis['status'] == 'dns_issue':
            return "Connected but DNS not working [WARNING]"
        elif diagnosis['status'] == 'unstable_connection':
            return "Unstable connection (high packet loss) [WARNING]"
        elif diagnosis['status'] == 'slow_connection':
            return "Slow connection (high latency) [WARNING]"
        else:
            return "Unknown status"
