import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { dashboardAPI } from '../api';

const Dashboard = ({ onNavigate }) => {
  const { isAdmin, loading: authLoading } = useAuth();
  const [stats, setStats] = useState({
    attendance: { total_days: 0, last_attendance: null },
    companies: { total: 0, by_status: { applied: 0, docs_passed: 0, interviewed: 0, accepted: 0, rejected: 0 } },
    coding: { total: 0, solved: 0, unsolved: 0 },
    schedules: { active: 0, inactive: 0 }
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const loadStatsRef = useRef(null);

  const loadStats = async () => {
    try {
      setLoading(true);
      setError(null);

      let response;
      try {
        if (isAdmin) {
          response = await dashboardAPI.getStats();
        } else {
          response = await dashboardAPI.getPublicStats();
        }
      } catch (e) {
        response = await dashboardAPI.getPublicStats();
      }

      if (!response?.data) throw new Error('응답 데이터 없음');

      setStats({
        attendance: response.data.attendance ?? { total_days: 0, last_attendance: null },
        companies: response.data.companies ?? { total: 0, by_status: { applied: 0, docs_passed: 0, interviewed: 0, accepted: 0, rejected: 0 } },
        coding: response.data.coding ?? { total: 0, solved: 0, unsolved: 0 },
        schedules: response.data.schedules ?? { active: 0, inactive: 0 }
      });
    } catch (err) {
      console.error('Failed to load stats:', err);
      setError('데이터를 불러올 수 없습니다. Flask 서버가 실행 중인지 확인해주세요.');
    } finally {
      setLoading(false);
    }
  };

  loadStatsRef.current = loadStats;

  useEffect(() => {
    loadStats();
  }, [isAdmin, authLoading]);

  useEffect(() => {
    const onVisibility = () => {
      if (document.visibilityState === 'visible' && loadStatsRef.current) {
        loadStatsRef.current();
      }
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => document.removeEventListener('visibilitychange', onVisibility);
  }, []);

  if (loading) {
    return <div className="loading">로딩 중...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>{error}</p>
        <button onClick={loadStats}>다시 시도</button>
      </div>
    );
  }

  return (
    <div className="section dashboard-section">
      <h2 className="section-title">대시보드</h2>
      
      <div className="stats-grid">
        <div className={`stat-card stat-1 ${onNavigate ? 'stat-card--clickable' : ''}`} onClick={onNavigate ? () => onNavigate('attendance') : undefined}>
          <div className="stat-content">
            <h3>총 출석일</h3>
            <p className="stat-number">{stats.attendance.total_days}일</p>
            {stats.attendance.last_attendance && (
              <p className="stat-detail">최근: {new Date(stats.attendance.last_attendance).toLocaleDateString('ko-KR')}</p>
            )}
            {onNavigate && <span className="stat-link">보기 →</span>}
          </div>
        </div>

        <div className={`stat-card stat-2 ${onNavigate ? 'stat-card--clickable' : ''}`} onClick={onNavigate ? () => onNavigate('companies') : undefined}>
          <div className="stat-content">
            <h3>지원한 회사</h3>
            <p className="stat-number">{stats.companies.total}개</p>
            <div className="stat-breakdown">
              <span>합격 {stats.companies.by_status.accepted || 0}</span>
              <span>진행중 {stats.companies.by_status.applied + (stats.companies.by_status.docs_passed || 0) + (stats.companies.by_status.interviewed || 0)}</span>
            </div>
            {onNavigate && <span className="stat-link">보기 →</span>}
          </div>
        </div>

        <div className={`stat-card stat-3 ${onNavigate ? 'stat-card--clickable' : ''}`} onClick={onNavigate ? () => onNavigate('coding') : undefined}>
          <div className="stat-content">
            <h3>코딩 테스트</h3>
            <p className="stat-number">{stats.coding.total}문제</p>
            <div className="stat-breakdown">
              <span>해결 {stats.coding.solved}</span>
              <span>{stats.coding.total > 0 ? Math.round((stats.coding.solved / stats.coding.total) * 100) : 0}%</span>
            </div>
            {onNavigate && <span className="stat-link">보기 →</span>}
          </div>
        </div>

        <div className={`stat-card stat-4 ${onNavigate ? 'stat-card--clickable' : ''}`} onClick={onNavigate ? () => onNavigate('schedule') : undefined}>
          <div className="stat-content">
            <h3>주간 일정</h3>
            <p className="stat-number">{stats.schedules.active}개</p>
            <div className="stat-breakdown">
              <span>활성 {stats.schedules.active}</span>
              <span>휴무 {stats.schedules.inactive}</span>
            </div>
            {onNavigate && <span className="stat-link">보기 →</span>}
          </div>
        </div>
      </div>

      {!isAdmin && (
        <div className="public-notice">
          <p>읽기 전용입니다. 데이터 수정을 원하면 로그인하세요.</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
