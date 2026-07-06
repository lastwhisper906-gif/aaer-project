"""Loop-3 예측 봉인 (D16). 예측 파일의 SHA-256을 커밋용 봉인 기록으로 남긴다.

사용: python tools/seal_predictions.py [scoring/loop3/predictions.md]
  → scoring/loop3/sealed_hash.txt 생성. 이 파일을 본 실행 **전에** 커밋+push해야
    봉인이 성립한다 (커밋 타임스탬프가 증거). 예측 파일 자체는 실행 후 공개해도 됨.
"""
import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "scoring/loop3/predictions.md"
    if not target.is_file():
        print(f"{target}: 예측 파일 없음 — prediction_form.md를 채워 이 경로에 저장할 것")
        return 1
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    out = REPO / "scoring/loop3/sealed_hash.txt"
    out.write_text(f"sha256({target.name}) = {digest}\n", encoding="utf-8")
    print(f"sealed: {digest}\n→ {out} 를 본 실행 전에 커밋+push해야 봉인 성립 (D16/D15)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
