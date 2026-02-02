# Private 학습 자료

> 이 폴더는 .gitignore에 포함되어 GitHub에 업로드되지 않습니다.
> 면접 예상 질문, 회사별 전략 등 공개하면 안 되는 내용을 저장하세요.

---

## 📁 폴더 구조 (권장)

```
private/
├── interview-questions/
│   ├── backend-30-questions.md    # 백엔드 단골 질문 30개
│   ├── project-scenarios.md       # 프로젝트별 예상 질문
│   └── answers/                   # 답변 작성
├── company-analysis/
│   ├── target-companies.md        # 지원할 회사 리스트
│   ├── application-status.md      # 지원 현황 추적
│   └── companies/                 # 회사별 분석
└── study-notes/
    └── weak-points.md             # 취약 부분 정리
```

---

## 💡 사용 방법

### 면접 질문 작성
```markdown
# backend-30-questions.md

## 1. HTTP와 HTTPS의 차이는?

**답변:**
HTTP는 평문 통신이고, HTTPS는 SSL/TLS로 암호화합니다.
...

**꼬리 질문:**
- SSL 핸드셰이크 과정은?
- 대칭키와 비대칭키 차이는?
```

### 회사 분석
```markdown
# companies/카카오.md

## 기본 정보
- 기술 스택: Java Spring Boot, Kafka
- 주요 서비스: 카카오톡, 카카오페이

## 지원 동기
Bros 프로젝트에서 카카오페이 API 연동 경험...

## 예상 질문
1. 카카오페이 결제 플로우 설명해보세요
2. Spring Boot vs Flask 차이는?
```

---

**⚠️ 주의**: 이 폴더는 Git에 올라가지 않으므로 백업 필수!
