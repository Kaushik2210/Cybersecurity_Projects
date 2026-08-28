#!/usr/bin/env bash
# Scaffold a new day's project folder from the README template.
#
# Usage: ./scripts/new_day.sh <day-number> <slug>
# Example: ./scripts/new_day.sh 07 vulnerability-assessment
#   -> creates projects/day-07-vulnerability-assessment/

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <day-number> <slug>"
  echo "Example: $0 07 vulnerability-assessment"
  exit 1
fi

# Zero-pad the day number to two digits.
DAY_NUM=$(printf "%02d" "$((10#$1))")
SLUG="$2"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DAY_DIR="$REPO_ROOT/projects/day-${DAY_NUM}-${SLUG}"

if [ -d "$DAY_DIR" ]; then
  echo "Error: $DAY_DIR already exists." >&2
  exit 1
fi

mkdir -p "$DAY_DIR/code" "$DAY_DIR/evidence"

# Seed the README from the template, filling in the day number.
sed "s/Day NN/Day ${DAY_NUM}/g" "$REPO_ROOT/templates/PROJECT_README_TEMPLATE.md" \
  > "$DAY_DIR/README.md"

cat > "$DAY_DIR/walkthrough.md" <<EOF
# Day ${DAY_NUM} — Walkthrough

Narrated, step-by-step commands for this project. Each step: what you run, what
it does, and what the expected output looks like.

## Step 1
\`\`\`bash
# command here
\`\`\`
Expected output:
\`\`\`
...
\`\`\`

<!-- Screenshot placeholder: ![](screens/01.png) -->
EOF

cat > "$DAY_DIR/notes.md" <<EOF
# Day ${DAY_NUM} — Notes

## What I learned

## What broke and how I fixed it

## Interview questions someone could ask me about this
1. Q:
   A:
EOF

echo "Created $DAY_DIR"
echo "  README.md, walkthrough.md, notes.md, code/, evidence/"
