# Michigan Compiled Laws MBP Optimization

This directory contains optimization scripts and resources for the michigancompiledlawsMBP repository.

## Repository Statistics

- **Total HTML Files:** 236 HTML files
- **Large Files:** Files with >= 5000 lines need splitting
- **Optimization Status:** Starting Phase 2

## Scripts

- `split_html_simple.py` - Split large HTML chapter files into smaller sections by line count

## Optimization Plan

### Phase 2: Content Optimization
1. Split large HTML files (>5000 lines)
2. Create repository indexes
3. Convert HTML to markdown where appropriate
4. Create search indexes

### Files to Split (Top Priority)
- Chapter 500.html (55,843 lines)
- Chapter 324.html (49,844 lines)
- Chapter 4.html (43,607 lines)
- Chapter 333.html (36,851 lines)
- Chapter 760 Code of Criminal Procedure.html (23,565 lines)
- Chapter 760 - 777.html (23,565 lines)
- Chapter 388.html (22,385 lines)
- Chapter 257.html (22,336 lines)
- Chapter 600.html (21,047 lines)
- Chapter 125.html (20,783 lines)

## Usage

```bash
# Split top 5 large files
python optimization/split_html_simple.py .

# Split specific file
python optimization/split_html_simple.py path/to/file.html
```

## Integration

This repository is part of the Ω-CONVERGENCE MICHIGAN LEGAL INTELLIGENCE SINGULARITY.
See [Michigan-MCLA/OPTIMIZATION_MASTER_PLAN.md](https://github.com/fatcrapinmybutt/Michigan-MCLA/blob/main/OPTIMIZATION_MASTER_PLAN.md) for the complete optimization roadmap.
