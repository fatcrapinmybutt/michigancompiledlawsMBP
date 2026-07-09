#!/bin/bash

# Script to split all remaining large HTML files (>5000 lines) in michigancompiledlawsMBP

echo "=== Starting Batch Split of Remaining Large Files ==="
echo "Date: $(date)"
echo ""

cd /workspace/fatcrapinmybutt__michigancompiledlawsMBP

# List of files to split (all >5000 lines and not yet split)
FILES_TO_SPLIT=(
    "Chapter 445.html"
    "Chapter 380.html"
    "Chapter 450.html"
    "Chapter 3.html"
    "Chapter 211.html"
    "Chapter 440.html"
    "Chapter 400.html"
    "Chapter 700.html"
    "Chapter 141.html"
    "Chapter 722.html"
    "Chapter 205.html"
    "Chapter 330.html"
    "Chapter 28.html"
    "Chapter 339.html"
    "Chapter 460.html"
    "Chapter 207.html"
    "Chapter 487.html"
    "Chapter 338.html"
    "Chapter 18.html"
    "Chapter 287.html"
    "Chapter 123.html"
    "Chapter 81 - 113.html"
    "Chapter 247.html"
    "Chapter 457.html"
)

echo "Files to process: ${#FILES_TO_SPLIT[@]}"
echo ""

SUCCESS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

for file in "${FILES_TO_SPLIT[@]}"; do
    echo "Processing: $file"
    
    # Check if file exists
    if [ ! -f "$file" ]; then
        echo "  ❌ File not found: $file"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi
    
    # Check if already split
    if [ -d "${file%.html}_split" ]; then
        echo "  ⏭️  Already split: $file"
        SKIP_COUNT=$((SKIP_COUNT + 1))
        continue
    fi
    
    # Get line count
    LINE_COUNT=$(wc -l < "$file" 2>/dev/null | awk '{print $1}')
    echo "  Lines: $LINE_COUNT"
    
    # Split the file
    python optimization/split_single_file.py "$file" 5000
    
    if [ $? -eq 0 ]; then
        echo "  ✅ Successfully split: $file"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "  ❌ Failed to split: $file"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    
    echo ""
done

echo "=== Batch Split Summary ==="
echo "Successful: $SUCCESS_COUNT"
echo "Failed: $FAIL_COUNT"
echo "Skipped (already split): $SKIP_COUNT"
echo "Total processed: $((SUCCESS_COUNT + FAIL_COUNT + SKIP_COUNT))"
echo "Date: $(date)"
