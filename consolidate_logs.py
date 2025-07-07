#!/usr/bin/env python3
"""
==================================================
🚀 Batch log consolidator for multiple app folders
==================================================
✅ Groups multiline log entries under one timestamp
✅ Supports multiple input filename patterns
✅ Assigns today's date 00:00:00 for unmatched blocks
✅ Outputs Laravel-style logs:
   [YYYY-MM-DD HH:MM:SS] local.LEVEL: message
"""

import os
import glob
import re
from datetime import datetime

APP_ENV = 'local'

# Directories
INPUT_ROOT = '/var/www/html/storage/logs-files'
OUTPUT_DIR = '/var/www/html/storage/logs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# App folders to include
INCLUDED_FOLDERS = [
    'bi.web',
    'bi.api',
    'idp.api',
    'idp.web',
    'ai.service',
    'bi.jobs',
    'bi.dataservice',
    'ums.web',
]

# Log type configurations
LOG_TYPES = {
    'error': {
        'patterns': ['errors.txt', 'errors.log', 'warnings.log'],
        'outfile': os.path.join(OUTPUT_DIR, 'error.log'),
        'level': 'ERROR',
    },
    'debug': {
        'patterns': ['debug-*.txt', 'debug-info.log'],
        'outfile': os.path.join(OUTPUT_DIR, 'debug.log'),
        'level': 'INFO',
    }
}

# Regex for header lines
header_regex = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+\s+\[\d+\]\s+\w+\s+(.*)'
)

def parse_blocks(lines, forced_level):
    """
    Groups lines into blocks by header lines.
    Returns list of (datetime, formatted log entry) tuples.
    """
    blocks = []
    current_block_lines = []
    current_timestamp = None

    for line in lines:
        line = line.rstrip()
        if not line:
            continue

        header_match = header_regex.match(line)
        if header_match:
            # flush previous block if any
            if current_block_lines:
                blocks.append((current_timestamp, '\n'.join(current_block_lines)))
            # start new block
            timestamp_str, message = header_match.groups()
            try:
                current_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                current_timestamp = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                timestamp_str = current_timestamp.strftime('%Y-%m-%d 00:00:00')
                message = f'Unmatched header: {line.strip()}'
            # First line of block in Laravel format
            first_line = f'[{timestamp_str}] {APP_ENV}.{forced_level}: {message}'
            current_block_lines = [first_line]
        else:
            # Indented / non-header lines → continuation
            if current_block_lines:
                current_block_lines.append(line)
            else:
                # Unmatched line without header context
                today = datetime.today().strftime('%Y-%m-%d')
                fallback_time = f'{today} 00:00:00'
                current_timestamp = datetime.strptime(fallback_time, '%Y-%m-%d %H:%M:%S')
                unmatched_line = f'[{fallback_time}] {APP_ENV}.{forced_level}: Unmatched line: {line.strip()}'
                current_block_lines = [unmatched_line]

    # flush final block
    if current_block_lines:
        blocks.append((current_timestamp, '\n'.join(current_block_lines)))

    return blocks

print("🚀 Starting consolidation...")

for log_type, config in LOG_TYPES.items():
    all_entries = []
    print("\n===============================================")
    print(f"📦 Processing log type: {log_type.upper()}")
    print(f"   ➜ Output file: {config['outfile']}")
    print("===============================================")

    for folder in INCLUDED_FOLDERS:
        input_dir = os.path.join(INPUT_ROOT, folder)

        # Match all patterns for this log type
        matching_files = []
        for pattern in config['patterns']:
            matching_files.extend(glob.glob(os.path.join(input_dir, pattern)))

        if not matching_files:
            print(f"⚠️  No matching files in {folder}")
            continue

        for filepath in sorted(matching_files):
            print(f"✅ Reading: {filepath}")
            with open(filepath, 'r') as f:
                lines = f.readlines()
                blocks = parse_blocks(lines, config['level'])
                all_entries.extend(blocks)

    # Sort by timestamp
    all_entries.sort(key=lambda x: x[0])

    # Write output file
    with open(config['outfile'], 'w') as out:
        for _, block in all_entries:
            out.write(block + '\n')

    print(f"✅ Done: {config['outfile']} written with {len(all_entries)} blocks.")

print("\n🎉 All logs processed successfully!")
