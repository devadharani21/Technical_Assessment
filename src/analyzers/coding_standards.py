"""Coding Standards Analyzer - Checks for style and convention violations."""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any
import subprocess
import json


class CodingStandardsAnalyzer:
    """Analyzes code for coding standard violations."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the analyzer with configuration.
        
        Args:
            config: Configuration dictionary containing coding standards
        """
        self.config = config.get('coding_standards', {})
        self.max_line_length = self.config.get('max_line_length', 120)
        self.max_function_length = self.config.get('max_function_length', 50)
        self.max_complexity = self.config.get('max_complexity', 10)
        self.max_nested_blocks = self.config.get('max_nested_blocks', 4)
        self.naming_conventions = self.config.get('naming_conventions', {})
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a single file for coding standard violations.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary containing violations and metrics
        """
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check line length
            violations.extend(self._check_line_length(lines, file_path))
            
            # Check naming conventions
            violations.extend(self._check_naming_conventions(content, file_path))
            
            # Check function length and complexity
            violations.extend(self._check_function_metrics(content, file_path))
            
            # Check nested blocks
            violations.extend(self._check_nested_blocks(content, file_path))
            
            # Run flake8 if available
            violations.extend(self._run_flake8(file_path))
            
            # Run pylint if available
            violations.extend(self._run_pylint(file_path))
            
        except Exception as e:
            violations.append({
                'file': str(file_path),
                'line': 0,
                'type': 'error',
                'severity': 'critical',
                'message': f"Error analyzing file: {str(e)}"
            })
        
        return {
            'file': str(file_path),
            'total_violations': len(violations),
            'violations': violations,
            'severity_breakdown': self._count_by_severity(violations)
        }
    
    def _check_line_length(self, lines: List[str], file_path: Path) -> List[Dict[str, Any]]:
        """Check for lines exceeding maximum length."""
        violations = []
        for i, line in enumerate(lines, 1):
            if len(line) > self.max_line_length:
                violations.append({
                    'file': str(file_path),
                    'line': i,
                    'type': 'line_length',
                    'severity': 'low',
                    'message': f"Line exceeds {self.max_line_length} characters (found {len(line)})",
                    'code': line[:100] + '...' if len(line) > 100 else line
                })
        return violations
    
    def _check_naming_conventions(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Check naming conventions for tests, classes, and functions."""
        violations = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Check class names
                if isinstance(node, ast.ClassDef):
                    class_pattern = self.naming_conventions.get('class_pattern', '')
                    if class_pattern and not re.match(class_pattern, node.name):
                        violations.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'type': 'naming_convention',
                            'severity': 'medium',
                            'message': f"Class name '{node.name}' doesn't match pattern {class_pattern}",
                            'code': node.name
                        })
                
                # Check function/method names
                if isinstance(node, ast.FunctionDef):
                    # Test functions should start with test_
                    test_prefix = self.naming_conventions.get('test_prefix', 'test_')
                    if not node.name.startswith('_') and not node.name.startswith(test_prefix):
                        violations.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'type': 'naming_convention',
                            'severity': 'medium',
                            'message': f"Test function '{node.name}' should start with '{test_prefix}'",
                            'code': node.name
                        })
                    
                    # Check function naming pattern
                    function_pattern = self.naming_conventions.get('function_pattern', '')
                    if function_pattern and not re.match(function_pattern, node.name):
                        violations.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'type': 'naming_convention',
                            'severity': 'low',
                            'message': f"Function name '{node.name}' doesn't follow snake_case convention",
                            'code': node.name
                        })
        
        except SyntaxError as e:
            violations.append({
                'file': str(file_path),
                'line': e.lineno or 0,
                'type': 'syntax_error',
                'severity': 'critical',
                'message': f"Syntax error: {str(e)}",
                'code': ''
            })
        
        return violations
    
    def _check_function_metrics(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Check function length and complexity."""
        violations = []
        
        try:
            tree = ast.parse(content)
            lines = content.split('\n')
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check function length
                    func_length = node.end_lineno - node.lineno + 1
                    if func_length > self.max_function_length:
                        violations.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'type': 'function_length',
                            'severity': 'medium',
                            'message': f"Function '{node.name}' is too long ({func_length} lines, max {self.max_function_length})",
                            'code': node.name
                        })
                    
                    # Check cyclomatic complexity (simplified)
                    complexity = self._calculate_complexity(node)
                    if complexity > self.max_complexity:
                        violations.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'type': 'complexity',
                            'severity': 'high',
                            'message': f"Function '{node.name}' has high complexity ({complexity}, max {self.max_complexity})",
                            'code': node.name
                        })
        
        except SyntaxError:
            pass  # Already caught in naming check
        
        return violations
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _check_nested_blocks(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Check for deeply nested code blocks."""
        violations = []
        
        try:
            tree = ast.parse(content)
            
            def check_nesting(node, depth=0):
                if depth > self.max_nested_blocks:
                    violations.append({
                        'file': str(file_path),
                        'line': node.lineno,
                        'type': 'nesting',
                        'severity': 'high',
                        'message': f"Code block nested too deeply (depth {depth}, max {self.max_nested_blocks})",
                        'code': ''
                    })
                
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                        check_nesting(child, depth + 1)
                    else:
                        check_nesting(child, depth)
            
            check_nesting(tree)
        
        except SyntaxError:
            pass
        
        return violations
    
    def _run_flake8(self, file_path: Path) -> List[Dict[str, Any]]:
        """Run flake8 linter."""
        violations = []
        
        try:
            result = subprocess.run(
                ['flake8', '--format=json', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                try:
                    flake8_results = json.loads(result.stdout)
                    for file_violations in flake8_results.values():
                        for violation in file_violations:
                            violations.append({
                                'file': str(file_path),
                                'line': violation.get('line_number', 0),
                                'type': 'flake8',
                                'severity': 'low',
                                'message': f"{violation.get('code', '')}: {violation.get('text', '')}",
                                'code': violation.get('code', '')
                            })
                except json.JSONDecodeError:
                    pass
        
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass  # Flake8 not available or timeout
        
        return violations
    
    def _run_pylint(self, file_path: Path) -> List[Dict[str, Any]]:
        """Run pylint linter."""
        violations = []
        
        try:
            result = subprocess.run(
                ['pylint', '--output-format=json', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                try:
                    pylint_results = json.loads(result.stdout)
                    for issue in pylint_results:
                        severity_map = {
                            'error': 'high',
                            'warning': 'medium',
                            'convention': 'low',
                            'refactor': 'medium'
                        }
                        
                        violations.append({
                            'file': str(file_path),
                            'line': issue.get('line', 0),
                            'type': 'pylint',
                            'severity': severity_map.get(issue.get('type', ''), 'low'),
                            'message': f"{issue.get('symbol', '')}: {issue.get('message', '')}",
                            'code': issue.get('symbol', '')
                        })
                except json.JSONDecodeError:
                    pass
        
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass  # Pylint not available or timeout
        
        return violations
    
    def _count_by_severity(self, violations: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count violations by severity."""
        counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for violation in violations:
            severity = violation.get('severity', 'low')
            counts[severity] = counts.get(severity, 0) + 1
        
        return counts

