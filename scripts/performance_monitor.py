#!/usr/bin/env python3
"""
Performance monitoring and optimization for BHIV HR Platform
"""

import psutil
import time
import logging
import json
from datetime import datetime, timezone
from typing import Dict, List
import requests

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """System performance monitoring and alerting"""
    
    def __init__(self):
        self.metrics_history = []
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'response_time_ms': 5000
        }
    
    def collect_system_metrics(self) -> Dict:
        """Collect system performance metrics"""
        try:
            metrics = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk': psutil.disk_usage('/')._asdict(),
                'network': psutil.net_io_counters()._asdict(),
                'processes': len(psutil.pids())
            }
            
            # Calculate percentages
            metrics['memory_percent'] = metrics['memory']['percent']
            metrics['disk_percent'] = (metrics['disk']['used'] / metrics['disk']['total']) * 100
            
            return metrics
        except Exception as e:
            logger.error(f"Error collecting metrics: {str(e)}")
            return {}
    
    def test_api_performance(self, base_url: str = "http://localhost:8000") -> Dict:
        """Test API endpoint performance"""
        endpoints = [
            '/health',
            '/candidates/stats',
            '/v1/jobs'
        ]
        
        performance_data = {}
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                end_time = time.time()
                
                response_time_ms = (end_time - start_time) * 1000
                
                performance_data[endpoint] = {
                    'response_time_ms': response_time_ms,
                    'status_code': response.status_code,
                    'success': response.status_code == 200
                }
                
            except Exception as e:
                performance_data[endpoint] = {
                    'response_time_ms': None,
                    'status_code': None,
                    'success': False,
                    'error': str(e)
                }
        
        return performance_data
    
    def check_alerts(self, metrics: Dict) -> List[str]:
        """Check for performance alerts"""
        alerts = []
        
        if metrics.get('cpu_percent', 0) > self.alert_thresholds['cpu_percent']:
            alerts.append(f"High CPU usage: {metrics['cpu_percent']:.1f}%")
        
        if metrics.get('memory_percent', 0) > self.alert_thresholds['memory_percent']:
            alerts.append(f"High memory usage: {metrics['memory_percent']:.1f}%")
        
        if metrics.get('disk_percent', 0) > self.alert_thresholds['disk_percent']:
            alerts.append(f"High disk usage: {metrics['disk_percent']:.1f}%")
        
        return alerts
    
    def generate_report(self) -> Dict:
        """Generate performance report"""
        system_metrics = self.collect_system_metrics()
        api_performance = self.test_api_performance()
        alerts = self.check_alerts(system_metrics)
        
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'system_metrics': system_metrics,
            'api_performance': api_performance,
            'alerts': alerts,
            'health_status': 'healthy' if not alerts else 'warning'
        }
        
        # Store in history
        self.metrics_history.append(report)
        
        # Keep only last 100 entries
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        return report
    
    def optimize_recommendations(self, metrics: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if metrics.get('cpu_percent', 0) > 70:
            recommendations.append("Consider scaling horizontally or optimizing CPU-intensive operations")
        
        if metrics.get('memory_percent', 0) > 75:
            recommendations.append("Monitor memory leaks and consider increasing available RAM")
        
        if metrics.get('disk_percent', 0) > 80:
            recommendations.append("Clean up old logs and temporary files, consider disk expansion")
        
        # Check API performance
        api_perf = self.test_api_performance()
        slow_endpoints = [
            endpoint for endpoint, data in api_perf.items()
            if data.get('response_time_ms', 0) > 2000
        ]
        
        if slow_endpoints:
            recommendations.append(f"Optimize slow endpoints: {', '.join(slow_endpoints)}")
        
        return recommendations

def main():
    """Main monitoring function"""
    monitor = PerformanceMonitor()
    
    print("BHIV HR Platform - Performance Monitor")
    print("=" * 50)
    
    # Generate report
    report = monitor.generate_report()
    
    # Display results
    print(f"Timestamp: {report['timestamp']}")
    print(f"Health Status: {report['health_status'].upper()}")
    print()
    
    # System metrics
    print("System Metrics:")
    metrics = report['system_metrics']
    print(f"  CPU Usage: {metrics.get('cpu_percent', 0):.1f}%")
    print(f"  Memory Usage: {metrics.get('memory_percent', 0):.1f}%")
    print(f"  Disk Usage: {metrics.get('disk_percent', 0):.1f}%")
    print(f"  Active Processes: {metrics.get('processes', 0)}")
    print()
    
    # API performance
    print("API Performance:")
    for endpoint, data in report['api_performance'].items():
        status = "✓" if data['success'] else "✗"
        response_time = data.get('response_time_ms', 0)
        print(f"  {status} {endpoint}: {response_time:.0f}ms")
    print()
    
    # Alerts
    if report['alerts']:
        print("⚠️  Alerts:")
        for alert in report['alerts']:
            print(f"  - {alert}")
        print()
    
    # Recommendations
    recommendations = monitor.optimize_recommendations(metrics)
    if recommendations:
        print("💡 Optimization Recommendations:")
        for rec in recommendations:
            print(f"  - {rec}")
    else:
        print("✅ System performance is optimal")

if __name__ == "__main__":
    main()