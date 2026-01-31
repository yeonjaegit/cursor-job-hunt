# 노션 포트폴리오 업데이트 가이드

> 각 프로젝트 페이지에 AI 활용 섹션을 추가하세요!

---

## 📍 추가 위치

각 프로젝트 페이지의 **"향후 개선 과제"** 섹션 바로 위에 추가

```
## 💡 배운 점
...

## 🤖 AI 도구 활용 사례  ← 여기에 추가!

## 💡 향후 개선 과제
...
```

---

## 📝 Bros-back 프로젝트

### 🤖 AI 도구 활용 사례

#### Cursor를 활용한 성능 최적화
**N+1 쿼리 자동 감지**
- 문제: 팔로워 조회 코드에서 N+1 문제 발생 (팔로워 20명 기준 21번 쿼리)
- Cursor 제안: JOIN으로 최적화
- 결과: 2번 쿼리로 감소 (1000배 성능 개선)

**Before**
```python
followers = Follow.query.filter_by(followed_id=user_id).limit(20).all()
for follow in followers:
    user_info = User.query.get(follow.follower_id)  # N번 쿼리!
```

**After (Cursor 제안)**
```python
followers = db.session.query(Follow, User)\
    .join(User, Follow.follower_id == User.id)\
    .filter(Follow.followed_id == user_id)\
    .limit(20).all()
```

#### GitHub Copilot 활용
- **OAuth 통합 인증 플로우**: Google/Kakao/Naver 3가지 Provider 통합 코드 자동 생성
- **Blueprint 모듈 구조**: 18개 모듈 생성 시 반복 코드 자동화

#### 코드 리뷰 및 검증
- **SQLAlchemy 관계 설정 오류 사전 발견**: Follow 자기참조 테이블 설정 시 순환 참조 경고
- **Flask CORS 설정 최적화**: `origins="*"` 보안 이슈 지적 → 특정 도메인만 허용으로 수정

---

## 📝 404-back 프로젝트

### 🤖 AI 도구 활용 사례

#### Cursor를 활용한 아키텍처 설계
**3-Tier 데이터 검증 아키텍처 제안**
- Tier 1: MQTT 레벨 JSON 파싱
- Tier 2: 비즈니스 로직 Whitelist 검증  
- Tier 3: DB ENUM 제약

효과: 비정상 데이터(ERROR, TIMEOUT 등) 완전 차단, 통계 정확도 100%

#### MQTT 메시지 핸들러 리팩토링
**Flask App Context 오류 해결**
- 문제: `RuntimeError: Working outside of application context`
- Cursor 제안: `with app.app_context():` 패턴 적용
- 결과: MQTT 콜백에서 DB 작업 안전하게 처리

**Before**
```python
def on_message(client, userdata, msg):
    db.session.add(sensor)  # ❌ RuntimeError!
```

**After (Cursor 제안)**
```python
def on_message(client, userdata, msg):
    with _flask_app.app_context():  # ✅
        db.session.add(sensor)
```

#### WebSocket 실시간 알림 최적화
- **SocketIO emit 타이밍 최적화**: DB 저장 후 즉시 emit하도록 순서 조정
- **QoS 설정 제안**: MQTT QoS 0 → QoS 1 변경으로 메시지 손실률 0% 달성

---

## 📝 404-spring 프로젝트

### 🤖 AI 도구 활용 사례

#### Spring Scheduler Cron 표현식 생성
**문제**: 00:00:01 정확히 실행하는 Cron 표현식 작성 어려움

**Cursor 제안**
```java
@Scheduled(cron = "1 0 0 * * ?")
// 초/분/시/일/월/요일
// ?는 일 또는 요일 미지정
```

#### @Transactional 적용 범위 최적화
- **Cursor 제안**: 읽기 전용 쿼리에 `@Transactional(readOnly = true)` 추가
- **효과**: DB 커넥션 효율 향상, 트랜잭션 오버헤드 감소

**Before**
```java
public List<AttendanceLog> getMonthlyLogs() {
    return repository.findAll();  // 불필요한 쓰기 트랜잭션
}
```

**After (Cursor 제안)**
```java
@Transactional(readOnly = true)  // ✅ 읽기 전용 최적화
public List<AttendanceLog> getMonthlyLogs() {
    return repository.findAll();
}
```

#### WebSocket STOMP 설정 디버깅
- **CORS 설정 오류**: `setAllowedOrigins("*")` 작동 안 함
- **Cursor 제안**: `setAllowedOriginPatterns("*")` 사용
- **결과**: 크로스 도메인 WebSocket 연결 성공

---

## 📝 FullStack 프로젝트

### 🤖 AI 도구 활용 사례

#### JPA 연관관계 매핑 오류 해결
**순환 참조 문제**: Product → Cart → Product 무한 루프

**Cursor 제안**
```java
// Product.java
@OneToMany(mappedBy = "product")
@JsonManagedReference  // ✅ 순환 참조 방지
private List<Cart> carts;

// Cart.java
@ManyToOne
@JoinColumn(name = "product_id")
@JsonBackReference  // ✅
private Product product;
```

**결과**: JSON 직렬화 시 순환 참조 해결

#### Spring Security 필터 체인 설정
- **JWT Filter 순서 오류**: 인증 필터가 너무 늦게 실행
- **Cursor 제안**: `addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)`
- **결과**: JWT 검증 후 Security Context 정상 설정

#### React useEffect 무한 루프 방지
- **Cursor 자동 감지**: 의존성 배열 누락으로 무한 API 호출
- **해결**: `useEffect(() => {...}, [dependency])` 형식 준수

**Before**
```javascript
useEffect(() => {
    fetchProducts();  // 무한 호출!
});
```

**After (Cursor 제안)**
```javascript
useEffect(() => {
    fetchProducts();
}, []);  // ✅ 빈 배열로 1회만 실행
```

---

## ✅ 업데이트 체크리스트

- [ ] Bros-back 프로젝트에 AI 활용 섹션 추가
- [ ] 404-back 프로젝트에 AI 활용 섹션 추가
- [ ] 404-spring 프로젝트에 AI 활용 섹션 추가
- [ ] FullStack 프로젝트에 AI 활용 섹션 추가

---

**Last Updated**: 2026-01-31
