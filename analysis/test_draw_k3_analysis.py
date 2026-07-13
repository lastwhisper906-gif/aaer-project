"""draw_k3_analysis tier_block 픽스처 테스트 (무호출) — flip 방향·병기 통계 존재."""
import draw_k3_analysis as dk


def _row(cid, tier, group, draws):
    import statistics
    r = {"case_id": cid, "tier": tier, "group": group, "draws": draws}
    r["median3"] = statistics.median(draws)
    r["band_min_max"] = [min(draws), max(draws)]
    r["flag_draw1"] = draws[0] >= dk.FLAG
    r["flag_median3"] = r["median3"] >= dk.FLAG
    r["flip"] = (None if r["flag_draw1"] == r["flag_median3"] else
                 "gained_flag" if r["flag_median3"] else "lost_flag")
    return r


def test_tier_block_flips_and_co_report():
    rows = [
        _row("t1", "wave1", "treatment", [55, 45, 40]),   # draw1 flag, median 45 → lost
        _row("t2", "wave1", "treatment", [45, 60, 55]),   # draw1 no, median 55 → gained
        _row("t3", "wave1", "treatment", [80, 82, 78]),   # 안정 flag
        _row("c1", "wave1", "control", [20, 25, 22]),
        _row("c2", "wave1", "control", [30, 28, 35]),
    ]
    blk = dk.tier_block(rows, "wave1")
    assert blk["flip_rate"] == "2/5"
    dirs = {f["case_id"]: f["direction"] for f in blk["flips"]}
    assert dirs == {"t1": "lost_flag", "t2": "gained_flag"}
    s = blk["median3_stats_co_report"]
    assert s["auc"] == 1.0 and "병기 전용" in s["note"]
