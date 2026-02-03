# 취업 성공 관리 시스템

> Flask + MySQL + React를 활용한 풀스택 취업 준비 관리 시스템

## 프로젝트 소개

백엔드 개발자 취업을 위한 **실전 프로젝트**로, 출석 관리, 주별 스케줄, 회사 지원 현황, 코딩테스트 기록을 체계적으로 관리하는 웹 애플리케이션입니다.

- **관리자 전용**: 단일 계정으로 로그인 시 모든 CRUD 가능
- **읽기 전용**: 비로그인 시 데이터 조회만 가능 (공개 대시보드)

## 📊 공부 현황

<!-- PROGRESS_START -->
| 출석 | 코딩테스트 | 회사 지원 | 오늘 일정 |
|:---:|:---:|:---:|:---:|
| 📅 **1**일 | 📝 **0**/0 | 🏢 **0**건 | ✅ **0**개 |

<details>
<summary>상세 보기</summary>

**📅 출석** · 최근: 2026-02-03 · 최근 7일: 02/03

**📝 코딩테스트** · L1: 0 / L2: 0 / L3+: 0

**🏢 회사** · 서류지원 0 · 서류합격 0 · 면접 0 · 합격 0 · 불합격 0

</details>

<sub>🕐 2026-02-03 02:21</sub>
<!-- PROGRESS_END -->

<details>
<summary>갱신 방법</summary>

```bash
python scripts/update_readme_progress.py
```
</details>

## 기술 스택

### Backend
- **Flask** 3.0.0
- **SQLAlchemy** (MySQL ORM)
- **Flask-JWT-Extended** (JWT 인증, Access/Refresh Token)
- **Flask-Bcrypt** (비밀번호 암호화)
- **Flask-CORS**
- **PyMySQL** (MySQL 드라이버)

### Frontend
- **React** 18
- **Vite** 6
- **Axios** (RESTful 통신)

### Database
- **MySQL** 8.0+

## 주요 기능

### 1. 회원 인증
- 로그인 (관리자 전용, 회원가입 UI 비노출)
- JWT Access/Refresh 토큰 기반 인증
- Bcrypt 비밀번호 암호화

### 2. 출석 체크
- 일일 출석 기록
- 월별 캘린더 시각화
- 총 출석일 추적

### 3. 주별 스케줄 관리
- **매주 새 스케줄** (이번 주 수정이 다음 주에 영향 없음)
- 기본 템플릿: 09-11 코딩테스트, 11-13 회사지원, 13-14 점심, 14-17 프로젝트복기, 17-18 정리 및 복습, 18-21 운동
- 수·토·일 기본 휴무 (요일별 수정 가능)
- 일정 추가/수정/삭제
- 특정 시간대 휴무 처리 (ON/OFF 토글)
- 전체 휴무 / 기본 복원
- 순서 변경 (위아래 스왑)
- 당일 체크리스트 (완료 여부 표시)
- 주간 네비게이션 (이전 주 / 다음 주 / 이번 주)

### 4. 회사 지원 현황
- 회사 정보 등록 (회사명, 직무, 지원일)
- 상태: 서류 지원 → 서류 합격 → 면접 완료 → 최종 합격/불합격
- 서류 합격 시 면접일 설정
- 메모 기능

### 5. 코딩테스트
- 문제 풀이 기록 (제목, 레벨, 플랫폼)
- Level 0-5 분류
- 해결/미해결 상태
- 해결일 기록
- 메모 기능

### 6. 대시보드
- 총 출석일
- 회사 지원 수 (상태별)
- 코딩테스트 해결 문제 수
- 주간 일정 활성 개수

## 설치 및 실행

### 1. 사전 준비
- Python 3.8+
- Node.js 18+
- MySQL 8.0+

### 2. DB 생성
MySQL에서 `cursor-job-hunt` 데이터베이스 생성

### 3. 백엔드
```bash
cd backend
pip install -r requirements.txt
```

`.env` 파일 설정 (backend 폴더에):
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=1234
DB_NAME=cursor-job-hunt
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

관리자 계정 생성:
```bash
python create_admin.py
# 기본: admin / admin1234
```

실행:
```bash
python app.py
# 또는 flask run
```
→ `http://localhost:5000`

### 4. 프론트엔드
```bash
cd frontend
npm install
npm run dev
```
→ `http://localhost:5173` (Vite 개발 서버, /api → 5000 프록시)

## API 엔드포인트

### 인증
- `POST /api/auth/login` - 로그인
- `POST /api/auth/refresh` - 토큰 갱신
- `GET /api/auth/me` - 현재 사용자

### 공개 (인증 불필요)
- `GET /api/public/dashboard` - 대시보드 통계
- `GET /api/public/attendance` - 출석 목록
- `GET /api/public/schedules?week_start=&day_of_week=` - 일정
- `GET /api/public/companies` - 회사 목록
- `GET /api/public/coding` - 코딩 문제 목록

### 출석
- `GET /api/attendance`
- `POST /api/attendance`
- `GET /api/attendance/stats`

### 스케줄
- `GET /api/schedules?week_start=&day_of_week=` - 조회 (해당 주 없으면 기본 생성)
- `POST /api/schedules` - 추가
- `PUT /api/schedules/:id` - 수정
- `DELETE /api/schedules/:id` - 삭제
- `POST /api/schedules/day-off/:day` - 해당 요일 전체 휴무
- `POST /api/schedules/reset-day/:day` - 해당 요일 기본 복원
- `POST /api/schedules/swap` - 인접 일정 내용 교환
- `POST /api/schedules/:id/toggle` - 활성화/비활성화
- `GET /api/schedule-checks?date=` - 당일 체크 현황
- `POST /api/schedule-checks` - 체크 토글

### 회사
- `GET /api/companies`
- `POST /api/companies`
- `PUT /api/companies/:id`
- `DELETE /api/companies/:id`
- `GET /api/companies/stats`

### 코딩테스트
- `GET /api/coding`
- `POST /api/coding`
- `PUT /api/coding/:id`
- `DELETE /api/coding/:id`
- `GET /api/coding/stats`

### 대시보드
- `GET /api/dashboard` - 인증 필요

## DB 스키마

### users
- id, username, email, password, created_at

### attendances
- id, user_id, date, created_at

### schedules
- id, user_id, **week_start_date**, day_of_week (0-6), start_time, end_time, activity, is_active, notes, created_at, updated_at

### schedule_checks
- id, user_id, check_date, schedule_id, is_checked, created_at

### companies
- id, user_id, name, position, status, applied_date, **interview_date**, memo, created_at, updated_at

### coding_problems
- id, user_id, title, level, platform, status, solved_date, memo, created_at, updated_at

## 특징

- RESTful API
- JWT 인증 (Access + Refresh)
- SQLAlchemy ORM
- 주별 스케줄 (매주 독립)
- 읽기 전용 공개 모드
- 반응형 UI
- URL 해시로 탭 유지 (새로고침 시 현재 탭 유지)

## 배포

- 웹 배포는 하지 않음 (로컬 전용)
- README 공부 현황만 매일 갱신 후 GitHub에 push하여 포트폴리오로 활용

## 개발자

**최연재** - Backend Developer  
GitHub: [@yeonjaegit](https://github.com/yeonjaegit)

---

**취업 성공까지 화이팅! 🎯**
