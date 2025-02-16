import pandas as pd
import re

def validate_data(df, rules):
    errors = []

    # Check for null or blank values
    if "null_columns" in rules:
        for column in rules["null_columns"]:
            if column in df.columns:
                null_rows = df[df[column].isnull() | (df[column] == "")].index.tolist()
                if null_rows:
                    errors.append({"column": column, "error": f"Null/blank values found in rows {null_rows}"})
            else:
                errors.append({"column": column, "error": "Missing column in dataset"})

    # Check sum constraints for multiple columns
    if "sum_constraints" in rules:
        for column, expected_sum in rules["sum_constraints"].items():
            if column in df.columns:
                actual_sum = df[column].sum()
                if actual_sum != expected_sum:
                    errors.append({
                        "column": column,
                        "error": f"Sum mismatch: Expected {expected_sum}, got {actual_sum}"
                    })
            else:
                errors.append({"column": column, "error": "Missing column in dataset"})

    # Check multiplication constraints
    if "multiplication_constraints" in rules:
        for constraint in rules["multiplication_constraints"]:
            col1, col2, expected_value = constraint
            if col1 in df.columns and col2 in df.columns:
                incorrect_rows = df[(df[col1] * df[col2]) != expected_value].index.tolist()
                if incorrect_rows:
                    errors.append({
                        "columns": [col1, col2],
                        "error": f"Multiplication mismatch in rows {incorrect_rows}"
                    })
            else:
                errors.append({"columns": [col1, col2], "error": "One or both columns are missing"})

    # Check range constraints
    if "range_constraints" in rules:
        for column, (min_val, max_val) in rules["range_constraints"].items():
            if column in df.columns:
                out_of_range_rows = df[(df[column] < min_val) | (df[column] > max_val)].index.tolist()
                if out_of_range_rows:
                    errors.append({"column": column, "error": f"Out of range values in rows {out_of_range_rows}"})
            else:
                errors.append({"column": column, "error": "Missing column in dataset"})

    # Check unique constraints
    if "unique_constraints" in rules:
        for column in rules["unique_constraints"]:
            if column in df.columns:
                duplicate_rows = df[df[column].duplicated()].index.tolist()
                if duplicate_rows:
                    errors.append({"column": column, "error": f"Duplicate values found in rows {duplicate_rows}"})
            else:
                errors.append({"column": column, "error": "Missing column in dataset"})

    # Check regex validation
    if "regex_constraints" in rules:
        for column, pattern in rules["regex_constraints"].items():
            if column in df.columns:
                invalid_rows = df[~df[column].astype(str).str.match(pattern, na=False)].index.tolist()
                if invalid_rows:
                    errors.append({"column": column, "error": f"Invalid format in rows {invalid_rows}"})
            else:
                errors.append({"column": column, "error": "Missing column in dataset"})

    # Check data type constraints
    if "data_type_constraints" in rules:
        for column, expected_type in rules["data_type_constraints"].items():
            if column in df.columns:
                actual_dtype = str(df[column].dtype)
                if expected_type == "numeric" and not pd.api.types.is_numeric_dtype(df[column]):
                    errors.append({"column": column, "error": f"Expected numeric type, got {actual_dtype}"})
                elif expected_type == "string" and not pd.api.types.is_string_dtype(df[column]):
                    errors.append({"column": column, "error": f"Expected string type, got {actual_dtype}"})
            else:
                errors.append({"column": column, "error": "Missing column in dataset"})

    return errors
