#!/usr/bin/env python3
"""
Simple script to split large HTML chapter files by line count.
No external dependencies required.
"""

import re
import os
from pathlib import Path
from datetime import datetime, timezone


def split_html_file_simple(file_path, target_lines=5000):
    """Split an HTML file into smaller files by line count."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # If file is already small enough, return
    if len(lines) <= target_lines:
        print(f"File {file_path.name} is already small enough ({len(lines)} lines)")
        return [file_path]
    
    # Calculate number of sections needed
    num_sections = (len(lines) // target_lines) + 1
    section_size = len(lines) // num_sections
    
    print(f"Splitting {file_path.name} ({len(lines)} lines) into {num_sections} sections")
    
    # Create output directory
    output_dir = file_path.parent / f"{file_path.stem}_split"
    output_dir.mkdir(exist_ok=True)
    
    # Write each section
    output_files = []
    for i in range(num_sections):
        start = i * section_size
        end = (i + 1) * section_size if i < num_sections - 1 else len(lines)
        section_lines = lines[start:end]
        
        filename = f"{i+1:02d}_part.html"
        
        # Create complete HTML file
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Part {i+1} - {file_path.stem}</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Part {i+1} of {file_path.stem}</h1>
    <p>Lines {start+1} to {end}</p>
    {''.join(section_lines)}
</body>
</html>"""
        
        output_file = output_dir / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        output_files.append(output_file)
        print(f"  Created {output_file.name} ({len(section_lines)} lines)")
    
    # Create index file
    index_content = f"""# {file_path.stem.replace('-', ' ').replace('  ', ' ')} - Split Index

This directory contains the split version of `{file_path.name}`.

**Original File:** {file_path.name} ({len(lines)} lines, {len(content.encode('utf-8')):,} bytes)
**Split Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
**Number of Sections:** {num_sections}

## Sections

"""
    
    for i in range(num_sections):
        output_file = output_dir / f"{i+1:02d}_part.html"
        start_line = i * section_size + 1
        end_line = (i + 1) * section_size if i < num_sections - 1 else len(lines)
        index_content += f"{i+1}. [Part {i+1} - Lines {start_line}-{end_line}](./{output_file.name})\n"
    
    index_file = output_dir / "INDEX.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"  Created INDEX.html")
    
    return output_files + [index_file]


def find_and_split_large_files(repo_path, min_lines=5000, max_files=5):
    """Find and split all large HTML files in a repository."""
    repo_path = Path(repo_path)
    
    # Find all HTML files
    html_files = list(repo_path.glob('*.html'))
    
    # Filter for large files
    large_files = []
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if len(lines) >= min_lines:
            large_files.append((html_file, len(lines)))
    
    # Sort by size (largest first)
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(large_files)} files with >= {min_lines} lines:")
    for html_file, line_count in large_files[:max_files]:
        print(f"  {html_file}: {line_count} lines")
    
    # Split each large file (limit to max_files)
    all_output_files = []
    for html_file, line_count in large_files[:max_files]:
        print(f"\nProcessing {html_file}...")
        try:
            output_files = split_html_file_simple(html_file, min_lines)
            all_output_files.extend(output_files)
        except Exception as e:
            print(f"  Error processing {html_file}: {e}")
    
    return all_output_files


def create_optimization_directory(repo_path):
    """Create optimization directory structure."""
    repo_path = Path(repo_path)
    
    # Create optimization directory
    opt_dir = repo_path / 'optimization'
    opt_dir.mkdir(exist_ok=True)
    
    # Create README
    readme_content = f"""# Michigan Compiled Laws MBP Optimization

This directory contains optimization scripts and resources for the michigancompiledlawsMBP repository.

## Repository Statistics

- **Total HTML Files:** {len(list(repo_path.glob('*.html')))} HTML files
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
"""
    
    with open(opt_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Created optimization directory: {opt_dir}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python split_html_simple.py <repository_path> [min_lines] [max_files]")
        print("Default min_lines: 5000")
        print("Default max_files: 5")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    min_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    max_files = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    print(f"=== Splitting Large HTML Files in {repo_path} ===")
    print(f"Minimum lines to split: {min_lines}")
    print(f"Maximum files to process: {max_files}")
    
    # Create optimization directory
    create_optimization_directory(repo_path)
    
    # Find and split large files
    output_files = find_and_split_large_files(repo_path, min_lines, max_files)
    
    print(f"\n=== Summary ===")
    print(f"Processed {len(output_files)} files")
    print("Optimization complete!")
