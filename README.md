# 취업 성공 관리 시스템

> Flask + MySQL + React를 활용한 풀스택 취업 준비 관리 시스템

## 프로젝트 소개

백엔드 개발자 취업을 위한 **실전 프로젝트**로, 출석 관리, 고정 스케줄, 회사 지원 현황, 코딩테스트 기록을 체계적으로 관리하는 웹 애플리케이션입니다.

## 기술 스택

### Backend
- **Flask** 3.0.0
- **SQLAlchemy** (MySQL ORM)
- **Flask-JWT-Extended** (JWT 인증)
- **Flask-Bcrypt** (비밀번호 암호화)
- **PyMySQL** (MySQL 드라이버)

### Frontend
- **Vanilla JavaScript** (ES6+)
- **HTML5 / CSS3**
- **Fetch API** (RESTful 통신)

### Database
- **MySQL** 8.0+

## 주요 기능

### 1. 회원 인증
- 회원가입 / 로그인
- JWT 토큰 기반 인증
- Bcrypt 비밀번호 암호화

### 2. 출석 체크
- 일일 출석 기록
- 월별 캘린더 시각화
- 총 출석일 추적

### 3. 고정 스케줄 관리
- 요일별 고정 스케줄 (월~일)
- 스케줄 수정 (시간, 활동, 특이사항)
- 휴무 처리 (is_active 토글)
- 주간 학습 시간 자동 계산

### 4. 회사 지원 현황
- 회사 정보 등록 (회사명, 직무, 날짜)
- 상태 관리: 서류 지원 → 서류 합격 → 면접 완료 → 최종 합격/불합격
- 상태별 필터링
- 메모 기능

### 5. 코딩테스트
- 문제 풀이 기록 (제목, 레벨, 플랫폼)
- Level 1-5 분류
- 진행률 시각화 (목표: 100문제)
- 상태 관리: 해결/미해결/복습 필요
- 메모 기능

### 6. 대시보드
- 총 출석일
- 코딩테스트 해결 문제 수
- 회사 지원 수
- 주간 학습 시간

## 설치 및 실행

### 1. 사전 준비
- Python 3.8+
- MySQL 8.0+
- DBEaver에서 DB 생성: `corsor-job-hunt`

### 2. 백엔드 설치
```bash
cd backend
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일이 이미 생성되어 있습니다:
```
DB_NAME=corsor-job-hunt
DB_USER=root
DB_PASSWORD=1234
```

### 4. 백엔드 실행
```bash
cd backend
python app.py
```
서버가 `http://localhost:5000`에서 실행됩니다.

### 5. 프론트엔드 실행
```bash
cd frontend
# Live Server 또는 간단한 HTTP 서버로 실행
# VS Code: Live Server 확장 사용
# 또는
python -m http.server 8000
```
브라우저에서 `http://localhost:8000` 접속

## API 엔드포인트

### 인증
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/me` - 현재 사용자 정보

### 출석
- `GET /api/attendance` - 출석 목록
- `POST /api/attendance` - 출석 체크
- `GET /api/attendance/stats` - 출석 통계

### 스케줄
- `GET /api/schedules?day_of_week={0-6}` - 스케줄 조회
- `PUT /api/schedules/:id` - 스케줄 수정
- `POST /api/schedules/:id/toggle` - 스케줄 활성화/비활성화

### 회사
- `GET /api/companies` - 회사 목록
- `POST /api/companies` - 회사 추가
- `PUT /api/companies/:id` - 회사 수정
- `DELETE /api/companies/:id` - 회사 삭제
- `GET /api/companies/stats` - 회사 통계

### 코딩테스트
- `GET /api/coding` - 문제 목록
- `POST /api/coding` - 문제 추가
- `PUT /api/coding/:id` - 문제 수정
- `DELETE /api/coding/:id` - 문제 삭제
- `GET /api/coding/stats` - 코딩 통계

### 대시보드
- `GET /api/dashboard` - 통합 대시보드 데이터

## DB 스키마

### users
- id, username, email, password, created_at

### attendances
- id, user_id, date, created_at

### schedules
- id, user_id, day_of_week (0-6), start_time, end_time, activity, is_active, notes

### companies
- id, user_id, name, position, status, applied_date, memo

### coding_problems
- id, user_id, title, level, platform, status, solved_date, memo

## 특징

### ✅ 백엔드 포트폴리오 가치
- RESTful API 설계
- JWT 인증 구현
- SQLAlchemy ORM 활용
- 관계형 DB 설계 (1:N 관계)
- 비밀번호 암호화

### ✅ 실전 프로젝트
- 본인이 직접 사용하는 시스템
- 실제 취업 준비 과정을 관리
- 면접에서 "이 시스템을 개발한 이유"를 설명 가능

### ✅ 포트폴리오 웹사이트 디자인 적용
- 깔끔한 UI/UX
- 반응형 디자인
- 모바일 친화적

## 배포

### Backend
- Render.com (무료)
- Railway (무료)

### Frontend
- Vercel (무료)
- Netlify (무료)

## 개발자

**최연재** - Backend Developer
- GitHub: [@yeonjaegit](https://github.com/yeonjaegit)

---

**취업 성공까지 화이팅! 🎯**
