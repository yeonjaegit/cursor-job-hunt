# 🔧 초기 설정 가이드

> 최초 1회만 실행하면 됩니다!

---

## 📌 Step 1: GitHub Repository 생성

### 1. GitHub 웹사이트 접속
[https://github.com/new](https://github.com/new)

### 2. Repository 정보 입력
```
Repository name: cursor-job-hunt
Description: Cursor AI를 활용한 취업 준비 과정
Public ✅
Add a README: ❌ (체크 안 함!)
```

### 3. Create repository 클릭

---

## 📌 Step 2: 원격 저장소 연결

### PowerShell 또는 터미널에서 실행

```powershell
# cursor-job-hunt 연결
cd C:\Users\연재\Documents\GitHub\cursor-job-hunt
git remote add origin https://github.com/yeonjaegit/cursor-job-hunt.git
git branch -M main
git push -u origin main
```

### 첫 Push 완료 확인
```
✅ GitHub에서 확인: https://github.com/yeonjaegit/cursor-job-hunt
```

---

## 📌 Step 3: coding-test Repository도 동일하게

```powershell
# coding-test 연결
cd C:\Users\연재\Documents\GitHub\coding-test
git remote add origin https://github.com/yeonjaegit/coding-test.git
git branch -M main
git push -u origin main
```

---

## 📌 Step 4: 이력서에 링크 추가

### 이력서 "깃허브" 항목 수정
```
깃허브: https://github.com/yeonjaegit

추가:
학습 기록: https://github.com/yeonjaegit/cursor-job-hunt
코딩테스트: https://github.com/yeonjaegit/coding-test
```

### 포트폴리오 웹사이트 수정
GitHub 섹션에 추가:
- 학습 기록 링크
- "Cursor AI를 활용한 체계적인 취업 준비" 설명

---

## 📌 Step 5: Python 환경 확인

```powershell
python --version
# Python 3.8 이상이면 OK
```

---

## 🎉 설정 완료!

이제 매일 아침:
1. `START_HERE.md` 파일 열기
2. Cursor Chat에서 "오늘 학습 시작!"
3. 저녁에 `python scripts\quick_update.py`

---

## ❓ 문제 해결

### "git push 실패" 오류
```powershell
# 원격 저장소 확인
git remote -v

# 없으면 다시 추가
git remote add origin https://github.com/yeonjaegit/cursor-job-hunt.git
```

### "Python을 찾을 수 없습니다" 오류
Python 설치 필요:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

---

**⚠️ 이 파일은 설정 완료 후 삭제해도 됩니다!**
