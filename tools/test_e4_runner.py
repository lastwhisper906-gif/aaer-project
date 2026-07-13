"""E4 러너 로스터·가드 테스트 (CROSSMODEL_PLAN §1/§4/§5, 무호출)."""
import e4_runner as e4


def test_roster_arithmetic_and_order():
    assert len(e4.ROSTER) == 18 and e4.BUDGET == 18            # PLAN §5 cap ~20 내
    groups = [g for g, _, _ in e4.ROSTER]
    # PLAN §4 순서: 홀드아웃 → wave-2 → E1 대조군
    assert groups == ["holdout"] * 3 + ["wave2"] * 6 + ["e1_control"] * 9
    ids = [cid for _, _, cid in e4.ROSTER]
    assert len(set(ids)) == 18                                 # 중복 0


def test_roster_ids_resolve_in_case_files():
    cases = e4.load_cases()
    assert len(cases) == 18
    assert all(c["case_id"] for _, c in cases)


def test_model_pin_preregistered():
    assert e4.E4_MODEL == "claude-opus-4-8"                    # PLAN §2
