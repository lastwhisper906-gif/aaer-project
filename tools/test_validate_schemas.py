"""D1 (2026-07-06) 검증기 코드 수준 강제의 단위 테스트 — scheme_type × group 규칙."""
from validate_schemas import check_scheme_type_by_group


def run(cases):
    failures = []
    check_scheme_type_by_group(cases, failures)
    return failures


def test_treatment_requires_scheme_type():
    assert run([{"case_id": "T01", "group": "treatment"}])
    assert run([{"case_id": "T01", "group": "treatment", "scheme_type": []}])
    assert run([{"case_id": "T01", "group": "treatment", "scheme_type": None}])
    assert not run([{"case_id": "T01", "group": "treatment", "scheme_type": ["revenue_recognition"]}])


def test_control_forbids_scheme_type_value():
    assert run([{"case_id": "C01", "group": "control", "scheme_type": ["revenue_recognition"]}])
    assert not run([{"case_id": "C01", "group": "control", "scheme_type": None}])
    assert not run([{"case_id": "C01", "group": "control"}])
