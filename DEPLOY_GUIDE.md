# 🚀 배포 가이드

## 시스템 구조

### 🔓 공개 모드 (기본)
- 누구나 접속하여 **읽기 전용**으로 학습 현황 확인 가능
- 출석, 스케줄, 회사 지원, 코딩테스트 모두 조회 가능
- 수정/추가/삭제 버튼은 표시되지 않음

### 🔐 관리자 모드
- 네비게이션의 🔐 아이콘 클릭 → 로그인
- 모든 수정/추가/삭제 기능 활성화
- 출석 체크 가능

---

## Backend 배포 (Render.com)

### 1. GitHub에 Backend 푸시
```bash
cd backend
git init
git add .
git commit -m "Initial backend commit"
git remote add origin https://github.com/yeonjaegit/job-hunt-backend.git
git push -u origin main
```

### 2. Render.com 배포
1. https://render.com 접속 및 가입
2. "New +" → "Web Service" 클릭
3. GitHub 저장소 연결
4. 설정:
   - **Name**: job-hunt-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### 3. 환경 변수 설정
Render 대시보드에서 Environment Variables 추가:
```
SECRET_KEY=your-production-secret-key-here
JWT_SECRET_KEY=your-production-jwt-secret-key-here
DB_HOST=your-mysql-host
DB_PORT=3306
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=corsor-job-hunt
```

### 4. MySQL 데이터베이스
- **PlanetScale** (무료): https://planetscale.com
- 또는 **Railway** (무료): https://railway.app

### 5. gunicorn 추가
`backend/requirements.txt`에 추가:
```
gunicorn==21.2.0
```

---

## Frontend 배포 (GitHub Pages)

### 1. API URL 수정
`frontend/app.js` 1번 라인 수정:
```javascript
const API_BASE_URL = 'https://your-backend-url.onrender.com/api';
```

### 2. GitHub Pages 설정
```bash
cd ..  # cursor-job-hunt 루트로 이동
git add .
git commit -m "Add public read-only mode"
git push origin main
```

GitHub 저장소:
1. Settings → Pages
2. Source: **main** 브랜치 선택
3. 폴더: **/ (root)** 선택
4. Save

### 3. 프론트엔드 파일 루트로 이동
현재 `frontend/` 폴더에 있는 파일들을 **루트**로 이동:
```bash
# 현재 구조
cursor-job-hunt/
  ├── backend/
  └── frontend/
      ├── index.html
      ├── style.css
      └── app.js

# 변경할 구조
cursor-job-hunt/
  ├── backend/
  ├── index.html      ← 루트로 이동
  ├── style.css       ← 루트로 이동
  └── app.js          ← 루트로 이동
```

### 4. 배포 URL 확인
- GitHub Pages URL: `https://yeonjaegit.github.io/cursor-job-hunt/`
- 이 URL을 포트폴리오에 추가!

---

## 대안: Vercel 배포 (추천!)

### Frontend를 Vercel로 배포하는 이유
- GitHub Pages보다 빠름
- 커스텀 도메인 무료
- HTTPS 자동

### Vercel 배포 방법
1. https://vercel.com 접속 및 가입
2. "New Project" 클릭
3. GitHub 저장소 연결
4. 설정:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend/`
   - Deploy 클릭

---

## 첫 계정 생성

### Backend 실행 후 회원가입
```bash
# 로컬에서
cd backend
python app.py
```

**Postman 또는 curl로 첫 계정 생성:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "your-email@gmail.com",
    "password": "your-secure-password"
  }'
```

또는 프론트엔드에서:
1. `frontend/index.html` 임시 수정
2. 회원가입 섹션 주석 해제
3. 브라우저에서 회원가입
4. 다시 주석 처리 후 배포

---

## 보안 체크리스트

### ✅ Backend
- [x] JWT Secret Key 변경 (프로덕션 환경)
- [x] CORS 설정 확인
- [x] 모든 수정/삭제 API는 `@jwt_required()` 적용
- [x] 비밀번호 Bcrypt 암호화

### ✅ Frontend
- [x] 회원가입 UI 숨김
- [x] 관리자 로그인은 🔐 아이콘으로만 접근
- [x] 비로그인 시 수정/삭제 버튼 숨김
- [x] 공개 API (`/api/public/*`) 사용

---

## 사용 시나리오

### 일반 방문자
1. `https://yeonjaegit.github.io/cursor-job-hunt/` 접속
2. 대시보드 통계 확인
3. 출석 캘린더 확인
4. 스케줄 조회
5. 회사 지원 현황 조회
6. 코딩테스트 진행률 조회

### 관리자 (본인)
1. 네비게이션의 🔐 아이콘 클릭
2. 로그인 (username: admin, password: ***)
3. 출석 체크
4. 스케줄 수정
5. 회사 추가/수정/삭제
6. 문제 추가/수정/삭제
7. 로그아웃 (읽기 전용으로 전환)

---

## 포트폴리오 활용

### 이력서/자기소개서
```
📌 취업 성공 관리 시스템
- Flask + MySQL + Vanilla JS로 구현한 풀스택 웹 애플리케이션
- 공개 API로 누구나 학습 현황 조회 가능
- JWT 인증 기반 관리자 모드
- 실제 취업 준비 과정을 체계적으로 관리

🔗 https://yeonjaegit.github.io/cursor-job-hunt/
```

### 면접 대답
```
Q: 이 프로젝트에 대해 설명해주세요
A: 제 취업 준비 과정을 관리하기 위해 직접 개발한 시스템입니다.
   Flask로 RESTful API를 설계하고, JWT 인증을 구현했으며,
   공개 읽기 전용 API로 누구나 제 학습 현황을 확인할 수 있습니다.
   실제로 매일 사용 중이며, 출석, 스케줄, 회사 지원, 
   코딩테스트를 체계적으로 관리하고 있습니다.
```

---

## 최종 체크리스트

### Backend
- [ ] Render.com 배포 완료
- [ ] MySQL 데이터베이스 연결
- [ ] 환경 변수 설정
- [ ] 첫 계정 생성 (Postman)
- [ ] API 테스트 (공개 엔드포인트)

### Frontend
- [ ] API_BASE_URL 수정 (프로덕션 URL)
- [ ] GitHub Pages 또는 Vercel 배포
- [ ] 배포된 URL 접속 테스트
- [ ] 관리자 로그인 테스트
- [ ] 읽기 전용 모드 테스트

### 포트폴리오
- [ ] 포트폴리오 웹사이트에 프로젝트 추가
- [ ] README에 배포 URL 추가
- [ ] 이력서에 프로젝트 링크 추가

---

**배포 후 모두에게 공유하세요! 🚀**
**"제 취업 준비 현황을 실시간으로 확인하실 수 있습니다"**
