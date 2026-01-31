"""
하루 학습 시작 스크립트
Cursor에서 "오늘 학습 시작!" 하면 실행되는 자동화 스크립트
"""
import subprocess
import sys
import os
from pathlib import Path
from daily_checklist import create_checklist, update_start_here
import datetime

ROOT_DIR = Path(__file__).parent.parent

def start_study_timer():
    """알림 시스템 백그라운드 실행"""
    print("🔔 알림 시스템 시작 중...")
    
    try:
        # Windows에서 백그라운드 실행
        if sys.platform == 'win32':
            subprocess.Popen(
                [sys.executable, str(ROOT_DIR / "scripts" / "study_timer.py")],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            subprocess.Popen(
                [sys.executable, str(ROOT_DIR / "scripts" / "study_timer.py")],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        print("✅ 알림 시스템 실행 완료!")
    except Exception as e:
        print(f"⚠️ 알림 시스템 실행 실패: {e}")
        print("💡 수동으로 실행하세요: python scripts/study_timer.py")

def create_daily_checklist():
    """오늘 체크리스트 생성"""
    print("\n📋 오늘의 체크리스트 생성 중...")
    
    today = datetime.date.today()
    checklist_path = create_checklist(today)
    update_start_here(today)
    
    print(f"✅ 체크리스트 생성 완료: {checklist_path}")
    return checklist_path

def show_today_schedule():
    """오늘 할 일 요약"""
    today = datetime.date.today()
    weekday = ['월', '화', '수', '목', '금', '토', '일'][today.weekday()]
    weekday_num = today.weekday()  # 0=월, 1=화, 2=수, 3=목, 4=금, 5=토, 6=일
    
    print("\n" + "=" * 60)
    print(f"  🎯 {today.strftime('%Y년 %m월 %d일')} ({weekday}요일)")
    print("=" * 60)
    
    # 휴무일 체크 (수/토/일)
    if weekday_num in [2, 5, 6]:  # 수요일(2), 토요일(5), 일요일(6)
        if weekday_num == 2:
            print("\n💝 오늘은 휴무일! (여자친구 만나는 날)")
        else:
            print("\n💼 오늘은 휴무일! (알바)")
        print("\n잘 쉬고, 내일 다시 화이팅!")
        print("=" * 60 + "\n")
        return
    
    print("학습 시작!")
    print("=" * 60)
    
    # 2월 2일 특별 일정 (포트폴리오 수정일)
    if today.month == 2 and today.day == 2:
        print("\n⭐ 오늘은 첫날! 포트폴리오 수정 집중:")
        print("  📝 노션 포트폴리오 수정 (AI 활용 섹션 4개 추가)")
        print("  🌐 포트폴리오 웹사이트 확인")
        print("  💼 시간 되면 회사 지원 시작")
        print("\n⏰ 시간은 자유롭게 조정 OK!")
        print("💡 오늘의 핵심: 노션에 AI 섹션 완성!")
    else:
        # 정규 학습 일정 (월/화/목/금)
        print("\n📅 오늘의 일정:")
        print("  09:00-11:00  코딩테스트 (최대 2문제)")
        print("  11:00-12:00  프로젝트 복기")
        print("  12:00-13:30  점심 휴식")
        print("  13:30-15:00  회사 지원")
        print("  15:00-18:00  기술 면접 암기 & 복습")
        print("  18:00-21:00  복싱 (운동) ← 항상 마지막!")
    
    print("\n" + "=" * 60)
    print("💪 오늘도 화이팅!")
    print("=" * 60 + "\n")

def main():
    """메인 실행"""
    print("\n" + "🚀" * 20)
    print("  오늘 학습 시작!")
    print("🚀" * 20 + "\n")
    
    # 1. 알림 시스템 시작
    start_study_timer()
    
    # 2. 오늘 체크리스트 생성
    create_daily_checklist()
    
    # 3. 오늘 할 일 요약
    show_today_schedule()
    
    print("\n💡 다음 단계:")
    print("  1. 프로그래머스에서 코딩테스트 시작")
    print("  2. 막히면 Cursor에게 질문하세요!")
    print("  3. 11시에 프로젝트 복기 시작")
    print("\n✨ 좋은 하루 되세요!\n")

if __name__ == "__main__":
    main()
