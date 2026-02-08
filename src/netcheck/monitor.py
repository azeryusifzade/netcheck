"""
NetCheck - Network Monitor Module
Provides real-time continuous network monitoring
"""

import time
from datetime import datetime
from typing import Callable, Optional
from .network_checker import NetworkChecker
from .diagnostics import NetworkDiagnostics


class NetworkMonitor:
    """Continuous network monitoring"""
    
    def __init__(self, checker: NetworkChecker, interval: int = 10):
        self.checker = checker
        self.diagnostics = NetworkDiagnostics(checker)
        self.interval = interval
        self.previous_status = None
        self.running = False
    
    def monitor(self, callback: Optional[Callable] = None):
        """
        Start continuous monitoring
        callback: Optional function to call on status change
        """
        self.running = True
        print(f"Starting network monitor (checking every {self.interval} seconds)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Quick connectivity check
                connected = self.checker.is_connected()
                
                # If status changed, run full diagnostic
                if connected != self.previous_status:
                    self._handle_status_change(connected, timestamp)
                    
                    if callback:
                        callback(connected, timestamp)
                else:
                    # Status unchanged, just show heartbeat
                    status_symbol = "[OK]" if connected else "[FAIL]"
                    print(f"[{timestamp}] {status_symbol} Connection status: {'UP' if connected else 'DOWN'}")
                
                self.previous_status = connected
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            self.running = False
    
    def _handle_status_change(self, connected: bool, timestamp: str):
        """Handle network status change"""
        if connected and self.previous_status is False:
            # Connection restored
            print("\n" + "="*60)
            print(f"[{timestamp}] [ALERT] Internet connection RESTORED [OK]")
            print("="*60 + "\n")
            
        elif not connected and self.previous_status is True:
            # Connection lost
            print("\n" + "="*60)
            print(f"[{timestamp}] [ALERT] Internet connection LOST [FAIL]")
            
            # Run diagnostic to determine cause
            results = self.diagnostics.run_full_diagnostic()
            diagnosis = self.diagnostics.get_diagnosis(results)
            
            if diagnosis['issues']:
                print("\nReason:")
                for issue in diagnosis['issues']:
                    print(f"  - {issue}")
            
            if diagnosis['advice']:
                print("\nAdvice:")
                for advice in diagnosis['advice']:
                    print(f"  - {advice}")
            
            print("="*60 + "\n")
        
        elif self.previous_status is None:
            # Initial check
            if connected:
                print(f"[{timestamp}] [OK] Initial check: Internet is UP")
            else:
                print(f"[{timestamp}] [FAIL] Initial check: Internet is DOWN")
                
                # Run diagnostic
                results = self.diagnostics.run_full_diagnostic()
                diagnosis = self.diagnostics.get_diagnosis(results)
                
                if diagnosis['issues']:
                    print("\nIssues detected:")
                    for issue in diagnosis['issues']:
                        print(f"  - {issue}")
                
                if diagnosis['advice']:
                    print("\nRecommended actions:")
                    for advice in diagnosis['advice']:
                        print(f"  - {advice}")
                print()
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
