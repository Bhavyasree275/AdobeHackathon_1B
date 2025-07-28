#!/bin/bash
set -euo pipefail

INPUT_DIR="/app/input"
OUTPUT_DIR="/app/output"

PERSONA_FILE="$INPUT_DIR/persona.json"
JOB_FILE="$INPUT_DIR/job.txt"

echo "Starting 1B Processing for persona-driven document intelligence..."

for pdf_file in "$INPUT_DIR"/*.pdf; do
    if [ -f "$pdf_file" ]; then
        filename=$(basename "$pdf_file" .pdf)
        echo "Processing $filename.pdf"
        python3 /app/src/main.py "$pdf_file" "$OUTPUT_DIR/${filename}_output.json" "$PERSONA_FILE" "$JOB_FILE"
        echo "Finished $filename.pdf"
    fi
done

echo "All processing complete."