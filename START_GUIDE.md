# 🚀 빠른 시작 가이드

## 1단계: MySQL 확인

DBeaver에서 DB가 이미 생성되어 있는지 확인:
- DB명: `corsor-job-hunt`
- 사용자: `root`
- 비밀번호: `1234`

## 2단계: Python 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

## 3단계: Flask 서버 실행

```bash
cd backend
python app.py
```

성공 메시지:
```
* Running on http://0.0.0.0:5000
```

## 4단계: 프론트엔드 열기

### VS Code 사용자 (권장)
1. `frontend` 폴더의 `index.html` 우클릭
2. "Open with Live Server" 선택
3. 브라우저가 자동으로 열립니다

### 또는 간단한 HTTP 서버
```bash
cd frontend
python -m http.server 8000
```
브라우저에서 `http://localhost:8000` 접속

## 5단계: 첫 사용

1. **회원가입**
   - 사용자명 입력
   - 이메일 입력
   - 비밀번호 입력 (확인 포함)
   - "회원가입" 버튼 클릭

2. **자동 로그인**
   - 회원가입 후 자동으로 로그인됩니다
   - 대시보드가 표시됩니다

3. **고정 스케줄 확인**
   - 회원가입 시 기본 스케줄이 자동 생성됩니다
   - 스케줄 탭에서 확인 가능
   - 월/화/목/금: 09:00-20:00 (코딩테스트, 회사지원, 프로젝트복기, 운동)
   - 수요일: 휴무 (비활성화 상태)

4. **출석 체크**
   - 출석 탭으로 이동
   - "오늘 출석하기" 버튼 클릭
   - 캘린더에 초록색으로 표시됩니다

## 문제 해결

### Backend 오류

#### MySQL 연결 실패
```
Error: Can't connect to MySQL server
```
**해결:**
1. MySQL 서버 실행 확인
2. DBeaver에서 DB 생성 확인: `corsor-job-hunt`
3. `.env` 파일의 DB 정보 확인

#### 모듈 없음
```
ModuleNotFoundError: No module named 'flask'
```
**해결:**
```bash
pip install -r requirements.txt
```

### Frontend 오류

#### CORS 오류
```
Access to fetch has been blocked by CORS policy
```
**해결:**
- Backend가 실행 중인지 확인
- `http://localhost:5000`에 접속되는지 확인

#### 빈 화면
**해결:**
- F12 (개발자 도구) 열기
- Console 탭에서 에러 확인
- Network 탭에서 API 요청 확인

## 테스트 시나리오

### 1. 회원가입 및 로그인
1. 회원가입 (username: test, email: test@test.com, password: test1234)
2. 로그아웃
3. 로그인

### 2. 출석 체크
1. 출석 탭으로 이동
2. "오늘 출석하기" 클릭
3. 캘린더 확인

### 3. 스케줄 관리
1. 스케줄 탭으로 이동
2. 월요일 선택
3. 스케줄 수정 버튼 (✏️) 클릭
4. 시간 또는 활동 수정
5. 저장
6. 휴무 처리 버튼 (🚫) 클릭

### 4. 회사 지원
1. 회사 지원 현황 탭으로 이동
2. "+ 회사 추가" 클릭
3. 정보 입력 (예: 카카오, 백엔드 개발자)
4. 저장
5. 상태 변경 (서류 지원 → 서류 합격)

### 5. 코딩테스트
1. 코딩테스트 탭으로 이동
2. "+ 문제 추가" 클릭
3. 정보 입력 (예: 두 개 뽑아서 더하기, Level 1)
4. 저장
5. 진행률 확인

### 6. 대시보드 확인
1. 대시보드 탭으로 이동
2. 모든 통계 확인
   - 총 출석일: 1일
   - 코딩테스트: 1문제
   - 회사 지원: 1개
   - 주간 학습: 자동 계산

## 다음 단계

1. **매일 아침 루틴**
   - 출석 체크
   - 스케줄 확인

2. **공부 중**
   - 문제 풀면 즉시 기록
   - 회사 지원하면 즉시 기록

3. **저녁 정리**
   - 대시보드 통계 확인
   - 내일 스케줄 미리 조정

4. **배포** (선택)
   - Backend: Render/Railway
   - Frontend: Vercel/Netlify
   - 모바일에서도 사용 가능!

---

**문제가 있으면 언제든 물어보세요! 🚀**
