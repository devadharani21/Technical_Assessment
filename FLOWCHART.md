# Code Analytics Framework - Flowchart

## Overall System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      START: User Input                          │
│              python main.py --directory <path>                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Load Configuration                           │
│              (config/analysis_config.yaml)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Find Test Files                                 │
│        - Scan directory for test_*.py files                     │
│        - Apply include/exclude patterns                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Initialize Analyzers                               │
│  ┌──────────────────────────────────────────────────┐          │
│  │ 1. CodingStandardsAnalyzer                       │          │
│  │ 2. DuplicationDetector                           │          │
│  │ 3. FlakyPatternDetector                          │          │
│  └──────────────────────────────────────────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ANALYSIS PHASE                                 │
│                (For Each Test File)                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌─────────────────────┐   ┌─────────────────────┐
    │ Coding Standards    │   │  Duplication        │
    │    Analysis         │   │   Detection         │
    │  - Line length      │   │  - Hash blocks      │
    │  - Naming           │   │  - Compare files    │
    │  - Complexity       │   │  - Find matches     │
    │  - Nesting          │   │                     │
    └──────────┬──────────┘   └──────────┬──────────┘
               │                         │
               ▼                         ▼
    ┌─────────────────────┐
    │  Flaky Patterns     │
    │    Detection        │
    │  - time.sleep()     │
    │  - Implicit waits   │
    │  - External calls   │
    │  - Race conditions  │
    └──────────┬──────────┘
               │
               ▼
                            

┌─────────────────────────────────────────────────────────────────┐
│              Aggregate Results                                  │
│  - Collect all violations                                       │
│  - Calculate severity breakdown                                 │
│  - Generate summary statistics                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           Generate Excel Report                                 │
│                                                                 │
│  Sheet 1: Summary                                               │
│  Sheet 2: Flaky Patterns                                        │
│  Sheet 3: Code Duplication                                      │
│  Sheet 4: Coding Standards                                      │
│  Sheet 5: All Issues                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Save Report                                        │
│        reports/analysis_report.xlsx                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           Display Summary to Console                            │
│  - Total issues by severity                                     │
│  - Flaky pattern statistics                                     │
│  - Duplication percentage                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                          [END]
```

---

## Detailed Analysis Flow per File

```
┌─────────────────────────────────────────────────────────────────┐
│                   Input: test_file.py                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Read File Content                             │
│                   Parse to AST                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │
                ▼            ▼
     ┌──────────────┐ ┌──────────────┐
     │   Coding     │ │    Flaky     │
     │  Standards   │ │   Patterns   │
     └──────┬───────┘ └──────┬───────┘
            │                │
            │                │
            ▼                ▼
     [Violations]        [Issues]
            │                │
            └────────────────┘
                             │
                             ▼
                    [Combined Results]
```

---

## Coding Standards Analyzer Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              Coding Standards Analyzer                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│ Check Line   │   │ Check Naming     │   │ Check Function │
│   Length     │   │  Conventions     │   │   Complexity   │
│              │   │                  │   │                │
│ - Max 120    │   │ - test_ prefix   │   │ - Calculate CC │
│   chars      │   │ - snake_case     │   │ - Max CC: 10   │
└──────┬───────┘   └────────┬─────────┘   └────────┬───────┘
       │                    │                      │
       ▼                    ▼                      ▼
   [Violations]        [Violations]           [Violations]
       │                    │                      │
       └────────────────────┼──────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Check Nesting    │
                  │   Depth          │
                  │                  │
                  │ - Max depth: 4   │
                  └────────┬─────────┘
                           │
                           ▼
                  [All Violations]
```

---

## Flaky Pattern Detector Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              Flaky Pattern Detector                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│   Timing     │   │ External Deps    │   │ Race Conditions│
│   Issues     │   │                  │   │                │
│              │   │ - requests.get() │   │ - Thread()     │
│ - sleep()    │   │ - HTTP calls     │   │ - .start()     │
│ - wait()     │   │ - socket         │   │ - sync issues  │
└──────┬───────┘   └────────┬─────────┘   └────────┬───────┘
       │                    │                      │
       ▼                    ▼                      ▼
   [Issues]             [Issues]               [Issues]
       │                    │                      │
       └────────────────────┼──────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Test Structure   │
                  │   Analysis       │
                  │                  │
                  │ - Missing assert │
                  │ - Global state   │
                  │ - Random values  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Calculate Risk   │
                  │     Score        │
                  └────────┬─────────┘
                           │
                           ▼
                    [All Issues + Risk]
```

---

## Code Duplication Detector Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              Code Duplication Detector                          │
│                (All files processed)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   [File 1]             [File 2]             [File 3]
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│ Extract      │   │ Extract          │   │ Extract        │
│ Code Blocks  │   │ Code Blocks      │   │ Code Blocks    │
│              │   │                  │   │                │
│ - 6+ lines   │   │ - 6+ lines       │   │ - 6+ lines     │
│ - Functions  │   │ - Functions      │   │ - Functions    │
└──────┬───────┘   └────────┬─────────┘   └────────┬───────┘
       │                    │                      │
       ▼                    ▼                      ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│ Normalize    │   │ Normalize        │   │ Normalize      │
│              │   │                  │   │                │
│ - Remove     │   │ - Remove         │   │ - Remove       │
│   comments   │   │   comments       │   │   comments     │
│ - Strip      │   │ - Strip          │   │ - Strip        │
│   whitespace │   │   whitespace     │   │   whitespace   │
└──────┬───────┘   └────────┬─────────┘   └────────┬───────┘
       │                    │                      │
       ▼                    ▼                      ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│ Generate     │   │ Generate         │   │ Generate       │
│   Hash       │   │   Hash           │   │   Hash         │
└──────┬───────┘   └────────┬─────────┘   └────────┬───────┘
       │                    │                      │
       └────────────────────┼──────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Compare Hashes   │
                  │                  │
                  │ Find duplicates  │
                  │ across files     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Group Duplicates │
                  │                  │
                  │ - Count occurs   │
                  │ - List locations │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Calculate        │
                  │ Duplication %    │
                  └────────┬─────────┘
                           │
                           ▼
                    [Duplication Report]
```

---

## Excel Report Generation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              Excel Reporter                                     │
│         Input: Aggregated Results                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│   Create     │   │   Create         │   │   Create       │
│  Summary     │   │ Flaky Patterns   │   │  Duplication   │
│   Sheet      │   │    Sheet         │   │    Sheet       │
│              │   │                  │   │                │
│ - Metadata   │   │ - File/Line      │   │ - Locations    │
│ - Totals     │   │ - Category       │   │ - Occurrences  │
│ - Breakdown  │   │ - Severity       │   │ - Files        │
└──────┬───────┘   └────────┬─────────┘   └────────┬───────┘
       │                    │                      │
       └────────────────────┼──────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│   Create     │   │   Create         │   │   Create       │
│ Coding       │   │  All Issues      │   │                │
│ Standards    │   │    Sheet         │   │                │
│   Sheet      │   │                  │   │                │
│              │   │ - Combined       │   │                │
│ - Violations │   │ - Sortable       │   │                │
│ - Types      │   │ - Filterable     │   │                │
│ - Messages   │   │                  │   │                │
└──────┬───────┘   └────────┬─────────┘   └────────────────┘
       │                    │
       └────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   Format Sheets  │
                  │                  │
                  │ - Headers        │
                  │ - Colors         │
                  │ - Column widths  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   Save Workbook  │
                  │                  │
                  │ analysis_report  │
                  │     .xlsx        │
                  └────────┬─────────┘
                           │
                           ▼
                        [DONE]
```

---

## Decision Tree: Severity Assignment

```
                    [Issue Detected]
                          │
                          ▼
                    ┌──────────┐
                    │ Syntax   │──Yes──> [CRITICAL]
                    │ Error?   │
                    └────┬─────┘
                         │ No
                         ▼
                    ┌──────────┐
                    │ Flaky    │──Yes──> [HIGH]
                    │ Pattern? │
                    └────┬─────┘
                         │ No
                         ▼
                    ┌──────────┐
                    │ Code     │──Yes──> [MEDIUM]
                    │ Duplication?
                    └────┬─────┘
                         │ No
                         ▼
                    ┌──────────┐
                    │ Style    │──Yes──> [LOW]
                    │ Issue?   │
                    └──────────┘
```

---

## Data Flow Summary

```
Test Files  ──>  Analyzers  ──>  Results  ──>  Reporter  ──>  Excel File
   (.py)         (3 types)      (JSON)      (formatter)      (.xlsx)
     │               │             │              │               │
     │               │             │              │               │
     ▼               ▼             ▼              ▼               ▼
  Source         Process      Aggregate       Format          Output
   Code          & Detect     & Score         & Style        for User
```


