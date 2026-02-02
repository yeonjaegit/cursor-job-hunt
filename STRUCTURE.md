# 프로젝트 구조

## Backend (Flask)

```
backend/
├── app.py              # 애플리케이션 엔트리포인트
├── config.py           # 설정 (DB, JWT 등)
├── extensions.py       # Flask 확장 (db, jwt, bcrypt)
├── requirements.txt
├── models/             # DB 모델 (기능별 분리)
│   ├── __init__.py
│   ├── user.py
│   ├── attendance.py
│   ├── schedule.py
│   ├── company.py
│   └── coding_problem.py
├── routes/             # API 라우트 (기능별 분리)
│   ├── __init__.py     # 블루프린트 등록
│   ├── auth.py         # /api/auth/*
│   ├── attendance.py   # /api/attendance*
│   ├── schedule.py     # /api/schedules*
│   ├── companies.py    # /api/companies*
│   ├── coding.py       # /api/coding*
│   ├── dashboard.py    # /api/dashboard
│   └── public.py       # /api/public/* (읽기전용)
├── services/           # 비즈니스 로직
│   └── schedule_service.py  # 기본 일정 생성
└── scripts/
    └── create_admin.py # 관리자 계정 생성
```

## Frontend (React + Vite)

```
frontend/src/
├── main.jsx
├── App.jsx
├── App.css
├── index.css
├── api/                # API 클라이언트
│   ├── client.js       # Axios 인스턴스, 인터셉터
│   └── index.js        # API 메서드 (auth, dashboard, attendance 등)
├── contexts/
│   └── AuthContext.jsx
└── components/
    ├── AdminLogin.jsx
    ├── Dashboard.jsx
    ├── Attendance.jsx
    ├── Schedule.jsx
    ├── Companies.jsx
    ├── CodingTest.jsx
    └── Navigation.jsx
```

## 수정 사항 요약

### Backend
- **중복 라우트 제거**: `/api/dashboard`, `/api/public/companies`, `/api/public/coding` 중복 정의 제거
- **Coding stats 응답 형식 통일**: `total`, `solved`, `unsolved` 필드 추가 (프론트 호환)
- **기능별 폴더 구조**: models, routes, services 분리
- **JWT 에러 핸들러**: 401 반환, 한글 메시지

### Frontend
- **API 모듈 분리**: `api/client.js` (Axios), `api/index.js` (API 메서드)
- **AuthContext 버그 수정**: `setLoginJustCompleted` import 추가
- **모달 버튼**: `type="button"` 지정으로 폼 전송 방지
- **불필요 파일 삭제**: `app.js`, `style.css`, `services/api.js`
