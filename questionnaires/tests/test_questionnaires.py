import re
from pathlib import Path
from typing import Set

import pytest
import yaml
from questionnaire_validator.parser import QuestionnaireParseError, QuestionnaireParser

DATA_ROOT = Path(__file__).parent.parent 


def find_questionnaire_files():
    """Finds all .yaml and .yml files recursively under the DATA_ROOT."""
    yaml_files = list(DATA_ROOT.rglob("*.yaml"))
    yml_files = list(DATA_ROOT.rglob("*.yml"))
    all_files = [
        f for f in yaml_files + yml_files if f.name != "schema-questionnaire-v1.json"
    ]
    if not all_files:
        pytest.fail(
            f"No questionnaire YAML/YML files found under {DATA_ROOT}",
            pytrace=False,
        )

    file_ids = [str(p.relative_to(DATA_ROOT.parent)) for p in all_files]
    return all_files, file_ids


all_files, file_ids = find_questionnaire_files()


@pytest.mark.parametrize("yaml_file_path", all_files, ids=file_ids)
def test_parse_questionnaire(yaml_file_path: Path):
    """Tests that each questionnaire YAML file can be successfully parsed."""
    parser = QuestionnaireParser()

    try:
        content_bytes = yaml_file_path.read_bytes()
        _ = parser.parse(content_bytes, str(yaml_file_path))
    except (QuestionnaireParseError, Exception) as exc:
        pytest.fail(
            f"Failed to parse {yaml_file_path.name}.\n{type(exc).__name__}: {exc}",
            pytrace=False,
        )


@pytest.mark.parametrize("yaml_file_path", all_files, ids=file_ids)
def test_yaml_quoting_norway_problem(yaml_file_path: Path):
    """Tests that questionnaire YAML files don't have the 'Norway problem'
    where unquoted values like YES, NO, country codes, etc. get misinterpreted.
    """
    PROBLEMATIC_VALUES: Set[str] = {
        "YES", "NO", "TRUE", "FALSE",
        "Yes", "No", "True", "False",
        "yes", "no", "true", "false",
        "on", "off", "ON", "OFF",
        "NA",
        "null", "Null", "NULL", "~", "None", "none",
    }

    content = yaml_file_path.read_text()
    lines = content.splitlines()
    errors: list[str] = []

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if "option:" in line:
            match = re.search(r"option:\s*(.+?)(?:\s*#.*)?$", line)
            if match:
                value_part = match.group(1).strip()
                is_quoted = (
                    (value_part.startswith('"') and value_part.endswith('"'))
                    or (value_part.startswith("'") and value_part.endswith("'"))
                )

                if not is_quoted:
                    if value_part.upper() in PROBLEMATIC_VALUES:
                        errors.append(
                            f"Line {line_num}: Unquoted value '{value_part}' will be misinterpreted by YAML. "
                            f'Must be quoted as "{value_part}"'
                        )
                    elif re.match(r"^[\d]+-[\d]+$", value_part) or re.match(
                        r"^[\d]+\+$", value_part
                    ):
                        errors.append(
                            f"Line {line_num}: Numeric range '{value_part}' should be quoted. "
                            f'Must be quoted as "{value_part}" to ensure it\'s treated as a string'
                        )

    try:
        data = yaml.safe_load(content)
        if data and "blocks" in data and isinstance(data["blocks"], list):
            for block_idx, block in enumerate(data["blocks"]):
                if isinstance(block, dict) and "options" in block:
                    for opt_idx, option in enumerate(block["options"]):
                        if isinstance(option, dict) and "option" in option:
                            value = option["option"]
                            if not isinstance(value, str):
                                errors.append(
                                    f"Block {block_idx}, Option {opt_idx}: Value was parsed as {type(value).__name__} "
                                    f"instead of string. This indicates missing quotes in YAML!"
                                )
    except yaml.YAMLError as exc:
        errors.append(f"YAML parsing error: {exc}")

    if errors:
        error_message = f"\nYAML quoting issues found in {yaml_file_path.name}:\n"
        error_message += "\n".join(f"  - {error}" for error in errors)
        error_message += (
            "\n\nThis is the 'Norway problem' - unquoted values are being misinterpreted by YAML!"
        )
        pytest.fail(error_message, pytrace=False)
