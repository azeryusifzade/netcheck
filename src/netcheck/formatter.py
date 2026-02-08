"""
NetCheck - Output Formatter Module
Formats and displays network diagnostic results
"""

from typing import Dict, List


class OutputFormatter:
    """Formats output for terminal display"""
    
    @staticmethod
    def format_header(text: str) -> str:
        """Format section header"""
        return f"\n{'='*60}\n{text}\n{'='*60}"
    
    @staticmethod
    def format_status(label: str, value: str, success: bool = True) -> str:
        """Format a status line with check/cross symbol"""
        symbol = "[OK]" if success else "[FAIL]"
        return f"[{label}] {value} {symbol}"
    
    @staticmethod
    def format_info(label: str, value: str) -> str:
        """Format an information line"""
        return f"[{label}] {value}"
    
    @staticmethod
    def print_network_status(results: Dict):
        """Print network status overview"""
        print(OutputFormatter.format_header("NETWORK STATUS"))
        
        # Local IP
        if results.get('local_ip'):
            print(OutputFormatter.format_info("Local IP", results['local_ip']))
        else:
            print(OutputFormatter.format_status("Local IP", "Not detected", False))
        
        # External IP
        if results.get('external_ip'):
            print(OutputFormatter.format_info("External IP", results['external_ip']))
        else:
            print(OutputFormatter.format_status("External IP", "Not detected", False))
        
        # Gateway
        if results.get('gateway'):
            print(OutputFormatter.format_info("Gateway", results['gateway']))
        
        # Network Interfaces
        if results.get('interfaces'):
            print(f"\n[Network Interfaces]")
            for interface in results['interfaces']:
                print(f"  - {interface['name']} ({interface['type']}): {interface['ip']}")
    
    @staticmethod
    def print_connectivity_results(results: Dict):
        """Print connectivity test results"""
        print(OutputFormatter.format_header("CONNECTIVITY TEST"))
        
        # Ping Google DNS
        ping_dns = results.get('ping_google_dns', {})
        if ping_dns.get('success'):
            avg = ping_dns.get('avg')
            loss = ping_dns.get('loss', 0)
            avg_str = f"avg={avg:.0f}ms" if avg else "success"
            loss_str = f", loss={loss:.0f}%" if loss and loss > 0 else ""
            print(OutputFormatter.format_status("PING", f"8.8.8.8: {avg_str}{loss_str}", True))
        else:
            print(OutputFormatter.format_status("PING", "8.8.8.8: failed", False))
        
        # Ping Domain
        ping_domain = results.get('ping_domain', {})
        if ping_domain.get('success'):
            avg = ping_domain.get('avg')
            avg_str = f"avg={avg:.0f}ms" if avg else "success"
            print(OutputFormatter.format_status("PING", f"google.com: {avg_str}", True))
        else:
            print(OutputFormatter.format_status("PING", "google.com: failed", False))
        
        # DNS Check
        dns_working = results.get('dns_working', False)
        if dns_working:
            print(OutputFormatter.format_status("DNS", "google.com: working", True))
        else:
            print(OutputFormatter.format_status("DNS", "google.com: not responding", False))
    
    @staticmethod
    def print_diagnosis(diagnosis: Dict):
        """Print diagnostic results and advice"""
        print(OutputFormatter.format_header("DIAGNOSIS"))
        
        status = diagnosis.get('status', 'unknown')
        
        if status == 'healthy':
            print(OutputFormatter.format_status("STATUS", "Internet is working normally", True))
        else:
            print(OutputFormatter.format_status("STATUS", "Issues detected", False))
        
        # Print issues
        issues = diagnosis.get('issues', [])
        if issues:
            print("\n[Issues Detected]")
            for issue in issues:
                print(f"  - {issue}")
        
        # Print advice
        advice = diagnosis.get('advice', [])
        if advice:
            print("\n[Recommended Actions]")
            for item in advice:
                print(f"  - {item}")
    
    @staticmethod
    def print_full_report(results: Dict, diagnosis: Dict):
        """Print complete diagnostic report"""
        print("\n" + "="*60)
        print(" "*20 + "NETCHECK REPORT")
        print("="*60)
        
        OutputFormatter.print_network_status(results)
        OutputFormatter.print_connectivity_results(results)
        OutputFormatter.print_diagnosis(diagnosis)
        
        print("\n" + "="*60 + "\n")
    
    @staticmethod
    def print_simple_status(results: Dict, diagnosis: Dict):
        """Print simplified status view"""
        print("\n" + "="*60)
        print(" "*20 + "NETCHECK STATUS")
        print("="*60 + "\n")
        
        # Basic info
        if results.get('local_ip'):
            print(OutputFormatter.format_info("Local IP", results['local_ip']))
        if results.get('external_ip'):
            print(OutputFormatter.format_info("External IP", results['external_ip']))
        
        # Overall status
        print()
        status = diagnosis.get('status', 'unknown')
        if status == 'healthy':
            print(OutputFormatter.format_status("OVERALL", "Internet is working normally", True))
        else:
            print(OutputFormatter.format_status("OVERALL", "Connection issues detected", False))
            
            advice = diagnosis.get('advice', [])
            if advice:
                print("\n[Quick Advice]")
                print(f"  - {advice[0]}")
        
        print("\n" + "="*60 + "\n")
