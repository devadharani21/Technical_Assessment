"""Main Analyzer - Orchestrates all analysis modules."""

import yaml
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import fnmatch

from .analyzers.coding_standards import CodingStandardsAnalyzer
from .analyzers.duplication import DuplicationDetector
from .analyzers.flaky_patterns import FlakyPatternDetector


class CodeAnalyzer:
    """Main analyzer that orchestrates all analysis modules."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the analyzer with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'analysis_config.yaml'
        
        self.config = self._load_config(config_path)
        self.coding_standards = CodingStandardsAnalyzer(self.config)
        self.duplication = DuplicationDetector(self.config)
        self.flaky_patterns = FlakyPatternDetector(self.config)
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            return {}
    
    def analyze_directory(self, directory: Path) -> Dict[str, Any]:
        """
        Analyze all test files in a directory.
        
        Args:
            directory: Directory containing test files
            
        Returns:
            Complete analysis results
        """
        print(f"Starting analysis of: {directory}")
        start_time = datetime.now()
        
        # Find all test files
        test_files = self._find_test_files(directory)
        print(f"Found {len(test_files)} test files to analyze")
        
        if not test_files:
            return {
                'error': 'No test files found',
                'directory': str(directory)
            }
        
        # Perform analyses
        results = {
            'metadata': {
                'directory': str(directory),
                'total_files': len(test_files),
                'analysis_date': datetime.now().isoformat(),
                'start_time': start_time.isoformat()
            },
            'files': [],
            'coding_standards': [],
            'duplication': {},
            'flaky_patterns': [],
            'summary': {}
        }
        
        # Analyze each file
        print("\n=== Analyzing Coding Standards ===")
        for file_path in test_files:
            print(f"  Analyzing: {file_path.name}")
            standards_result = self.coding_standards.analyze_file(file_path)
            results['coding_standards'].append(standards_result)
        
        print("\n=== Detecting Code Duplication ===")
        duplication_result = self.duplication.analyze_files(test_files)
        results['duplication'] = duplication_result
        
        print("\n=== Detecting Flaky Patterns ===")
        for file_path in test_files:
            print(f"  Analyzing: {file_path.name}")
            flaky_result = self.flaky_patterns.analyze_file(file_path)
            results['flaky_patterns'].append(flaky_result)
        
        # Generate summary
        results['summary'] = self._generate_summary(results)
        
        end_time = datetime.now()
        results['metadata']['end_time'] = end_time.isoformat()
        results['metadata']['duration_seconds'] = (end_time - start_time).total_seconds()
        
        print(f"\n=== Analysis Complete ===")
        print(f"Duration: {results['metadata']['duration_seconds']:.2f} seconds")
        
        return results
    
    def _find_test_files(self, directory: Path) -> List[Path]:
        """Find all test files matching configured patterns."""
        test_files = []
        include_patterns = self.config.get('file_patterns', {}).get('include', ['test_*.py'])
        exclude_patterns = self.config.get('file_patterns', {}).get('exclude', [])
        
        for pattern in include_patterns:
            # Handle glob patterns
            if '**' in pattern:
                for file_path in directory.rglob(pattern.replace('**/', '')):
                    if file_path.is_file() and not self._should_exclude(file_path, exclude_patterns):
                        test_files.append(file_path)
            else:
                for file_path in directory.glob(pattern):
                    if file_path.is_file() and not self._should_exclude(file_path, exclude_patterns):
                        test_files.append(file_path)
        
        return sorted(set(test_files))
    
    def _should_exclude(self, file_path: Path, exclude_patterns: List[str]) -> bool:
        """Check if file should be excluded based on patterns."""
        file_str = str(file_path)
        
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(file_str, f"*{pattern}") or fnmatch.fnmatch(file_path.name, pattern):
                return True
        
        return False
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics from results."""
        summary = {
            'total_issues': 0,
            'by_severity': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
            'by_category': {},
            'top_issues': [],
            'most_problematic_files': [],
            'duplication_stats': {},
            'flaky_test_stats': {}
        }
        
        # Count coding standards violations
        for file_result in results['coding_standards']:
            summary['total_issues'] += file_result['total_violations']
            for severity, count in file_result['severity_breakdown'].items():
                summary['by_severity'][severity] += count
        
        # Count flaky pattern issues
        flaky_files_count = 0
        total_flaky_issues = 0
        high_risk_files = []
        
        for file_result in results['flaky_patterns']:
            total_flaky_issues += file_result['total_issues']
            if file_result['total_issues'] > 0:
                flaky_files_count += 1
            
            if file_result['risk_score'] >= 20:
                high_risk_files.append({
                    'file': file_result['file'],
                    'risk_score': file_result['risk_score'],
                    'issues': file_result['total_issues']
                })
            
            for issue in file_result['issues']:
                severity = issue['severity']
                summary['by_severity'][severity] += 1
                category = issue.get('category', 'unknown')
                summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
        
        summary['total_issues'] += total_flaky_issues
        
        # Duplication stats
        if results['duplication']:
            summary['duplication_stats'] = {
                'total_duplicates': results['duplication'].get('total_duplicates', 0),
                'duplication_percentage': results['duplication'].get('duplication_percentage', 0),
                'files_analyzed': results['duplication'].get('total_files_analyzed', 0)
            }
        
        # Flaky test stats
        summary['flaky_test_stats'] = {
            'files_with_flaky_patterns': flaky_files_count,
            'total_flaky_issues': total_flaky_issues,
            'high_risk_files': sorted(high_risk_files, key=lambda x: x['risk_score'], reverse=True)[:10]
        }
        
        # Find most problematic files
        file_issue_counts = {}
        
        for file_result in results['coding_standards']:
            file_path = file_result['file']
            file_issue_counts[file_path] = file_issue_counts.get(file_path, 0) + file_result['total_violations']
        
        for file_result in results['flaky_patterns']:
            file_path = file_result['file']
            file_issue_counts[file_path] = file_issue_counts.get(file_path, 0) + file_result['total_issues']
        
        summary['most_problematic_files'] = sorted(
            [{'file': f, 'issues': c} for f, c in file_issue_counts.items()],
            key=lambda x: x['issues'],
            reverse=True
        )[:10]
        
        return summary

