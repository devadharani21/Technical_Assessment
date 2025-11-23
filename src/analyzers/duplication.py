"""Duplication Detector - Identifies duplicate code blocks."""

import ast
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict


class DuplicationDetector:
    """Detects code duplication across test files."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the detector with configuration.
        
        Args:
            config: Configuration dictionary containing duplication settings
        """
        self.config = config.get('duplication', {})
        self.min_lines = self.config.get('min_lines', 6)
        self.min_tokens = self.config.get('min_tokens', 50)
        self.ignore_comments = self.config.get('ignore_comments', True)
        self.ignore_whitespace = self.config.get('ignore_whitespace', True)
        self.code_blocks = defaultdict(list)
    
    def analyze_files(self, file_paths: List[Path]) -> Dict[str, Any]:
        """
        Analyze multiple files for code duplication.
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Dictionary containing duplication findings
        """
        # First pass: collect all code blocks
        for file_path in file_paths:
            self._extract_code_blocks(file_path)
        
        # Second pass: find duplicates
        duplicates = self._find_duplicates()
        
        return {
            'total_files_analyzed': len(file_paths),
            'total_duplicates': len(duplicates),
            'duplicates': duplicates,
            'duplication_percentage': self._calculate_duplication_percentage(duplicates)
        }
    
    def _extract_code_blocks(self, file_path: Path):
        """Extract code blocks from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Extract line-based blocks
            for i in range(len(lines) - self.min_lines + 1):
                block = lines[i:i + self.min_lines]
                normalized_block = self._normalize_code(block)
                
                if normalized_block.strip():
                    block_hash = self._hash_code(normalized_block)
                    self.code_blocks[block_hash].append({
                        'file': str(file_path),
                        'start_line': i + 1,
                        'end_line': i + self.min_lines,
                        'code': '\n'.join(block)
                    })
            
            # Extract function-level duplicates
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_code = ast.get_source_segment(content, node)
                        if func_code:
                            normalized = self._normalize_code([func_code])
                            func_hash = self._hash_code(normalized)
                            self.code_blocks[f"func_{func_hash}"].append({
                                'file': str(file_path),
                                'start_line': node.lineno,
                                'end_line': node.end_lineno,
                                'code': func_code,
                                'type': 'function',
                                'name': node.name
                            })
            except SyntaxError:
                pass
        
        except Exception as e:
            print(f"Error extracting blocks from {file_path}: {e}")
    
    def _normalize_code(self, lines: List[str]) -> str:
        """Normalize code for comparison."""
        code = '\n'.join(lines)
        
        if self.ignore_comments:
            # Remove single-line comments
            code = '\n'.join([
                line.split('#')[0] if '#' in line else line
                for line in code.split('\n')
            ])
        
        if self.ignore_whitespace:
            # Normalize whitespace
            code = ' '.join(code.split())
        
        return code
    
    def _hash_code(self, code: str) -> str:
        """Generate hash for code block."""
        return hashlib.md5(code.encode()).hexdigest()
    
    def _find_duplicates(self) -> List[Dict[str, Any]]:
        """Find duplicate code blocks."""
        duplicates = []
        
        for block_hash, occurrences in self.code_blocks.items():
            if len(occurrences) > 1:
                # Group by file
                files_with_block = {}
                for occurrence in occurrences:
                    file_path = occurrence['file']
                    if file_path not in files_with_block:
                        files_with_block[file_path] = []
                    files_with_block[file_path].append(occurrence)
                
                # Report all duplicates - both within same file and across files
                # This helps identify code that should be refactored
                if len(occurrences) > 1:
                    duplicate_entry = {
                        'hash': block_hash,
                        'occurrences': len(occurrences),
                        'files_affected': len(files_with_block),
                        'locations': occurrences,
                        'severity': self._determine_severity(len(occurrences)),
                        'lines': occurrences[0]['end_line'] - occurrences[0]['start_line'] + 1,
                        'recommendation': 'Consider extracting to a shared utility function or fixture'
                    }
                    duplicates.append(duplicate_entry)
        
        # Sort by number of occurrences
        duplicates.sort(key=lambda x: x['occurrences'], reverse=True)
        
        return duplicates
    
    def _determine_severity(self, occurrences: int) -> str:
        """Determine severity based on number of occurrences."""
        if occurrences >= 5:
            return 'critical'
        elif occurrences >= 3:
            return 'high'
        elif occurrences >= 2:
            return 'medium'
        return 'low'
    
    def _calculate_duplication_percentage(self, duplicates: List[Dict[str, Any]]) -> float:
        """Calculate percentage of duplicated code."""
        if not duplicates:
            return 0.0
        
        total_duplicate_lines = sum(
            d['lines'] * (d['occurrences'] - 1) for d in duplicates
        )
        
        # This is a simplified calculation
        return round(total_duplicate_lines / max(sum(d['lines'] * d['occurrences'] for d in duplicates), 1) * 100, 2)

