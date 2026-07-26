import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, start=2):
                # Guard against completely blank rows (e.g. trailing newline)
                if not row or all((v is None or str(v).strip() == "") for v in row.values()):
                    continue

                # Guard against missing columns (a truly malformed row)
                required_cols = ('assignment', 'group', 'score', 'weight')
                if any(col not in row or row[col] is None or row[col].strip() == "" for col in required_cols):
                    print(f"Warning: Skipping row {row_num} - missing required field(s).")
                    continue

                # Guard against non-numeric score/weight values
                try:
                    score_val = float(row['score'])
                    weight_val = float(row['weight'])
                except ValueError:
                    print(f"Warning: Skipping row {row_num} - score/weight must be numeric "
                          f"(got score='{row['score']}', weight='{row['weight']}').")
                    continue

                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group': row['group'].strip(),
                    'score': score_val,
                    'weight': weight_val
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Runs the full grade evaluation pipeline:
      a) Score range validation (0-100)
      b) Weight validation (Total=100, Summative=40, Formative=60)
      c) Final Grade + GPA calculation
      d) Pass/Fail determination (>=50% in BOTH categories)
      e) Resubmission logic for failed formative assignments (highest weight, ties included)
      f) Final decision printout
    """
    print("\n--- Processing Grades ---")

    # ---- Edge case: no data at all (empty/fresh CSV) ----
    if not data:
        print("No assignment records found. The CSV file appears to be empty.")
        print("Nothing to evaluate. Please populate the file with grade data and try again.")
        return

    # ---------------------------------------------------------------
    # a) Score range validation (0-100)
    # ---------------------------------------------------------------
    invalid_scores = [a for a in data if not (0 <= a['score'] <= 100)]
    if invalid_scores:
        print("Error: The following assignments have scores outside the valid 0-100 range:")
        for a in invalid_scores:
            print(f"  - {a['assignment']}: {a['score']}")
        print("Please correct the CSV data before evaluation can continue.")
        return

    # ---------------------------------------------------------------
    # b) Weight validation (Total=100, Summative=40, Formative=60)
    # ---------------------------------------------------------------
    total_weight = sum(a['weight'] for a in data)
    formative = [a for a in data if a['group'].lower() == 'formative']
    summative = [a for a in data if a['group'].lower() == 'summative']

    formative_weight = sum(a['weight'] for a in formative)
    summative_weight = sum(a['weight'] for a in summative)

    # Catch unexpected group labels (neither Formative nor Summative)
    other_groups = [a for a in data if a['group'].lower() not in ('formative', 'summative')]
    if other_groups:
        print("Error: Found assignment(s) with an unrecognized 'group' value (must be "
              "'Formative' or 'Summative'):")
        for a in other_groups:
            print(f"  - {a['assignment']}: group='{a['group']}'")
        return

    weight_errors = []
    if abs(total_weight - 100) > 1e-9:
        weight_errors.append(f"Total weight is {total_weight}, expected exactly 100.")
    if abs(summative_weight - 40) > 1e-9:
        weight_errors.append(f"Summative weight is {summative_weight}, expected exactly 40.")
    if abs(formative_weight - 60) > 1e-9:
        weight_errors.append(f"Formative weight is {formative_weight}, expected exactly 60.")

    if weight_errors:
        print("Error: Weight validation failed:")
        for err in weight_errors:
            print(f"  - {err}")
        print("Evaluation cannot proceed until weights are corrected.")
        return

    # ---------------------------------------------------------------
    # c) Final Grade + GPA calculation
    # ---------------------------------------------------------------
    # Each assignment contributes (score * weight / 100) points to the 0-100 scale total.
    total_grade = sum(a['score'] * a['weight'] / 100 for a in data)
    gpa = (total_grade / 100) * 5.0

    # Category-level percentages (each category's weighted score, scaled to that
    # category's own weight so it reads as a 0-100% figure within the category).
    formative_score = sum(a['score'] * a['weight'] / 100 for a in formative)
    summative_score = sum(a['score'] * a['weight'] / 100 for a in summative)

    formative_pct = (formative_score / formative_weight) * 100 if formative_weight else 0
    summative_pct = (summative_score / summative_weight) * 100 if summative_weight else 0

    print(f"Total Weighted Grade: {total_grade:.2f} / 100")
    print(f"Final GPA: {gpa:.2f} / 5.0")
    print(f"Formative Category: {formative_pct:.2f}%")
    print(f"Summative Category: {summative_pct:.2f}%")

    # ---------------------------------------------------------------
    # d) Pass/Fail determination (>=50% in BOTH categories)
    # ---------------------------------------------------------------
    passed = formative_pct >= 50 and summative_pct >= 50
    status = "PASSED" if passed else "FAILED"

    # ---------------------------------------------------------------
    # e) Resubmission logic: failed formative assignments (<50%), highest weight, ties included
    # ---------------------------------------------------------------
    failed_formatives = [a for a in formative if a['score'] < 50]
    resubmission_targets = []

    if failed_formatives:
        max_weight = max(a['weight'] for a in failed_formatives)  # allowed here: not one of the banned Lab-2 functions
        resubmission_targets = [a for a in failed_formatives if a['weight'] == max_weight]

    # ---------------------------------------------------------------
    # f) Final decision printout
    # ---------------------------------------------------------------
    print(f"\nFinal Status: {status}")

    if resubmission_targets:
        print("Resubmission eligible (highest-weight failed formative assignment(s)):")
        for a in resubmission_targets:
            print(f"  - {a['assignment']} (Score: {a['score']}, Weight: {a['weight']})")
    elif failed_formatives:
        print("No resubmission targets identified.")
    else:
        print("No failed formative assignments - no resubmission needed.")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
