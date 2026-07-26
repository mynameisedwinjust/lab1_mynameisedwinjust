# Lab 1: Grade Evaluator & Archiver

A small Python + Bash toolkit that evaluates a student's grades from a CSV file
and archives that file for the next batch of data.

## Files

- grade-evaluator.py - reads a grades CSV, validates it, calculates the final
  grade/GPA, determines Pass/Fail status, and identifies which failed
  formative assignment(s) are eligible for resubmission.
- organizer.sh - archives the current grades.csv with a timestamp, resets a
  fresh empty grades.csv, and logs every run to organizer.log.
- grades.csv - sample grade data (assignment, group, score, weight).

## Requirements

- Python 3
- Bash

## Running the Python Grade Evaluator

Run: python3 grade-evaluator.py

You'll be prompted for a filename, e.g. grades.csv. The script then:

1. Validates every score is between 0 and 100.
2. Validates weights: total = 100, Summative = 40, Formative = 60.
3. Calculates the weighted Total Grade and GPA ((Total / 100) * 5.0).
4. Determines PASSED / FAILED - requires >=50% in both the Formative and
   Summative categories.
5. Lists any failed Formative assignment(s) (score < 50) that carry the
   highest weight among failures, as resubmission target(s), including ties.

### Edge cases handled

- Missing CSV file: clear error, no crash.
- Empty CSV (headers only): clear message, evaluation skipped gracefully.
- Rows with missing or non-numeric score/weight: skipped with a warning.
- Scores outside 0-100 or weights that don't sum correctly: evaluation stops
  with a descriptive error.

## Running the Organizer Shell Script

Run: chmod +x organizer.sh   then   ./organizer.sh

Each run will:

1. Create an archive/ directory if it doesn't exist.
2. Rename the current grades.csv to grades_TIMESTAMP.csv and move it
   into archive/.
3. Create a brand-new, empty grades.csv for the next batch.
4. Append a line to organizer.log recording the timestamp and filenames.
   Log entries accumulate across every run.

## Typical Workflow

python3 grade-evaluator.py
./organizer.sh
python3 grade-evaluator.py
