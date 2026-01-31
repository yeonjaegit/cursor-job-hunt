"""
일일 체크리스트 생성 및 관리 스크립트
"""
import os
import datetime
from pathlib import Path

# 프로젝트 루트 경로
ROOT_DIR = Path(__file__).parent.parent
DAILY_LOGS_DIR = ROOT_DIR / "daily-logs"

def get_today_date():
    """오늘 날짜 반환"""
    return datetime.date.today()

def create_checklist(date=None):
    """일일 체크리스트 생성"""
    if date is None:
        date = get_today_date()
    
    year_month = date.strftime("%Y-%m")
    date_str = date.strftime("%Y-%m-%d")
    weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
    
    # 월별 폴더 생성
    month_dir = DAILY_LOGS_DIR / year_month
    month_dir.mkdir(parents=True, exist_ok=True)
    
    # 체크리스트 파일 경로
    checklist_path = month_dir / f"checklist-{date_str}.md"
    
    if checklist_path.exists():
        print(f"✅ 체크리스트가 이미 존재합니다: {checklist_path}")
        return checklist_path
    
    # 체크리스트 내용
    content = f"""# 📋 {date_str} ({weekday}) 체크리스트

## ✅ 오늘의 목표

### 1. 코딩테스트 (목표: 2문제)
- [ ] 프로그래머스 Level 1 - 문제 1: ____________
- [ ] 프로그래머스 Level 1 - 문제 2: ____________

**학습 내용:**
- 

**어려웠던 점:**
- 

---

### 2. 회사 지원 (목표: 최대 5곳)
- [ ] 회사 1: ____________
- [ ] 회사 2: ____________
- [ ] 회사 3: ____________
- [ ] 회사 4: ____________
- [ ] 회사 5: ____________

**지원한 회사 메모:**
- 

---

### 3. 프로젝트 복기 (목표: 1시간)
- [ ] 복기 주제: ____________
- [ ] 면접 예상 질문 답변 작성 (3개)

**복기 내용:**
- 

---

### 4. 기술 면접 암기 (목표: 5개)
- [ ] 질문 1: ____________
- [ ] 질문 2: ____________
- [ ] 질문 3: ____________
- [ ] 질문 4: ____________
- [ ] 질문 5: ____________

**암기한 내용:**
- 

---

### 5. 복습/추가 학습
- [ ] 학습 주제: ____________

---

### 6. 운동
- [ ] 복싱 (18:00-21:00)

---

## 💡 Cursor 활용 사례

**오늘 Cursor로 해결한 문제:**
- 

---

## 📝 오늘의 회고

### 잘한 점
- 

### 아쉬운 점
- 

### 내일 개선할 점
- 

---

**작성 시각**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
    
    # 파일 생성
    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 체크리스트 생성 완료: {checklist_path}")
    return checklist_path

def update_start_here(date=None):
    """START_HERE.md 업데이트"""
    if date is None:
        date = get_today_date()
    
    date_str = date.strftime("%Y-%m-%d")
    weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
    year_month = date.strftime("%Y-%m")
    
    start_here_path = DAILY_LOGS_DIR / "START_HERE.md"
    
    content = f"""# 🚀 매일 여기서 시작하세요!

> **컴퓨터 켜면 이 파일을 Cursor로 여세요!**

---

## 오늘 날짜: {date_str} ({weekday})

### ✅ 오늘의 체크리스트

상세 체크리스트는 [`{year_month}/checklist-{date_str}.md`](./{year_month}/checklist-{date_str}.md)에서 확인하세요!

#### 간단 체크
- [ ] 코딩테스트 2문제 완료
- [ ] 회사 지원 완료
- [ ] 프로젝트 복기 완료
- [ ] 기술 면접 암기 완료
- [ ] 운동 완료

---

## 💬 Cursor에게 말하는 방법

### 아침에 시작할 때
```
"오늘 학습 시작!"
```

### 작업 완료했을 때
```
"코딩테스트 2문제 완료했어"
"회사 3곳 지원했어"
```

### 저녁에 기록할 때
```
"오늘 작업 기록해줘"
```

---

**💡 TIP**: 이 파일을 Cursor에서 열고 "오늘 학습 시작!"이라고 말하세요!
"""
    
    with open(start_here_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ START_HERE.md 업데이트 완료")

if __name__ == "__main__":
    print("📋 일일 체크리스트 생성 중...")
    checklist_path = create_checklist()
    update_start_here()
    print("\n🎉 완료! 오늘의 체크리스트를 확인하세요!")
    print(f"   → {checklist_path}")
