# Code Review Analytics Framework for Test Scripts

A comprehensive Python-based tool for analyzing test scripts to identify coding standard violations, code duplication, and flaky test patterns.

## 🎯 Objective

Analyze test scripts for:
- **Coding Standard Violations**: Style issues, naming conventions, complexity
- **Code Duplication**: Repeated code blocks across files
- **Flaky Test Patterns**: Hard-coded sleeps, race conditions, external dependencies

## 📋 Key Features

### 1. Coding Standards Analysis
- Line length violations
- Naming convention checks
- Function length and complexity
- Nested block depth detection

### 2. Code Duplication Detection
- Line-based and function-level duplication
- Cross-file duplicate detection
- Duplication percentage calculation

### 3. Flaky Pattern Detection
- **Timing issues**: Hard-coded sleeps, implicit waits
- **Race conditions**: Threading issues, synchronization problems
- **External dependencies**: Unmocked HTTP requests, network calls
- **Resource management**: Files without context managers, missing cleanup
- **Test structure**: Missing assertions, broad exception handling, global state modifications

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run analysis**
   ```bash
   python main.py --directory ./sample_tests
   ```

3. **View Excel report**
   ```bash
   # Report generated at: reports/analysis_report.xlsx
   ```

## 📁 Project Structure

```
Code-Analytics-Framework/
├── main.py                         # Main entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── config/
│   └── analysis_config.yaml       # Configuration file
├── src/
│   ├── analyzer.py                # Main analyzer orchestrator
│   ├── analyzers/                 # Analysis modules
│   │   ├── coding_standards.py   # Standards checker
│   │   ├── duplication.py        # Duplicate detector
│   │   └── flaky_patterns.py     # Flaky pattern detector
│   └── reporters/
│       └── excel_reporter.py      # Excel report generator
├── sample_tests/                   # Sample test files with issues
│   ├── test_login.py
│   ├── test_checkout.py
│   ├── test_user_profile.py
│   └── test_search.py
└── reports/                        # Output directory (auto-created)
    └── analysis_report.xlsx       # Generated Excel report
```

## 💻 Usage

### Basic Usage

```bash
# Analyze test files in a directory
python main.py --directory ./tests

# Specify output directory
python main.py --directory ./tests --output ./reports

# Save JSON output (for CI/CD integration)
python main.py --directory ./tests --json

# Use custom configuration
python main.py --directory ./tests --config ./custom_config.yaml

# Verbose output
python main.py --directory ./tests --verbose
```

### Command Line Options

```
-d, --directory PATH    Directory containing test scripts (required)
-o, --output PATH       Output directory for reports (default: ./reports)
-c, --config PATH       Path to custom configuration file
--json                  Also save results as JSON
-v, --verbose           Enable verbose output
```

## 📊 Excel Report Structure

The generated Excel report contains multiple sheets:

### 1. Summary Sheet
- Analysis metadata (date, directory, duration)
- Total issues by severity (Critical, High, Medium, Low)
- Flaky pattern statistics
- Code duplication percentage

### 2. Flaky Patterns Sheet
- File, line number, and category
- Severity and detailed message
- Risk score per file
- Actionable recommendations

### 3. Code Duplication Sheet
- Duplicate code blocks
- File locations (start/end lines)
- Number of occurrences
- Files affected
- Recommendations for refactoring

### 4. Coding Standards Sheet
- All style violations
- Line numbers and types
- Severity levels
- Code snippets

### 5. All Issues Sheet
- Combined view of all issues
- Sortable and filterable
- Easy prioritization

## ⚙️ Configuration

Customize analysis via `config/analysis_config.yaml`:

```yaml
coding_standards:
  max_line_length: 120
  max_function_length: 50
  max_complexity: 10
  max_nested_blocks: 4

flaky_patterns:
  timing:
    - pattern: "time\\.sleep\\("
      severity: "high"

duplication:
  min_lines: 6
  min_tokens: 50
```

## 📈 Understanding Key Metrics

### Severity Levels
- **Critical**: Must be fixed immediately (syntax errors, blocking issues)
- **High**: Should be fixed soon (flaky patterns, high complexity)
- **Medium**: Should be addressed (code duplication)
- **Low**: Nice to have (minor style issues)

### Cyclomatic Complexity
- **1-10**: Simple, easy to test
- **11-20**: More complex
- **21-50**: Very complex, hard to test
- **50+**: Extremely complex, unmaintainable

## 🔍 Sample Flaky Pattern Detection

Example findings table in Excel report:

| Script | Line | Pattern | Severity | Recommendation |
|--------|------|---------|----------|----------------|
| test_login.py | 15 | time.sleep(5) | High | Use explicit waits with conditions |
| test_login.py | 41 | requests.post() | High | Mock external HTTP requests |
| test_checkout.py | 149 | random.choice() | High | Use deterministic test data |
| test_user_profile.py | 17 | open() without with | Medium | Use context manager |

## ✅ Best Practices Recommendations

The tool provides actionable recommendations:

1. **Replace hard-coded sleeps** with explicit waits
2. **Mock external dependencies** (API calls, database connections)
3. **Extract duplicate code** to shared utilities or fixtures
4. **Reduce function complexity** by breaking into smaller functions
5. **Add proper assertions** to all test functions
6. **Use context managers** for resource management
7. **Implement proper setup/teardown** methods
8. **Avoid global state** modifications
9. **Use deterministic test data** instead of random values
10. **Follow AAA pattern**: Arrange, Act, Assert

## 🎓 Example Output

### Console Output
```
======================================================================
CODE ANALYTICS FRAMEWORK FOR TEST SCRIPTS
======================================================================

Analyzing: /path/to/sample_tests
Output: /path/to/reports
Report Format: Excel

Found 4 test files to analyze

=== Analyzing Coding Standards ===
=== Detecting Code Duplication ===
=== Detecting Flaky Patterns ===

=== Analysis Complete ===
Duration: 12.34 seconds

======================================================================
ANALYSIS SUMMARY
======================================================================

Total Issues Found: 87

By Severity:
  Critical  : 2
  High      : 25
  Medium    : 35
  Low       : 25

Flaky Test Patterns:
  Files Affected: 4
  Total Issues: 32

Code Duplication:
  Total Duplicates: 3
  Duplication %: 15.25%
```

## 🛠️ Sample Test Files

The `sample_tests/` directory contains intentionally flawed test files demonstrating common issues:

- **test_login.py**: Hard-coded sleeps, missing assertions, external HTTP requests, implicit waits, threading issues
- **test_checkout.py**: Significant code duplication, high complexity, excessive nesting, random values
- **test_user_profile.py**: Global variable modification, file operations without context managers, missing assertions
- **test_search.py**: Hard-coded sleeps, broad exception handling

## 🔧 CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Test Quality Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run analysis
        run: python main.py --directory ./tests --json
      
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: analysis-report
          path: reports/
```

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: No test files found
**Solution**: Check file patterns in config match your test file naming

### Issue: Analysis takes too long
**Solution**: Analyze specific subdirectories or adjust configuration thresholds

## 📦 Dependencies

Core dependencies:
- `pandas` - Data manipulation
- `openpyxl` - Excel file generation
- `pyyaml` - Configuration parsing
- `astroid` - Python AST utilities

## 📝 License

This is a demonstration project for code analytics capabilities.

---

## 🚀 Quick Start Summary

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `python3 main.py --directory sample_tests`
3. **Review**: Open `reports/analysis_report.xlsx`

**Start improving your test quality today!** 🎯
