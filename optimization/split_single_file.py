#!/usr/bin/env python3
"""
Split a single HTML file by line count.
"""

import os
from pathlib import Path
from datetime import datetime, timezone


def split_html_file_simple(file_path, target_lines=5000):
    """Split an HTML file into smaller files by line count."""
    file_path = Path(file_path)
    
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


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python split_single_file.py <file_path> [target_lines]")
        print("Default target_lines: 5000")
        sys.exit(1)
    
    file_path = sys.argv[1]
    target_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    
    print(f"=== Splitting {file_path} ===")
    print(f"Target lines per file: {target_lines}")
    
    output_files = split_html_file_simple(file_path, target_lines)
    
    print(f"\n=== Summary ===")
    print(f"Processed {len(output_files)} files")
    print("Optimization complete!")
