import pandas as pd
import secrets
from typing import Optional


REQUIRED_COLUMNS = {'name', 'email', 'branch', 'section', 'roll_number', 'passout_year'}


def parse_student_csv(file_path: str) -> tuple[list[dict], list[str]]:
    """
    Parse a student CSV/Excel file.
    Returns (students, errors).
    """
    errors = []

    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
    except Exception as e:
        return [], [f"Failed to read file: {str(e)}"]

    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return [], [f"Missing required columns: {', '.join(missing)}"]

    students = []
    for idx, row in df.iterrows():
        row_num = idx + 2  # 1-based + header row
        row_errors = []

        name = str(row.get('name', '')).strip()
        email = str(row.get('email', '')).strip()

        if not name:
            row_errors.append(f"Row {row_num}: name is required")
        if not email or '@' not in email:
            row_errors.append(f"Row {row_num}: valid email is required")

        if row_errors:
            errors.extend(row_errors)
            continue

        students.append({
            'name': name,
            'email': email.lower(),
            'branch': str(row.get('branch', '')).strip(),
            'section': str(row.get('section', '')).strip(),
            'roll_number': str(row.get('roll_number', '')).strip(),
            'passout_year': _safe_int(row.get('passout_year')),
            'temp_password': secrets.token_urlsafe(8),
        })

    return students, errors


def _safe_int(val) -> Optional[int]:
    try:
        return int(val)
    except (TypeError, ValueError):
        return None
