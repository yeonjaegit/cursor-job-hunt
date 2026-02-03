import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { codingAPI } from '../api';

const CodingTest = () => {
  const { isAdmin } = useAuth();
  const [problems, setProblems] = useState([]);
  const [stats, setStats] = useState({ total: 0, solved: 0, unsolved: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingProblem, setEditingProblem] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    platform: '프로그래머스',
    level: 0,
    is_solved: false,
    solved_date: new Date().toISOString().split('T')[0],
    url: '',
    notes: '',
  });

  const levelLabels = {
    0: 'Lv.0',
    1: 'Lv.1',
    2: 'Lv.2',
    3: 'Lv.3',
    4: 'Lv.4',
    5: 'Lv.5',
  };

  useEffect(() => {
    loadData();
  }, [isAdmin]);

  const loadData = async () => {
    try {
      const problemsRes = isAdmin 
        ? await codingAPI.getAll() 
        : await codingAPI.getPublicAll();
      const problemsList = problemsRes.data.problems || [];
      setProblems(problemsList);
      
      if (isAdmin) {
        const statsRes = await codingAPI.getStats();
        setStats(statsRes.data);
      } else {
        const solved = problemsList.filter(p => p.is_solved || p.status === 'solved').length;
        setStats({ total: problemsList.length, solved, unsolved: problemsList.length - solved });
      }
    } catch (error) {
      console.error('Failed to load coding problems:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    if (!isAdmin) {
      alert('관리자만 추가할 수 있습니다.');
      return;
    }
    setEditingProblem(null);
    setFormData({
      title: '',
      platform: '프로그래머스',
      level: 0,
      is_solved: false,
      solved_date: new Date().toISOString().split('T')[0],
      url: '',
      notes: '',
    });
    setShowModal(true);
  };

  const handleEdit = (problem) => {
    if (!isAdmin) {
      alert('관리자만 수정할 수 있습니다.');
      return;
    }
    setEditingProblem(problem);
    setFormData({
      title: problem.title,
      platform: '프로그래머스',
      level: problem.level,
      is_solved: problem.is_solved || problem.status === 'solved',
      solved_date: problem.solved_date || new Date().toISOString().split('T')[0],
      url: problem.url || '',
      notes: problem.notes || problem.memo || '',
    });
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isAdmin) return;

    const payload = {
      title: formData.title,
      platform: '프로그래머스',
      level: formData.level,
      status: formData.is_solved ? 'solved' : 'failed',
      solved_date: formData.solved_date,
      memo: formData.notes || null,
    };

    try {
      if (editingProblem) {
        await codingAPI.update(editingProblem.id, payload);
        alert('수정되었습니다.');
      } else {
        await codingAPI.create(payload);
        alert('추가되었습니다.');
      }
      setShowModal(false);
      loadData();
    } catch (error) {
      alert(error.response?.data?.error || '저장에 실패했습니다.');
    }
  };

  const handleDelete = async (problemId) => {
    if (!isAdmin) {
      alert('관리자만 삭제할 수 있습니다.');
      return;
    }

    if (!confirm('정말 삭제하시겠습니까?')) return;

    try {
      await codingAPI.delete(problemId);
      alert('삭제되었습니다.');
      loadData();
    } catch (error) {
      alert('삭제에 실패했습니다.');
    }
  };

  const toggleSolved = async (problemId, currentlySolved) => {
    if (!isAdmin) {
      alert('관리자만 상태를 변경할 수 있습니다.');
      return;
    }

    const problem = problems.find(p => p.id === problemId);
    if (!problem) return;

    try {
      await codingAPI.update(problemId, {
        title: problem.title,
        platform: '프로그래머스',
        level: problem.level,
        status: currentlySolved ? 'failed' : 'solved',
        solved_date: problem.solved_date || new Date().toISOString().split('T')[0],
        memo: problem.memo || problem.notes || null,
      });
      loadData();
    } catch (error) {
      alert(error.response?.data?.error || '상태 변경에 실패했습니다.');
    }
  };

  if (loading) {
    return <div className="loading">로딩 중...</div>;
  }

  const solvedProblems = problems.filter((p) => p.is_solved || p.status === 'solved');
  const unsolvedProblems = problems.filter((p) => !p.is_solved && p.status !== 'solved');
  const progress = problems.length > 0 ? (solvedProblems.length / problems.length) * 100 : 0;

  return (
    <div className="section coding-section">
      <div className="section-header">
        <h2 className="section-title">코딩 테스트</h2>
        {isAdmin && (
          <button className="btn btn-primary" onClick={handleAdd}>
            + 문제 추가
          </button>
        )}
      </div>

      {stats && (
        <div className="stats-row">
          <div className="stat-item">
            <span className="stat-label">총 문제:</span>
            <span className="stat-value">{stats.total}개</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">해결:</span>
            <span className="stat-value">{stats.solved}개</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">미해결:</span>
            <span className="stat-value">{stats.unsolved}개</span>
          </div>
        </div>
      )}

      {problems.length > 0 && (
        <div className="progress-section">
          <div className="progress-header">
            <span>진행률: {Math.round(progress)}%</span>
            <span>
              {solvedProblems.length} / {problems.length}
            </span>
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
        </div>
      )}

      {unsolvedProblems.length > 0 && (
        <div className="problems-group">
          <h3>미해결</h3>
          <div className="problems-list">
            {unsolvedProblems.map((problem) => (
              <div key={problem.id} className="problem-card unsolved">
                <div className="problem-header">
                  <div className="problem-title">
                    {problem.url ? (
                      <a href={problem.url} target="_blank" rel="noopener noreferrer">
                        {problem.title}
                      </a>
                    ) : (
                      <span>{problem.title}</span>
                    )}
                    <span className="problem-platform-inline">{problem.platform}</span>
                  </div>
                  <span className="problem-level">{levelLabels[problem.level] ?? `Lv.${problem.level}`}</span>
                </div>
                <div className="problem-info">
                  {(problem.notes || problem.memo) && <p className="problem-notes">{problem.notes || problem.memo}</p>}
                </div>
                {isAdmin && (
                  <div className="problem-actions">
                    <button
                      className="btn-icon"
                      onClick={() => toggleSolved(problem.id, problem.is_solved || problem.status === 'solved')}
                      title="해결 완료"
                    >
                      완료
                    </button>
                    <button className="btn-icon" onClick={() => handleEdit(problem)}>수정</button>
                    <button className="btn-icon btn-danger" onClick={() => handleDelete(problem.id)}>삭제</button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {solvedProblems.length > 0 && (
        <div className="problems-group">
          <h3>해결 완료</h3>
          <div className="problems-list">
            {solvedProblems.map((problem) => (
              <div key={problem.id} className="problem-card solved">
                <div className="problem-header">
                  <div className="problem-title">
                    {problem.url ? (
                      <a href={problem.url} target="_blank" rel="noopener noreferrer">
                        {problem.title}
                      </a>
                    ) : (
                      <span>{problem.title}</span>
                    )}
                    <span className="problem-platform-inline">{problem.platform}</span>
                  </div>
                  <span className="problem-level">{levelLabels[problem.level] ?? `Lv.${problem.level}`}</span>
                </div>
                <div className="problem-info">
                  {(problem.notes || problem.memo) && <p className="problem-notes">{problem.notes || problem.memo}</p>}
                </div>
                {isAdmin && (
                  <div className="problem-actions">
                    <button
                      className="btn-icon"
                      onClick={() => toggleSolved(problem.id, problem.is_solved || problem.status === 'solved')}
                      title="미해결로 변경"
                    >
                      미완료
                    </button>
                    <button className="btn-icon" onClick={() => handleEdit(problem)}>수정</button>
                    <button className="btn-icon btn-danger" onClick={() => handleDelete(problem.id)}>삭제</button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {problems.length === 0 && <p className="empty-message">등록된 문제가 없습니다.</p>}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingProblem ? '문제 수정' : '문제 추가'}</h3>
              <button type="button" className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="form-group">
                  <label>문제 제목 *</label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>난이도</label>
                  <select
                    value={formData.level}
                    onChange={(e) => setFormData({ ...formData, level: parseInt(e.target.value) })}
                  >
                    {[0, 1, 2, 3, 4, 5].map((level) => (
                      <option key={level} value={level}>
                        {levelLabels[level]}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>URL</label>
                  <input
                    type="url"
                    value={formData.url}
                    onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                    placeholder="https://..."
                  />
                </div>
                <div className="form-group">
                  <label>해결일</label>
                  <input
                    type="date"
                    value={formData.solved_date}
                    onChange={(e) => setFormData({ ...formData, solved_date: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group form-group-checkbox">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.is_solved}
                      onChange={(e) => setFormData({ ...formData, is_solved: e.target.checked })}
                    />
                    <span>해결 완료</span>
                  </label>
                </div>
                <div className="form-group">
                  <label>메모</label>
                  <textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    rows={3}
                    placeholder="풀이 방법, 알고리즘 등"
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  취소
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingProblem ? '수정' : '추가'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default CodingTest;
