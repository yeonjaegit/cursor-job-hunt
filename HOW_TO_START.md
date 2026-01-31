# 🚀 매일 학습 시작하는 방법

> **매일 아침 컴퓨터를 켜면 이 가이드를 따라하세요!**

---

## 📌 Step 1: Cursor에서 파일 열기

### 방법 A: START_HERE.md 열기 (추천)
```
C:\Users\연재\Documents\GitHub\cursor-job-hunt\daily-logs\START_HERE.md
```

### 방법 B: 오늘 체크리스트 직접 열기
```
C:\Users\연재\Documents\GitHub\cursor-job-hunt\daily-logs\2026-02\checklist-2026-02-03.md
```

---

## 📌 Step 2: Cursor Chat에서 시작 멘트

Ctrl+L을 눌러 Cursor Chat을 열고:

```
"오늘 학습 시작!"
```

그러면 Cursor가:
1. 오늘 날짜 체크리스트 자동 생성
2. 목표 확인
3. 필요한 작업 안내

---

## 📌 Step 3: 하루 동안 학습

### 코딩테스트 시작할 때
```
C:\Users\연재\Documents\GitHub\coding-test\programmers\level1\
```
폴더로 이동해서 새 문제 파일 생성하거나 예시 문제 참고

**Cursor Chat에서:**
```
"프로그래머스 Level 1 새 문제 만들어줘"
```

### 회사 지원 완료했을 때
```
"회사 2곳 지원했어 - 카카오, 네이버"
```
→ Cursor가 자동으로 체크리스트 업데이트

### 코딩테스트 완료했을 때
```
"코딩테스트 2문제 완료 - 두개뽑아서더하기, 완주하지못한선수"
```

---

## 📌 Step 4: 저녁에 기록 및 커밋

### 오늘 작업 기록
**Cursor Chat에서:**
```
"오늘 작업 기록해줘"
```

Cursor가:
1. 오늘 한 작업 정리
2. 체크리스트 업데이트
3. README 통계 업데이트

---

### GitHub 업데이트 (10초 소요)

**방법 A: 스크립트 실행 (추천)**
```powershell
cd C:\Users\연재\Documents\GitHub\cursor-job-hunt
python scripts\quick_update.py
```

**방법 B: 수동 커밋**
```bash
git add .
git commit -m "docs: 2026-02-03 study log"
git push
```

---

## 💡 자주 사용하는 Cursor 명령어

### 학습 관련
```
"오늘 학습 시작!"              # 아침 시작
"오늘 작업 기록해줘"            # 저녁 정리
"코딩테스트 2문제 완료했어"    # 작업 완료
"회사 3곳 지원했어"            # 지원 완료
```

### 코딩테스트
```
"새 프로그래머스 문제 만들어줘"
"이 코드 최적화해줘"
"시간 복잡도 분석해줘"
"이 문제 힌트 줘"
```

### 프로젝트 복기
```
"Bros 프로젝트 기술 면접 질문 만들어줘"
"Write-Heavy 전략 설명해줘"
"N+1 쿼리 문제 예시 보여줘"
```

### 면접 준비
```
"HTTP와 HTTPS 차이 설명해줘"
"이 답변을 면접관에게 설명하듯이 다시 정리해줘"
```

---

## 🔧 초기 설정 (최초 1회만)

### GitHub Repository 생성 및 연결

```bash
# 1. GitHub에서 새 Repository 생성
#    - 이름: cursor-job-hunt
#    - Public
#    - README 생성 안 함

# 2. 원격 저장소 연결
cd C:\Users\연재\Documents\GitHub\cursor-job-hunt
git remote add origin https://github.com/yeonjaegit/cursor-job-hunt.git
git branch -M main
git push -u origin main

# 3. coding-test도 동일하게
cd C:\Users\연재\Documents\GitHub\coding-test
git remote add origin https://github.com/yeonjaegit/coding-test.git
git branch -M main
git push -u origin main
```

---

## 🎯 하루 루틴 요약

| 시간 | 활동 | Cursor 명령어 |
|------|------|---------------|
| 09:00 | 학습 시작 | "오늘 학습 시작!" |
| 11:00 | 코테 완료 | "코딩테스트 2문제 완료" |
| 15:00 | 회사 지원 | "회사 3곳 지원했어" |
| 21:30 | 저녁 정리 | "오늘 작업 기록해줘" |
| 21:35 | GitHub 푸시 | `python scripts\quick_update.py` |

---

**💡 TIP**: 이 파일을 즐겨찾기해두고 매일 참고하세요!
