"""Flaky Pattern Detector - Identifies patterns that can cause test flakiness."""

import re
import ast
from pathlib import Path
from typing import List, Dict, Any


class FlakyPatternDetector:
    """Detects patterns that commonly cause flaky tests."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the detector with configuration.
        
        Args:
            config: Configuration dictionary containing flaky pattern definitions
        """
        self.config = config.get('flaky_patterns', {})
        self.patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Compile regex patterns from configuration."""
        compiled = {}
        
        for category, patterns in self.config.items():
            compiled[category] = []
            for pattern_def in patterns:
                compiled[category].append({
                    'regex': re.compile(pattern_def['pattern']),
                    'message': pattern_def['message'],
                    'severity': pattern_def['severity']
                })
        
        return compiled
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a single file for flaky patterns.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary containing detected flaky patterns
        """
        flaky_issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Pattern-based detection
            flaky_issues.extend(self._detect_regex_patterns(lines, file_path))
            
            # AST-based detection for more complex patterns
            flaky_issues.extend(self._detect_ast_patterns(content, file_path))
            
            # Analyze test structure
            flaky_issues.extend(self._analyze_test_structure(content, file_path))
            
        except Exception as e:
            flaky_issues.append({
                'file': str(file_path),
                'line': 0,
                'category': 'error',
                'severity': 'critical',
                'message': f"Error analyzing file: {str(e)}",
                'pattern': 'N/A',
                'recommendation': 'Fix syntax errors first'
            })
        
        return {
            'file': str(file_path),
            'total_issues': len(flaky_issues),
            'issues': flaky_issues,
            'risk_score': self._calculate_risk_score(flaky_issues),
            'categories': self._categorize_issues(flaky_issues)
        }
    
    def _detect_regex_patterns(self, lines: List[str], file_path: Path) -> List[Dict[str, Any]]:
        """Detect flaky patterns using regex."""
        issues = []
        
        for category, pattern_list in self.patterns.items():
            for pattern_def in pattern_list:
                for line_num, line in enumerate(lines, 1):
                    if pattern_def['regex'].search(line):
                        issues.append({
                            'file': str(file_path),
                            'line': line_num,
                            'category': category,
                            'severity': pattern_def['severity'],
                            'message': pattern_def['message'],
                            'pattern': pattern_def['regex'].pattern,
                            'code': line.strip(),
                            'recommendation': self._get_recommendation(category)
                        })
        
        return issues
    
    def _detect_ast_patterns(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Detect flaky patterns using AST analysis."""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            # Check for missing assertions in test functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    has_assertion = any(
                        isinstance(child, ast.Assert) or
                        (isinstance(child, ast.Expr) and 
                         isinstance(child.value, ast.Call) and
                         hasattr(child.value.func, 'attr') and
                         child.value.func.attr.startswith('assert'))
                        for child in ast.walk(node)
                    )
                    
                    if not has_assertion:
                        issues.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'category': 'test_structure',
                            'severity': 'high',
                            'message': f"Test function '{node.name}' has no assertions",
                            'pattern': 'missing_assertion',
                            'code': node.name,
                            'recommendation': 'Add assertions to verify expected behavior'
                        })
            
            # Check for try-except blocks that catch all exceptions
            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    for handler in node.handlers:
                        if handler.type is None or (
                            isinstance(handler.type, ast.Name) and 
                            handler.type.id == 'Exception'
                        ):
                            issues.append({
                                'file': str(file_path),
                                'line': node.lineno,
                                'category': 'error_handling',
                                'severity': 'medium',
                                'message': 'Catching broad exceptions can hide test failures',
                                'pattern': 'broad_exception',
                                'code': 'except Exception',
                                'recommendation': 'Catch specific exceptions'
                            })
            
            # Check for random number generation
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if (hasattr(node.func, 'attr') and 
                        node.func.attr in ['random', 'randint', 'choice', 'shuffle']):
                        issues.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'category': 'randomness',
                            'severity': 'high',
                            'message': 'Random values can cause non-deterministic test behavior',
                            'pattern': 'random_value',
                            'code': 'random()',
                            'recommendation': 'Use fixed seeds or deterministic values'
                        })
        
        except SyntaxError:
            pass
        
        return issues
    
    def _analyze_test_structure(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze test structure for potential issues."""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            # Check for setup/teardown issues
            has_setup = False
            has_teardown = False
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name in ['setUp', 'setup_method', 'setup']:
                        has_setup = True
                    if node.name in ['tearDown', 'teardown_method', 'teardown']:
                        has_teardown = True
            
            # Check if setup exists but teardown doesn't
            if has_setup and not has_teardown:
                issues.append({
                    'file': str(file_path),
                    'line': 0,
                    'category': 'resource_management',
                    'severity': 'medium',
                    'message': 'Setup method exists but no teardown - potential resource leak',
                    'pattern': 'missing_teardown',
                    'code': 'setUp without tearDown',
                    'recommendation': 'Add teardown method to clean up resources'
                })
            
            # Check for global state modification
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            # Check if assigning to what looks like a global
                            if target.id.isupper():
                                issues.append({
                                    'file': str(file_path),
                                    'line': node.lineno,
                                    'category': 'global_state',
                                    'severity': 'high',
                                    'message': f"Potential global state modification: {target.id}",
                                    'pattern': 'global_modification',
                                    'code': target.id,
                                    'recommendation': 'Avoid modifying global state in tests'
                                })
        
        except SyntaxError:
            pass
        
        return issues
    
    def _get_recommendation(self, category: str) -> str:
        """Get recommendation based on issue category."""
        recommendations = {
            'timing': 'Use explicit waits with conditions instead of fixed sleeps',
            'race_conditions': 'Use proper synchronization mechanisms and locks',
            'external_dependencies': 'Mock external services and network calls',
            'resource_issues': 'Use context managers and ensure proper cleanup',
            'wait_issues': 'Use WebDriverWait with expected conditions',
            'test_structure': 'Follow AAA pattern: Arrange, Act, Assert',
            'randomness': 'Use fixed seeds or deterministic test data',
            'error_handling': 'Be specific about expected exceptions',
            'global_state': 'Use fixtures or dependency injection',
            'resource_management': 'Implement proper setup and teardown'
        }
        
        return recommendations.get(category, 'Review and refactor the code')
    
    def _calculate_risk_score(self, issues: List[Dict[str, Any]]) -> int:
        """Calculate overall risk score for flakiness."""
        severity_weights = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 2
        }
        
        score = sum(severity_weights.get(issue['severity'], 0) for issue in issues)
        return min(score, 100)  # Cap at 100
    
    def _categorize_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize and count issues."""
        categories = {}
        
        for issue in issues:
            category = issue['category']
            categories[category] = categories.get(category, 0) + 1
        
        return categories

