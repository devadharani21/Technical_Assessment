#!/usr/bin/env python3
"""
Code Analytics Framework - Main Entry Point

A comprehensive tool for analyzing test scripts for quality issues,
code duplication, and flaky test patterns.
"""

import argparse
import sys
from pathlib import Path
import json

from src.analyzer import CodeAnalyzer
from src.reporters.excel_reporter import ExcelReporter


def main():
    """Main entry point for the Code Analytics Framework."""
    parser = argparse.ArgumentParser(
        description='Code Analytics Framework for Test Scripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze test files in a directory
  python main.py --directory ./tests

  # Specify output directory
  python main.py --directory ./tests --output ./reports

  # Use custom configuration
  python main.py --directory ./tests --config ./my_config.yaml
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        required=True,
        help='Directory containing test scripts to analyze'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='./reports',
        help='Output directory for reports (default: ./reports)'
    )
    
    # Removed format option - only Excel is generated
    
    parser.add_argument(
        '-c', '--config',
        type=str,
        default=None,
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Also save results as JSON'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    test_dir = Path(args.directory)
    if not test_dir.exists():
        print(f"Error: Directory '{test_dir}' does not exist")
        sys.exit(1)
    
    if not test_dir.is_dir():
        print(f"Error: '{test_dir}' is not a directory")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("CODE ANALYTICS FRAMEWORK FOR TEST SCRIPTS")
    print("=" * 70)
    print(f"\nAnalyzing: {test_dir}")
    print(f"Output: {output_dir}")
    print(f"Report Format: Excel")
    print()
    
    try:
        # Initialize analyzer
        analyzer = CodeAnalyzer(config_path=args.config)
        
        # Perform analysis
        print("\n" + "=" * 70)
        print("STARTING ANALYSIS")
        print("=" * 70)
        results = analyzer.analyze_directory(test_dir)
        
        if 'error' in results:
            print(f"\nError: {results['error']}")
            sys.exit(1)
        
        # Save JSON if requested
        if args.json:
            json_path = output_dir / 'analysis_results.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"\nJSON results saved: {json_path}")
        
        # Generate Excel report
        print("\n" + "=" * 70)
        print("GENERATING EXCEL REPORT")
        print("=" * 70)
        print()
        
        excel_reporter = ExcelReporter()
        excel_path = output_dir / 'analysis_report.xlsx'
        excel_reporter.generate_report(results, excel_path)
        
        # Print summary
        print("\n" + "=" * 70)
        print("ANALYSIS SUMMARY")
        print("=" * 70)
        
        summary = results.get('summary', {})
        
        print(f"\nTotal Issues Found: {summary.get('total_issues', 0)}")
        print("\nBy Severity:")
        for severity in ['critical', 'high', 'medium', 'low']:
            count = summary.get('by_severity', {}).get(severity, 0)
            print(f"  {severity.capitalize():10s}: {count}")
        
        flaky_stats = summary.get('flaky_test_stats', {})
        print(f"\nFlaky Test Patterns:")
        print(f"  Files Affected: {flaky_stats.get('files_with_flaky_patterns', 0)}")
        print(f"  Total Issues: {flaky_stats.get('total_flaky_issues', 0)}")
        
        dup_stats = summary.get('duplication_stats', {})
        if dup_stats:
            print(f"\nCode Duplication:")
            print(f"  Total Duplicates: {dup_stats.get('total_duplicates', 0)}")
            print(f"  Duplication %: {dup_stats.get('duplication_percentage', 0):.2f}%")
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"\nReports saved to: {output_dir}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

