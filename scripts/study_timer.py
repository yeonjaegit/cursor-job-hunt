"""
학습 시간표 알림 시스템
- 일정 시작 10분 전 알림
- 유동적으로 시간 조정 가능
- Windows 알림 사용
"""
import datetime
import time
import json
from pathlib import Path
from plyer import notification

# 프로젝트 루트 경로
ROOT_DIR = Path(__file__).parent.parent
SCHEDULE_FILE = ROOT_DIR / "scripts" / "schedule.json"

# 기본 시간표
DEFAULT_SCHEDULE = {
    "09:00": {
        "activity": "코딩테스트",
        "duration_minutes": 120,
        "goal": "Python 알고리즘 2문제",
        "flexible": True
    },
    "11:00": {
        "activity": "프로젝트 복기",
        "duration_minutes": 60,
        "goal": "면접 시나리오 준비",
        "flexible": True
    },
    "12:00": {
        "activity": "점심 & 휴식",
        "duration_minutes": 90,
        "goal": "",
        "flexible": False
    },
    "13:30": {
        "activity": "회사 분석 & 서류 지원",
        "duration_minutes": 90,
        "goal": "주 5개 이상 지원",
        "flexible": True
    },
    "15:00": {
        "activity": "기술 면접 암기 & 복습",
        "duration_minutes": 180,
        "goal": "단골 질문 30개 숙지",
        "flexible": True
    },
    "18:00": {
        "activity": "복싱 (운동)",
        "duration_minutes": 180,
        "goal": "항상 마지막!",
        "flexible": False
    }
}

def load_schedule():
    """시간표 로드 (없으면 기본값 사용)"""
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        save_schedule(DEFAULT_SCHEDULE)
        return DEFAULT_SCHEDULE

def save_schedule(schedule):
    """시간표 저장"""
    SCHEDULE_FILE.parent.mkdir(exist_ok=True)
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)

def parse_time(time_str):
    """시간 문자열을 datetime으로 변환 (HH:MM 형식)"""
    now = datetime.datetime.now()
    hour, minute = map(int, time_str.split(':'))
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)

def send_notification(title, message, duration=10):
    """Windows 알림 전송"""
    try:
        notification.notify(
            title=title,
            message=message,
            app_name='학습 타이머',
            timeout=duration
        )
    except Exception as e:
        print(f"알림 전송 실패: {e}")

def check_upcoming_activities():
    """10분 후 시작할 일정 확인"""
    schedule = load_schedule()
    now = datetime.datetime.now()
    
    for time_str, activity_info in schedule.items():
        activity_time = parse_time(time_str)
        time_diff = (activity_time - now).total_seconds()
        
        # 10분 전 알림
        if 595 <= time_diff <= 605:  # 10분 ±5초
            send_notification(
                title=f"⏰ {activity_info['activity']} 10분 전!",
                message=f"{time_str}에 시작 예정\n목표: {activity_info['goal']}"
            )
            print(f"[알림] {activity_info['activity']} 10분 전")

def check_current_activity():
    """현재 진행 중인 일정 확인"""
    schedule = load_schedule()
    now = datetime.datetime.now()
    
    for time_str, activity_info in schedule.items():
        activity_time = parse_time(time_str)
        end_time = activity_time + datetime.timedelta(minutes=activity_info['duration_minutes'])
        
        # 현재 시간이 일정 범위 내
        if activity_time <= now < end_time:
            remaining = (end_time - now).total_seconds() / 60
            
            # 종료 5분 전 알림
            if 4 <= remaining <= 6:
                if activity_info['flexible']:
                    message = f"{int(remaining)}분 후 종료 예정\n더 할래요? (시간 연장 가능)"
                else:
                    message = f"{int(remaining)}분 후 종료 예정"
                
                send_notification(
                    title=f"⏱️ {activity_info['activity']} 종료 임박",
                    message=message
                )
                print(f"[알림] {activity_info['activity']} 종료 5분 전")
            
            return activity_info
    
    return None

def extend_activity(time_str, extra_minutes):
    """일정 연장"""
    schedule = load_schedule()
    
    if time_str in schedule:
        schedule[time_str]['duration_minutes'] += extra_minutes
        save_schedule(schedule)
        print(f"✅ {schedule[time_str]['activity']} {extra_minutes}분 연장")
        
        send_notification(
            title="⏱️ 시간 연장",
            message=f"{schedule[time_str]['activity']} {extra_minutes}분 추가"
        )
    else:
        print(f"❌ {time_str} 일정을 찾을 수 없습니다.")

def show_today_schedule():
    """오늘 시간표 출력"""
    schedule = load_schedule()
    now = datetime.datetime.now()
    
    print("=" * 60)
    print(f"  📅 오늘의 학습 시간표 ({now.strftime('%Y-%m-%d %A')})")
    print("=" * 60)
    
    for time_str, activity_info in sorted(schedule.items()):
        activity_time = parse_time(time_str)
        end_time = activity_time + datetime.timedelta(minutes=activity_info['duration_minutes'])
        
        # 현재 진행 중인 일정 표시
        if activity_time <= now < end_time:
            status = "🔵 진행중"
        elif now >= end_time:
            status = "✅ 완료"
        else:
            status = "⏳ 예정"
        
        flexible_mark = "🔄" if activity_info['flexible'] else ""
        
        print(f"\n{status} {time_str} - {end_time.strftime('%H:%M')} {flexible_mark}")
        print(f"   📌 {activity_info['activity']}")
        if activity_info['goal']:
            print(f"   🎯 {activity_info['goal']}")
    
    print("\n" + "=" * 60)
    print("💡 시간 연장이 필요하면 언제든지 말씀해주세요!")
    print("=" * 60)

def main_loop():
    """메인 알림 루프"""
    print("🎓 학습 타이머 시작!")
    print("Ctrl+C로 종료")
    
    show_today_schedule()
    
    try:
        while True:
            check_upcoming_activities()
            check_current_activity()
            time.sleep(60)  # 1분마다 체크
    except KeyboardInterrupt:
        print("\n👋 학습 타이머 종료")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "show":
            show_today_schedule()
        elif command == "extend":
            if len(sys.argv) < 4:
                print("사용법: python study_timer.py extend 09:00 30")
            else:
                time_str = sys.argv[2]
                extra_minutes = int(sys.argv[3])
                extend_activity(time_str, extra_minutes)
        elif command == "reset":
            save_schedule(DEFAULT_SCHEDULE)
            print("✅ 시간표 초기화 완료")
        else:
            print("알 수 없는 명령어입니다.")
            print("사용법:")
            print("  python study_timer.py          # 알림 시작")
            print("  python study_timer.py show     # 오늘 시간표 보기")
            print("  python study_timer.py extend 09:00 30  # 09:00 일정 30분 연장")
            print("  python study_timer.py reset    # 시간표 초기화")
    else:
        main_loop()
