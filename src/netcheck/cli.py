"""
NetCheck - CLI Module
Handles command-line interface and argument parsing
"""

import argparse
import sys
from .network_checker import NetworkChecker
from .diagnostics import NetworkDiagnostics
from .monitor import NetworkMonitor
from .formatter import OutputFormatter


class NetCheckCLI:
    """Command-line interface for NetCheck"""
    
    def __init__(self):
        self.checker = NetworkChecker()
        self.diagnostics = NetworkDiagnostics(self.checker)
        self.formatter = OutputFormatter()
    
    def run(self, args=None):
        """Main entry point for CLI"""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        # Execute appropriate command
        if parsed_args.command == 'status':
            self.cmd_status()
        elif parsed_args.command == 'ping':
            self.cmd_ping()
        elif parsed_args.command == 'full':
            self.cmd_full()
        elif parsed_args.command == 'monitor':
            self.cmd_monitor(parsed_args.interval)
        else:
            parser.print_help()
    
    def create_parser(self):
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog='netcheck',
            description='NetCheck - Terminal Network Diagnostic Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  netcheck status          Show basic network status
  netcheck ping            Run ping and DNS tests
  netcheck full            Run complete diagnostic report
  netcheck monitor         Start continuous monitoring (default: 10s interval)
  netcheck monitor -i 30   Start monitoring with 30s interval
            """
        )
        
        parser.add_argument(
            'command',
            choices=['status', 'ping', 'full', 'monitor'],
            help='Command to execute'
        )
        
        parser.add_argument(
            '-i', '--interval',
            type=int,
            default=10,
            help='Monitoring interval in seconds (default: 10)'
        )
        
        return parser
    
    def cmd_status(self):
        """Execute status command - basic network info"""
        print("\nChecking network status...")
        
        results = {
            'local_ip': self.checker.get_local_ip(),
            'external_ip': self.checker.get_external_ip(),
            'gateway': self.checker.get_gateway(),
            'interfaces': self.checker.get_network_interfaces(),
            'internet_connected': self.checker.is_connected()
        }
        
        # Quick diagnosis
        if results['internet_connected']:
            diagnosis = {'status': 'healthy', 'issues': [], 'advice': ['Internet is working normally']}
        else:
            diagnosis = {'status': 'no_connection', 'issues': ['No internet connection'], 
                        'advice': ['Check your network connection']}
        
        self.formatter.print_simple_status(results, diagnosis)
    
    def cmd_ping(self):
        """Execute ping command - connectivity tests"""
        print("\nRunning connectivity tests...")
        
        results = {
            'ping_google_dns': {},
            'ping_domain': {},
            'dns_working': False
        }
        
        # Ping Google DNS
        print("  - Pinging 8.8.8.8...")
        success, avg, loss = self.checker.ping_host("8.8.8.8", count=4)
        results['ping_google_dns'] = {'success': success, 'avg': avg, 'loss': loss}
        
        # Ping domain
        print("  - Pinging google.com...")
        success, avg, loss = self.checker.ping_host("google.com", count=4)
        results['ping_domain'] = {'success': success, 'avg': avg, 'loss': loss}
        
        # Check DNS
        print("  - Checking DNS resolution...")
        results['dns_working'] = self.checker.check_dns("google.com")
        
        # Print results
        self.formatter.print_connectivity_results(results)
        
        # Simple diagnosis
        if results['ping_google_dns']['success'] and results['dns_working']:
            print("\n[STATUS] Connectivity tests passed [OK]\n")
        else:
            print("\n[STATUS] Connectivity tests failed [FAIL]")
            if not results['dns_working']:
                print("  - DNS is not working properly")
                print("  - Try changing DNS server to 8.8.8.8\n")
    
    def cmd_full(self):
        """Execute full command - complete diagnostic report"""
        print("\nRunning full diagnostic...")
        print("  - Checking network interfaces...")
        print("  - Testing connectivity...")
        print("  - Running DNS checks...")
        
        results = self.diagnostics.run_full_diagnostic()
        diagnosis = self.diagnostics.get_diagnosis(results)
        
        self.formatter.print_full_report(results, diagnosis)
    
    def cmd_monitor(self, interval: int):
        """Execute monitor command - continuous monitoring"""
        monitor = NetworkMonitor(self.checker, interval=interval)
        monitor.monitor()


def main():
    """Main entry point"""
    try:
        cli = NetCheckCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
