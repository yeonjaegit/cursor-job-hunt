import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { attendanceAPI } from '../api';

const Attendance = () => {
  const { isAdmin } = useAuth();
  const [attendances, setAttendances] = useState([]);
  const [stats, setStats] = useState({ total_days: 0, last_attendance: null });
  const [loading, setLoading] = useState(true);
  const [checkingIn, setCheckingIn] = useState(false);
  const [error, setError] = useState(null);
  const [viewDate, setViewDate] = useState(() => new Date());

  useEffect(() => {
    loadData();
  }, [isAdmin]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const attendanceRes = isAdmin 
        ? await attendanceAPI.getAll() 
        : await attendanceAPI.getPublicAll();
      
      const attendancesList = attendanceRes.data.attendances || [];
      setAttendances(attendancesList);
      
      setStats({
        total_days: attendancesList.length,
        last_attendance: attendancesList[0]?.date || null
      });
    } catch (error) {
      console.error('Failed to load attendance:', error);
      setError('데이터를 불러올 수 없습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleCheckIn = async () => {
    if (!isAdmin) {
      alert('관리자만 출석 체크가 가능합니다.');
      return;
    }

    setCheckingIn(true);
    try {
      await attendanceAPI.checkIn();
      alert('출석 체크 완료');
      loadData();
    } catch (error) {
      const status = error.response?.status;
      const msg = error.response?.data?.error;
      const fallback = (status === 401 || status === 422) 
        ? '토큰이 만료되었습니다. 다시 로그인해주세요.' 
        : '출석 체크에 실패했습니다.';
      alert(msg || fallback);
    } finally {
      setCheckingIn(false);
    }
  };

  const renderCalendar = () => {
    const attendanceSet = new Set(
      (attendances || []).map((a) => new Date(a.date).toDateString())
    );

    const today = new Date();
    const currentYear = viewDate.getFullYear();
    const currentMonth = viewDate.getMonth();

    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    const weeks = [];
    let week = new Array(7).fill(null);

    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentYear, currentMonth, day);
      const dow = date.getDay();
      if (dow === 0 && day > 1) {
        weeks.push([...week]);
        week = new Array(7).fill(null);
      }
      week[dow] = {
        day,
        isToday: date.toDateString() === today.toDateString(),
        hasAttendance: attendanceSet.has(date.toDateString()),
      };
    }
    weeks.push(week);

    return (
      <div className="attendance-calendar">
        <div className="calendar-header">
          <button
            type="button"
            className="calendar-nav"
            onClick={() => setViewDate(new Date(currentYear, currentMonth - 1))}
          >
            이전
          </button>
          <h3>{currentYear}년 {currentMonth + 1}월</h3>
          <button
            type="button"
            className="calendar-nav"
            onClick={() => setViewDate(new Date(currentYear, currentMonth + 1))}
          >
            다음
          </button>
        </div>
        <div className="calendar-weekdays">
          {['일', '월', '화', '수', '목', '금', '토'].map((d, i) => (
            <div key={i} className="calendar-weekday">{d}</div>
          ))}
        </div>
        <div className="calendar-grid">
          {weeks.flat().map((dayData, i) => (
            <div
              key={i}
              className={`calendar-day ${dayData?.isToday ? 'today' : ''} ${
                dayData?.hasAttendance ? 'has-attendance' : ''
              }`}
            >
              {dayData?.day ?? ''}
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (loading) {
    return <div className="loading">로딩 중...</div>;
  }

  return (
    <div className="section attendance-section">
      <div className="section-header">
        <h2 className="section-title">출석 캘린더</h2>
        {isAdmin && (
          <button 
            className="btn btn-primary" 
            onClick={handleCheckIn}
            disabled={checkingIn}
          >
            {checkingIn ? '처리 중...' : '오늘 출석하기'}
          </button>
        )}
      </div>

      {stats && (
        <div className="stats-row">
          <div className="stat-item">
            <span className="stat-label">총 출석일</span>
            <span className="stat-value">{stats.total_days}일</span>
          </div>
          {stats.last_attendance && (
            <div className="stat-item">
              <span className="stat-label">최근 출석</span>
              <span className="stat-value">
                {new Date(stats.last_attendance).toLocaleDateString('ko-KR')}
              </span>
            </div>
          )}
        </div>
      )}

      <div className="calendar-wrapper attendance-calendar-full">
        {renderCalendar()}
      </div>
    </div>
  );
};

export default Attendance;
