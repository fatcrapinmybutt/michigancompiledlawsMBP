#!/usr/bin/env python3
"""
Split large HTML chapter files in michigancompiledlawsMBP repository for better performance.
This script identifies and splits HTML files larger than the target size.
"""

import re
import os
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup


def split_html_file(file_path, target_lines=5000):
    """Split an HTML file into smaller files based on section headings."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # If file is already small enough, return
    if len(lines) <= target_lines:
        print(f"File {file_path.name} is already small enough ({len(lines)} lines)")
        return [file_path]
    
    # Parse HTML to find sections
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all top-level headings (h2, h3, etc.)
    sections = []
    current_section = []
    
    # Get all elements
    all_elements = soup.find_all(recursive=False)
    
    # If we can't find clear sections, split by line count
    if not all_elements or len(all_elements) < 3:
        print(f"File {file_path.name} has no clear HTML structure, splitting by line count")
        
        # Split by line count
        num_sections = (len(lines) // target_lines) + 1
        section_size = len(lines) // num_sections
        
        sections = []
        for i in range(num_sections):
            start = i * section_size
            end = (i + 1) * section_size if i < num_sections - 1 else len(lines)
            section_lines = lines[start:end]
            sections.append((f"Part {i+1}", section_lines))
    else:
        # Try to split by h2 headings
        h2_headings = soup.find_all(['h2', 'h3'])
        if h2_headings:
            current_content = []
            for element in soup.children:
                if element.name and element.name in ['h2', 'h3']:
                    if current_content:
                        sections.append((str(current_heading), current_content))
                    current_heading = element
                    current_content = [str(element)]
                else:
                    if hasattr(element, 'name') and element.name:
                        current_content.append(str(element))
            
            if current_content:
                sections.append((str(current_heading), current_content))
        else:
            # Fallback: split by line count
            num_sections = (len(lines) // target_lines) + 1
            section_size = len(lines) // num_sections
            
            sections = []
            for i in range(num_sections):
                start = i * section_size
                end = (i + 1) * section_size if i < num_sections - 1 else len(lines)
                section_lines = lines[start:end]
                sections.append((f"Part {i+1}", section_lines))
    
    # If we have sections, split them
    if len(sections) > 1:
        print(f"Splitting {file_path.name} ({len(lines)} lines) into {len(sections)} sections")
        
        # Create output directory
        output_dir = file_path.parent / f"{file_path.stem}_split"
        output_dir.mkdir(exist_ok=True)
        
        # Write each section
        output_files = []
        for i, (heading, section_content) in enumerate(sections):
            # Clean heading for filename
            clean_heading = re.sub(r'[^\w\s-]', '', heading)
            clean_heading = clean_heading.replace(' ', '_').replace('-', '_')
            clean_heading = re.sub(r'_+', '_', clean_heading).strip('_')
            
            filename = f"{i+1:02d}_{clean_heading[:50]}.html"
            
            # Create HTML wrapper
            if isinstance(section_content, list):
                html_content = '\n'.join(section_content)
            else:
                html_content = str(section_content)
            
            # Create complete HTML file
            full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{heading} - {file_path.stem}</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>{heading}</h1>
    {html_content}
</body>
</html>"""
            
            output_file = output_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            output_files.append(output_file)
            print(f"  Created {output_file.name}")
        
        # Create index file
        index_content = f"""# {file_path.stem.replace('-', ' ').replace('  ', ' ')} - Split Index

This directory contains the split version of `{file_path.name}`.

**Original File:** {file_path.name} ({len(lines)} lines, {len(content.encode('utf-8')):,} bytes)
**Split Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
**Number of Sections:** {len(sections)}

## Sections

"""
        
        for i, (heading, _) in enumerate(sections):
            output_file = output_dir / output_files[i].name
            index_content += f"{i+1}. [{heading}](./{output_file.name})\n"
        
        index_file = output_dir / "INDEX.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"  Created INDEX.html")
        
        return output_files + [index_file]
    else:
        print(f"File {file_path.name} has no clear sections to split")
        return [file_path]


def find_and_split_large_files(repo_path, min_lines=5000):
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
    for html_file, line_count in large_files:
        print(f"  {html_file}: {line_count} lines")
    
    # Split each large file
    all_output_files = []
    for html_file, line_count in large_files[:10]:  # Limit to top 10 for now
        print(f"\nProcessing {html_file}...")
        try:
            output_files = split_html_file(html_file, min_lines)
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

- `split_html_chapters.py` - Split large HTML chapter files into smaller sections

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
# Split all large files
python optimization/split_html_chapters.py .

# Split specific file
python optimization/split_html_chapters.py path/to/file.html
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
        print("Usage: python split_html_chapters.py <repository_path> [min_lines]")
        print("Default min_lines: 5000")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    min_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    
    print(f"=== Splitting Large HTML Files in {repo_path} ===")
    print(f"Minimum lines to split: {min_lines}")
    
    # Create optimization directory
    create_optimization_directory(repo_path)
    
    # Find and split large files
    output_files = find_and_split_large_files(repo_path, min_lines)
    
    print(f"\n=== Summary ===")
    print(f"Processed {len(output_files)} files")
    print("Optimization complete!")
