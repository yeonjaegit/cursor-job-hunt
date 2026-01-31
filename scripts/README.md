# 자동화 스크립트 사용법

## 📋 daily_checklist.py - 일일 체크리스트 생성

**기능:**
- 오늘 날짜의 체크리스트 자동 생성
- START_HERE.md 업데이트

**사용법:**
```bash
python scripts/daily_checklist.py
```

**결과:**
- `daily-logs/2026-02/checklist-2026-02-02.md` 생성
- START_HERE.md 오늘 날짜로 업데이트

---

## 📊 progress_tracker.py - 진행 상황 추적

**기능:**
- 모든 체크리스트 분석
- 코딩테스트, 회사 지원 통계 계산
- README.md 자동 업데이트

**사용법:**
```bash
python scripts/progress_tracker.py
```

**결과:**
- `stats/progress.json` 저장
- README.md 배지 및 진행 바 업데이트

---

## 🚀 quick_update.py - GitHub 빠른 업데이트

**기능:**
- Git add, commit, push를 한 번에 실행
- 자동으로 커밋 메시지 생성

**사용법:**
```bash
# 기본 사용 (자동 메시지)
python scripts/quick_update.py

# 커스텀 메시지
python scripts/quick_update.py "Bros README 개선 완료"
```

**결과:**
- 모든 변경사항 커밋 및 푸시
- GitHub에 자동 업로드

---

## 💡 매일 사용하는 워크플로우

### 아침 (학습 시작)
```bash
# 1. 오늘의 체크리스트 생성
python scripts/daily_checklist.py

# 2. START_HERE.md 열기
# → Cursor에서 "오늘 학습 시작!"
```

### 저녁 (학습 종료)
```bash
# 1. 진행 상황 업데이트
python scripts/progress_tracker.py

# 2. GitHub에 푸시
python scripts/quick_update.py
```

---

## 🔧 초기 설정 (최초 1회만)

### 1. GitHub Repository 생성
```bash
# GitHub에서 cursor-job-hunt 저장소 생성 후

cd cursor-job-hunt
git init
git add .
git commit -m "feat: 초기 설정"
git branch -M main
git remote add origin https://github.com/yeonjaegit/cursor-job-hunt.git
git push -u origin main
```

### 2. Python 환경 확인
```bash
python --version  # Python 3.8 이상 필요
```

---

## ❓ 문제 해결

### "git push 실패" 오류
```bash
# 원격 저장소 확인
git remote -v

# 없다면 추가
git remote add origin https://github.com/yeonjaegit/cursor-job-hunt.git
```

### "파일을 찾을 수 없습니다" 오류
```bash
# cursor-job-hunt 폴더에서 실행하는지 확인
cd C:\Users\연재\Documents\GitHub\cursor-job-hunt
python scripts/daily_checklist.py
```
