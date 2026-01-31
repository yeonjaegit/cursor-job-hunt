"""
학습 진행 상황 추적 및 통계 생성 스크립트
"""
import json
import datetime
from pathlib import Path
import re

# 프로젝트 루트 경로
ROOT_DIR = Path(__file__).parent.parent
DAILY_LOGS_DIR = ROOT_DIR / "daily-logs"
STATS_FILE = ROOT_DIR / "stats" / "progress.json"

def count_completed_tasks(checklist_path):
    """체크리스트에서 완료된 작업 카운트"""
    if not checklist_path.exists():
        return 0, 0
    
    content = checklist_path.read_text(encoding='utf-8')
    total = len(re.findall(r'- \[[ x]\]', content))
    completed = len(re.findall(r'- \[x\]', content))
    
    return completed, total

def extract_coding_problems(checklist_path):
    """코딩테스트 문제 수 추출"""
    if not checklist_path.exists():
        return 0
    
    content = checklist_path.read_text(encoding='utf-8')
    # "### 1. 코딩테스트" 섹션 찾기
    coding_section = re.search(r'### 1\. 코딩테스트.*?(?=###|\Z)', content, re.DOTALL)
    if not coding_section:
        return 0
    
    completed = len(re.findall(r'- \[x\]', coding_section.group(0)))
    return completed

def extract_company_applications(checklist_path):
    """회사 지원 수 추출"""
    if not checklist_path.exists():
        return 0
    
    content = checklist_path.read_text(encoding='utf-8')
    # "### 2. 회사 지원" 섹션 찾기
    company_section = re.search(r'### 2\. 회사 지원.*?(?=###|\Z)', content, re.DOTALL)
    if not company_section:
        return 0
    
    completed = len(re.findall(r'- \[x\]', company_section.group(0)))
    return completed

def calculate_stats():
    """전체 통계 계산"""
    total_coding_problems = 0
    total_company_applications = 0
    total_study_days = 0
    
    # 모든 체크리스트 파일 찾기
    checklist_files = list(DAILY_LOGS_DIR.rglob("checklist-*.md"))
    total_study_days = len(checklist_files)
    
    for checklist in checklist_files:
        problems = extract_coding_problems(checklist)
        applications = extract_company_applications(checklist)
        
        total_coding_problems += problems
        total_company_applications += applications
    
    return {
        "total_coding_problems": total_coding_problems,
        "total_company_applications": total_company_applications,
        "total_study_days": total_study_days,
        "last_updated": datetime.datetime.now().isoformat()
    }

def update_readme_stats(stats):
    """README.md의 통계 업데이트"""
    readme_path = ROOT_DIR / "README.md"
    
    if not readme_path.exists():
        print("❌ README.md를 찾을 수 없습니다.")
        return
    
    content = readme_path.read_text(encoding='utf-8')
    
    # 뱃지 업데이트
    content = re.sub(
        r'\[!\[Days\].*?\]\(\)',
        f'[![Days](https://img.shields.io/badge/학습일수-{stats["total_study_days"]}일-blue)]()',
        content
    )
    content = re.sub(
        r'\[!\[Solved\].*?\]\(\)',
        f'[![Solved](https://img.shields.io/badge/코딩테스트-{stats["total_coding_problems"]}문제-green)]()',
        content
    )
    content = re.sub(
        r'\[!\[Applied\].*?\]\(\)',
        f'[![Applied](https://img.shields.io/badge/지원-{stats["total_company_applications"]}개-orange)]()',
        content
    )
    
    # 진행 상황 바 업데이트
    coding_progress = min(stats["total_coding_problems"], 100)
    progress_bar = "█" * (coding_progress // 10) + "░" * (10 - coding_progress // 10)
    
    progress_section = f"""### 진행 상황
```
코딩테스트: {stats["total_coding_problems"]}/100 문제 {progress_bar} {coding_progress}%
회사 지원:  {stats["total_company_applications"]}개 (서류 합격 0개)
학습 일수:  {stats["total_study_days"]}일 연속 ⭐
```"""
    
    content = re.sub(
        r'### 진행 상황\n```[\s\S]*?```',
        progress_section,
        content
    )
    
    # Last Updated 업데이트
    today = datetime.date.today().strftime("%Y-%m-%d")
    content = re.sub(
        r'\*\*Last Updated\*\*:.*',
        f'**Last Updated**: {today}',
        content
    )
    
    readme_path.write_text(content, encoding='utf-8')
    print(f"✅ README.md 통계 업데이트 완료")

def save_stats(stats):
    """통계를 JSON 파일로 저장"""
    STATS_FILE.parent.mkdir(exist_ok=True)
    
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 통계 파일 저장 완료: {STATS_FILE}")

def main():
    """메인 함수"""
    print("📊 학습 진행 상황을 분석하고 있습니다...\n")
    
    stats = calculate_stats()
    
    print("📈 현재 통계:")
    print(f"   - 학습 일수: {stats['total_study_days']}일")
    print(f"   - 코딩테스트: {stats['total_coding_problems']}문제")
    print(f"   - 회사 지원: {stats['total_company_applications']}개\n")
    
    save_stats(stats)
    update_readme_stats(stats)
    
    print("\n🎉 완료!")

if __name__ == "__main__":
    main()
