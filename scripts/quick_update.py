"""
GitHub 빠른 업데이트 스크립트
하루 끝나고 학습 기록을 커밋하고 푸시합니다.
"""
import subprocess
import sys
import datetime
from pathlib import Path

def run_command(command, cwd=None):
    """명령어 실행"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """메인 함수"""
    # 프로젝트 루트로 이동
    root_dir = Path(__file__).parent.parent
    
    print("📝 오늘 학습 기록을 GitHub에 업데이트합니다...\n")
    
    # 날짜 정보
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    weekday = ["월", "화", "수", "목", "금", "토", "일"][today.weekday()]
    
    # Git 상태 확인
    success, stdout, stderr = run_command("git status --short", cwd=root_dir)
    if not success:
        print("❌ Git 저장소가 아니거나 오류가 발생했습니다.")
        print(f"   오류: {stderr}")
        return
    
    if not stdout.strip():
        print("✅ 변경사항이 없습니다.")
        return
    
    print("📋 변경된 파일:")
    print(stdout)
    
    # 커밋 메시지 생성
    if len(sys.argv) > 1:
        commit_message = sys.argv[1]
    else:
        commit_message = f"docs: {date_str} ({weekday}) 학습 기록"
    
    print(f"\n💬 커밋 메시지: {commit_message}\n")
    
    # Git add
    print("1️⃣ 파일 스테이징 중...")
    success, _, stderr = run_command("git add .", cwd=root_dir)
    if not success:
        print(f"❌ git add 실패: {stderr}")
        return
    print("   ✅ 완료\n")
    
    # Git commit
    print("2️⃣ 커밋 생성 중...")
    success, _, stderr = run_command(f'git commit -m "{commit_message}"', cwd=root_dir)
    if not success:
        if "nothing to commit" in stderr:
            print("   ℹ️ 커밋할 변경사항이 없습니다.")
        else:
            print(f"❌ git commit 실패: {stderr}")
            return
    else:
        print("   ✅ 완료\n")
    
    # Git push
    print("3️⃣ GitHub에 푸시 중...")
    success, stdout, stderr = run_command("git push", cwd=root_dir)
    if not success:
        print(f"❌ git push 실패: {stderr}")
        print("\n💡 원격 저장소가 설정되지 않았을 수 있습니다.")
        print("   다음 명령어로 원격 저장소를 추가하세요:")
        print(f"   git remote add origin https://github.com/yeonjaegit/cursor-job-hunt.git")
        return
    print("   ✅ 완료\n")
    
    print("🎉 GitHub 업데이트 완료!")
    print(f"   → https://github.com/yeonjaegit/cursor-job-hunt")

if __name__ == "__main__":
    main()
