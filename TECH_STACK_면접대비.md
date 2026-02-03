# cursor-job-hunt 기술 스택 면접 대비

> 1·2·3차 프로젝트 코드 기준 분석. "쓸 줄 모르는" 기술이 포함되어 있는지 확인.

## cursor-job-hunt 사용 기술

| 분류 | 기술 | 1차(커피) | 2차(Bros) | 3차(404) | 비고 |
|------|------|:---:|:---:|:---:|------|
| Backend | Flask | ✓ | ✓ | ✓ | 동일 |
| Backend | Flask-SQLAlchemy | ✓ | ✓ | ✓ | 동일 |
| Backend | Flask-CORS | ✓ | ✓ | ✓ | 동일 |
| Backend | Flask-JWT-Extended | ✓ | ✓ | ✓ | 404, Bros에서 동일 사용 |
| Backend | Flask-Bcrypt | | ✓ | | Bros auth에서 비밀번호 해시 사용. Bcrypt는 업계 표준 |
| Backend | PyMySQL | ✓ | ✓ | ✓ | MySQL 연결용 |
| Frontend | React | ✓ | ✓ | ✓ | 동일 |
| Frontend | Vite | ✓ | ✓ | ✓ | 동일 |
| Frontend | Axios | ✓ | ✓ | ✓ | 동일 |
| DB | MySQL | ✓ | ✓ | ✓ | 동일 |
| Auth | JWT (Access+Refresh) | ✓ | ✓ | ✓ | 404에도 refresh 설정 있음 |
| Auth | Bcrypt | ✓ | ✓ | | Spring Security/JWT에서 비밀번호 해시 |

## 결론: **모두 기존 프로젝트에서 사용한 기술**

- **Flask-Bcrypt**: Bros/404에서 비밀번호 저장 시 해시 사용. Flask-Bcrypt는 `bcrypt.generate_password_hash()`, `check_password_hash()` 두 함수만 쓰면 됨. 5분이면 설명 가능.
- **Context API vs Redux**: cursor-job-hunt는 Redux 대신 React Context(AuthContext) 사용. 더 단순함. Redux 쓴 1·3차보다 구현이 쉽다는 걸 설명 가능.
- **Hash 라우팅**: `window.location.hash`로 탭 유지. React Router 없이 구현. SPA 기본 개념으로 충분히 설명 가능.

## 면접 예상 Q&A

**Q: JWT Refresh Token 구현 경험?**  
→ 404-back, cursor-job-hunt에서 `@jwt_required(refresh=True)` 로 구현. Access 만료 시 Refresh로 재발급.

**Q: Flask Blueprint 구조?**  
→ Bros 18개 Blueprint, cursor-job-hunt도 auth, attendance, schedule 등 Blueprint로 분리.

**Q: SQLAlchemy ORM 사용?**  
→ Bros, 404, cursor-job-hunt 모두 동일. `db.Model`, `query.filter_by()` 등.

**Q: React 상태 관리?**  
→ 1·3차: Redux. cursor-job-hunt: Context API (로그인 상태만 있어서 단순 구조 선택).
