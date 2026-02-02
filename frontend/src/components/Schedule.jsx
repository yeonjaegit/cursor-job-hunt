import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { scheduleAPI } from '../api';

const DAY_LABELS = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'];

const toLocalDateString = (date) => {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
};

const getWeekMonday = (d) => {
  const date = d instanceof Date ? new Date(d.getTime()) : new Date(d + 'T12:00:00');
  const day = date.getDay();
  const daysToMonday = day === 0 ? 6 : day - 1;
  const monday = new Date(date);
  monday.setDate(date.getDate() - daysToMonday);
  return toLocalDateString(monday);
};

const formatWeekRange = (weekStart) => {
  const m = new Date(weekStart + 'T12:00:00');
  const sun = new Date(m);
  sun.setDate(sun.getDate() + 6);
  return `${m.getMonth() + 1}/${m.getDate()} ~ ${sun.getMonth() + 1}/${sun.getDate()}`;
};

const Schedule = () => {
  const { isAdmin } = useAuth();
  const [schedules, setSchedules] = useState([]);
  const [checks, setChecks] = useState({});
  const [weekStart, setWeekStart] = useState(getWeekMonday(new Date()));
  const getTodayDayOfWeek = () => {
    const jsDay = new Date().getDay();
    return (jsDay + 6) % 7;
  };
  const todayDayNum = getTodayDayOfWeek();
  const thisWeekStart = getWeekMonday(new Date());
  const [selectedDay, setSelectedDay] = useState(String(todayDayNum));
  const selectedDayNum = selectedDay === '' ? null : Number(selectedDay);
  const [editingSchedule, setEditingSchedule] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [addingDay, setAddingDay] = useState(null);
  const [addForm, setAddForm] = useState({
    start_time: '09:00',
    end_time: '10:00',
    activity: '',
    is_active: true,
    notes: '',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSchedules();
  }, [selectedDay, isAdmin, weekStart]);

  useEffect(() => {
    if (isAdmin && selectedDay !== '' && Number(selectedDay) === todayDayNum && weekStart === thisWeekStart) {
      loadChecks();
    }
  }, [isAdmin, selectedDay, weekStart]);

  const loadSchedules = async () => {
    try {
      const response = isAdmin
        ? await scheduleAPI.getAll(selectedDayNum, weekStart)
        : await scheduleAPI.getPublicAll(selectedDayNum, weekStart);
      setSchedules(response.data.schedules || []);
    } catch (error) {
      console.error('Failed to load schedules:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadChecks = async () => {
    if (!isAdmin) return;
    try {
      const today = new Date().toISOString().split('T')[0];
      const res = await scheduleAPI.getChecks(today);
      setChecks(res.data.checks || {});
    } catch {
      setChecks({});
    }
  };

  const handleEdit = (schedule) => {
    if (!isAdmin) return;
    setEditingSchedule(schedule);
  };

  const handleSave = async () => {
    if (!isAdmin) return;
    try {
      await scheduleAPI.update(editingSchedule.id, {
        start_time: editingSchedule.start_time,
        end_time: editingSchedule.end_time,
        activity: editingSchedule.activity,
        is_active: editingSchedule.is_active,
        notes: editingSchedule.notes,
      });
      setEditingSchedule(null);
      loadSchedules();
    } catch (error) {
      alert(error.response?.data?.error || '수정에 실패했습니다.');
    }
  };

  const handleDelete = async () => {
    if (!isAdmin || !editingSchedule) return;
    if (!confirm('이 일정을 삭제하시겠습니까?')) return;
    try {
      await scheduleAPI.delete(editingSchedule.id);
      setEditingSchedule(null);
      loadSchedules();
    } catch (error) {
      alert(error.response?.data?.error || '삭제에 실패했습니다.');
    }
  };

  const handleToggle = async (scheduleId) => {
    if (!isAdmin) return;
    try {
      await scheduleAPI.toggleActive(scheduleId);
      loadSchedules();
    } catch (error) {
      alert('상태 변경에 실패했습니다.');
    }
  };

  const handleSwap = async (scheduleId, direction) => {
    if (!isAdmin) return;
    try {
      await scheduleAPI.swap(scheduleId, direction);
      loadSchedules();
    } catch (error) {
      alert(error.response?.data?.error || '순서 변경에 실패했습니다.');
    }
  };

  const handleCheck = async (scheduleId, checked) => {
    if (!isAdmin) return;
    try {
      const today = new Date().toISOString().split('T')[0];
      await scheduleAPI.toggleCheck(scheduleId, checked, today);
      setChecks((prev) => ({ ...prev, [scheduleId]: checked }));
    } catch (error) {
      alert('체크 저장에 실패했습니다.');
    }
  };

  const handleSetDayOff = async (dayNum) => {
    if (!isAdmin) return;
    if (!confirm('이 요일 전체를 휴무로 설정하시겠습니까?')) return;
    try {
      await scheduleAPI.setDayOff(dayNum, weekStart);
      loadSchedules();
    } catch (error) {
      alert(error.response?.data?.error || '설정에 실패했습니다.');
    }
  };

  const handleResetDay = async (dayNum) => {
    if (!isAdmin) return;
    if (!confirm('이 요일을 기본 일정으로 복원하시겠습니까?')) return;
    try {
      await scheduleAPI.resetDay(dayNum, weekStart);
      loadSchedules();
    } catch (error) {
      alert(error.response?.data?.error || '복원에 실패했습니다.');
    }
  };

  const handleOpenAdd = (dayNum) => {
    setAddingDay(dayNum);
    setAddForm({
      start_time: '09:00',
      end_time: '10:00',
      activity: '',
      is_active: true,
      notes: '',
    });
    setShowAddModal(true);
  };

  const handleAddSubmit = async (e) => {
    e.preventDefault();
    if (!isAdmin || addingDay == null || !addForm.activity.trim()) {
      alert('활동을 입력해주세요.');
      return;
    }
    try {
      await scheduleAPI.create({
        week_start: weekStart,
        day_of_week: addingDay,
        start_time: addForm.start_time,
        end_time: addForm.end_time,
        activity: addForm.activity.trim(),
        is_active: addForm.is_active,
        notes: addForm.notes || null,
      });
      setShowAddModal(false);
      setAddingDay(null);
      loadSchedules();
    } catch (error) {
      alert(error.response?.data?.error || '추가에 실패했습니다.');
    }
  };

  const isDayOff = (daySchedules) =>
    daySchedules.length === 1 && daySchedules[0].activity === '휴무' && !daySchedules[0].is_active;

  const groupByDay = () => {
    const grouped = {};
    DAY_LABELS.forEach((_, i) => {
      grouped[i] = schedules.filter((s) => Number(s.day_of_week) === i);
    });
    return grouped;
  };

  if (loading) return <div className="loading">로딩 중...</div>;

  const groupedSchedules =
    selectedDay !== '' && selectedDay != null
      ? { [selectedDay]: schedules.filter((s) => Number(s.day_of_week) === Number(selectedDay)) }
      : groupByDay();

  const showChecklist = isAdmin && weekStart === thisWeekStart;

  const goPrevWeek = () => {
    const d = new Date(weekStart + 'T12:00:00');
    d.setDate(d.getDate() - 7);
    setWeekStart(getWeekMonday(d));
  };

  const goNextWeek = () => {
    const d = new Date(weekStart + 'T12:00:00');
    d.setDate(d.getDate() + 7);
    setWeekStart(getWeekMonday(d));
  };

  const goThisWeek = () => setWeekStart(thisWeekStart);

  return (
    <div className="section schedule-section">
      <div className="section-header">
        <h2 className="section-title">일정 시간표</h2>
        <div className="schedule-header-controls">
          <div className="week-nav">
            <button type="button" className="schedule-nav-btn" onClick={goPrevWeek}>◀ 이전 주</button>
            <span className="week-range">{formatWeekRange(weekStart)}</span>
            <button type="button" className="schedule-nav-btn" onClick={goNextWeek}>다음 주 ▶</button>
            {weekStart !== thisWeekStart && (
              <button type="button" className="schedule-nav-btn btn-this-week" onClick={goThisWeek}>이번 주</button>
            )}
          </div>
          <select
            className="day-filter"
            value={selectedDay}
            onChange={(e) => setSelectedDay(e.target.value)}
          >
          <option value="">전체 보기</option>
          {DAY_LABELS.map((label, idx) => (
            <option key={label} value={idx}>
              {idx === todayDayNum ? `오늘 (${label})` : label}
            </option>
          ))}
          </select>
        </div>
      </div>

      <div className="schedule-timeline-container">
        {Object.entries(groupedSchedules).map(([dayKey, daySchedules]) => {
          const dayNum = Number(dayKey);
          const dayLabel = DAY_LABELS[dayNum] || '';
          if (daySchedules.length === 0 && selectedDay !== '') return null;

          const off = isDayOff(daySchedules);
          const isToday = dayNum === todayDayNum;

          return (
            <div key={dayLabel} className="schedule-day-card">
              <div className="schedule-day-header">
                <h3 className="schedule-day-title">{dayLabel}</h3>
                {isAdmin && (
                  <div className="schedule-day-buttons">
                    <button
                      type="button"
                      className="btn-schedule-sm btn-schedule-add"
                      onClick={() => handleOpenAdd(dayNum)}
                    >
                      + 일정 추가
                    </button>
                    {off ? (
                      <button
                        type="button"
                        className="btn-schedule-sm"
                        onClick={() => handleResetDay(dayNum)}
                      >
                        기본 복원
                      </button>
                    ) : (
                      <button
                        type="button"
                        className="btn-schedule-sm btn-schedule-outline"
                        onClick={() => handleSetDayOff(dayNum)}
                      >
                        전체 휴무
                      </button>
                    )}
                  </div>
                )}
              </div>

              {daySchedules.length === 0 ? (
                <p className="schedule-empty">일정이 없습니다.</p>
              ) : (
                <div className="schedule-timeline">
                  {daySchedules.map((schedule, idx) => (
                    <div
                      key={schedule.id}
                      className={`schedule-timeline-item ${!schedule.is_active ? 'schedule-inactive' : ''}`}
                    >
                      <div className="schedule-timeline-time">
                        <span className="time-range">
                          {schedule.start_time} – {schedule.end_time}
                        </span>
                      </div>
                      <div className="schedule-timeline-dot" />
                      <div className="schedule-timeline-content">
                        <div className="schedule-timeline-main">
                          {showChecklist && isToday && schedule.activity !== '휴무' ? (
                            <label className="schedule-check-label">
                              <input
                                type="checkbox"
                                checked={!!checks[schedule.id]}
                                onChange={(e) => handleCheck(schedule.id, e.target.checked)}
                                className="schedule-check-input"
                              />
                              <span className="schedule-activity">{schedule.activity}</span>
                            </label>
                          ) : (
                            <span className="schedule-activity">{schedule.activity}</span>
                          )}
                          {schedule.notes && (
                            <p className="schedule-notes">{schedule.notes}</p>
                          )}
                        </div>
                        {isAdmin && !off && (
                          <div className="schedule-item-actions">
                            <button
                              type="button"
                              className="schedule-action-btn"
                              onClick={() => handleSwap(schedule.id, 'up')}
                              disabled={idx === 0}
                              title="위로"
                            >
                              ▲
                            </button>
                            <button
                              type="button"
                              className="schedule-action-btn"
                              onClick={() => handleSwap(schedule.id, 'down')}
                              disabled={idx === daySchedules.length - 1}
                              title="아래로"
                            >
                              ▼
                            </button>
                            <button
                              type="button"
                              className="schedule-action-btn"
                              onClick={() => handleEdit(schedule)}
                              title="시간/내용 수정"
                            >
                              ✎
                            </button>
                            <button
                              type="button"
                              className={`schedule-action-btn ${!schedule.is_active ? 'active' : ''}`}
                              onClick={() => handleToggle(schedule.id)}
                              title={schedule.is_active ? '비활성화' : '활성화'}
                            >
                              {schedule.is_active ? 'ON' : 'OFF'}
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {showAddModal && addingDay != null && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{DAY_LABELS[addingDay]} 일정 추가</h3>
              <button type="button" className="modal-close" onClick={() => setShowAddModal(false)}>×</button>
            </div>
            <form onSubmit={handleAddSubmit}>
              <div className="modal-body">
                <div className="form-row">
                  <div className="form-group">
                    <label>시작 시간</label>
                    <input
                      type="time"
                      value={addForm.start_time}
                      onChange={(e) => setAddForm({ ...addForm, start_time: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>종료 시간</label>
                    <input
                      type="time"
                      value={addForm.end_time}
                      onChange={(e) => setAddForm({ ...addForm, end_time: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label>활동 *</label>
                  <input
                    type="text"
                    value={addForm.activity}
                    onChange={(e) => setAddForm({ ...addForm, activity: e.target.value })}
                    placeholder="예: 코딩테스트, 회사지원..."
                    required
                  />
                </div>
                <div className="form-group-checkbox">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={addForm.is_active}
                      onChange={(e) => setAddForm({ ...addForm, is_active: e.target.checked })}
                    />
                    <span>활성</span>
                  </label>
                </div>
                <div className="form-group">
                  <label>메모</label>
                  <textarea
                    value={addForm.notes}
                    onChange={(e) => setAddForm({ ...addForm, notes: e.target.value })}
                    rows={2}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAddModal(false)}>취소</button>
                <button type="submit" className="btn btn-primary">추가</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {editingSchedule && (
        <div className="modal-overlay" onClick={() => setEditingSchedule(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>일정 수정</h3>
              <button type="button" className="modal-close" onClick={() => setEditingSchedule(null)}>
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="form-row">
                <div className="form-group">
                  <label>시작 시간</label>
                  <input
                    type="time"
                    value={editingSchedule.start_time}
                    onChange={(e) =>
                      setEditingSchedule({ ...editingSchedule, start_time: e.target.value })
                    }
                  />
                </div>
                <div className="form-group">
                  <label>종료 시간</label>
                  <input
                    type="time"
                    value={editingSchedule.end_time}
                    onChange={(e) =>
                      setEditingSchedule({ ...editingSchedule, end_time: e.target.value })
                    }
                  />
                </div>
              </div>
              <div className="form-group">
                <label>활동</label>
                <input
                  type="text"
                  value={editingSchedule.activity}
                  onChange={(e) =>
                    setEditingSchedule({ ...editingSchedule, activity: e.target.value })
                  }
                />
              </div>
              <div className="form-group-checkbox">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={editingSchedule.is_active}
                    onChange={(e) =>
                      setEditingSchedule({ ...editingSchedule, is_active: e.target.checked })
                    }
                  />
                  <span>이 시간대 활성 (해제 시 휴무)</span>
                </label>
              </div>
              <div className="form-group">
                <label>메모</label>
                <textarea
                  value={editingSchedule.notes || ''}
                  onChange={(e) =>
                    setEditingSchedule({ ...editingSchedule, notes: e.target.value })
                  }
                  rows={3}
                />
              </div>
            </div>
            <div className="modal-footer modal-footer-edit">
              <button type="button" className="btn btn-danger-outline" onClick={handleDelete}>
                삭제
              </button>
              <div className="modal-footer-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setEditingSchedule(null)}>
                  취소
                </button>
                <button type="button" className="btn btn-primary" onClick={handleSave}>
                  저장
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Schedule;
