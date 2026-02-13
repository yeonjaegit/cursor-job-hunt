import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { companiesAPI } from '../api';

const Companies = () => {
  const { isAdmin } = useAuth();
  const [companies, setCompanies] = useState([]);
  const [stats, setStats] = useState({ total: 0, by_status: {} });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingCompany, setEditingCompany] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    position: '',
    status: 'applied',
    applied_date: new Date().toISOString().split('T')[0],
    interview_date: '',
    notes: '',
  });

  const statusOptions = [
    { value: 'applied', label: '서류 지원', bg: '#eff6ff', text: '#1e40af', border: '#93c5fd' },
    { value: 'docs_passed', label: '서류 합격', bg: '#f5f3ff', text: '#5b21b6', border: '#c4b5fd' },
    { value: 'interviewed', label: '면접 완료', bg: '#fffbeb', text: '#b45309', border: '#fcd34d' },
    { value: 'accepted', label: '최종 합격', bg: '#ecfdf5', text: '#047857', border: '#6ee7b7' },
    { value: 'rejected', label: '불합격', bg: '#fef2f2', text: '#b91c1c', border: '#fca5a5' },
  ];

  useEffect(() => {
    loadData();
  }, [isAdmin]);

  const loadData = async () => {
    try {
      const companiesRes = isAdmin 
        ? await companiesAPI.getAll() 
        : await companiesAPI.getPublicAll();
      const companiesList = companiesRes.data.companies || [];
      setCompanies(companiesList);
      
      if (isAdmin) {
        const statsRes = await companiesAPI.getStats();
        setStats(statsRes.data);
      } else {
        const byStatus = { applied: 0, docs_passed: 0, interviewed: 0, accepted: 0, rejected: 0 };
        companiesList.forEach(c => { byStatus[c.status] = (byStatus[c.status] || 0) + 1; });
        setStats({ total: companiesList.length, by_status: byStatus });
      }
    } catch (error) {
      console.error('Failed to load companies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    if (!isAdmin) {
      alert('관리자만 추가할 수 있습니다.');
      return;
    }
    setEditingCompany(null);
    setFormData({
      name: '',
      position: '',
      status: 'applied',
      applied_date: new Date().toISOString().split('T')[0],
      interview_date: '',
      notes: '',
    });
    setShowModal(true);
  };

  const handleEdit = (company) => {
    if (!isAdmin) {
      alert('관리자만 수정할 수 있습니다.');
      return;
    }
    setEditingCompany(company);
    setFormData({
      name: company.name,
      position: company.position,
      status: company.status,
      applied_date: company.applied_date,
      interview_date: company.interview_date || '',
      notes: company.notes || company.memo || '',
    });
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isAdmin) return;

    const payload = {
      name: formData.name,
      position: formData.position,
      status: formData.status,
      applied_date: formData.applied_date,
      interview_date: formData.interview_date || null,
      memo: formData.notes,
    };
    try {
      if (editingCompany) {
        await companiesAPI.update(editingCompany.id, payload);
        alert('수정되었습니다.');
      } else {
        await companiesAPI.create(payload);
        alert('추가되었습니다.');
      }
      setShowModal(false);
      loadData();
    } catch (error) {
      alert(error.response?.data?.error || '저장에 실패했습니다.');
    }
  };

  const handleDelete = async (companyId) => {
    if (!isAdmin) {
      alert('관리자만 삭제할 수 있습니다.');
      return;
    }

    if (!confirm('정말 삭제하시겠습니까?')) return;

    try {
      await companiesAPI.delete(companyId);
      alert('삭제되었습니다.');
      loadData();
    } catch (error) {
      alert('삭제에 실패했습니다.');
    }
  };

  const getStatusLabel = (status) => {
    return statusOptions.find((opt) => opt.value === status)?.label || status;
  };

  const getStatusStyle = (status) => {
    const opt = statusOptions.find((o) => o.value === status);
    if (!opt) return { backgroundColor: '#f1f5f9', color: '#475569', border: '1px solid #e2e8f0' };
    return { backgroundColor: opt.bg, color: opt.text, border: `1px solid ${opt.border}` };
  };

  if (loading) {
    return <div className="loading">로딩 중...</div>;
  }

  const filteredCompanies = companies.filter((company) =>
    company.name.toLowerCase().includes(searchTerm.trim().toLowerCase())
  );

  return (
    <div className="section companies-section">
      <div className="section-header">
        <h2 className="section-title">회사 지원 현황</h2>
        <div className="companies-header-actions">
          <div className="companies-search">
            <input
              type="text"
              placeholder="회사명 검색"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
              <button
                type="button"
                className="companies-search-clear"
                onClick={() => setSearchTerm('')}
              >
                ×
              </button>
            )}
          </div>
          {isAdmin && (
            <button className="btn btn-primary" onClick={handleAdd}>
              + 회사 추가
            </button>
          )}
        </div>
      </div>

      {stats && (
        <div className="stats-row companies-stats">
          <div className="stat-item">
            <span className="stat-label">총 지원</span>
            <span className="stat-value">{stats.total}개</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">서류 지원</span>
            <span className="stat-value">{stats.by_status?.applied || 0}개</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">서류 합격</span>
            <span className="stat-value">{stats.by_status?.docs_passed || 0}개</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">면접 완료</span>
            <span className="stat-value">{stats.by_status?.interviewed || 0}개</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">최종 합격</span>
            <span className="stat-value">{stats.by_status?.accepted || 0}개</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">불합격</span>
            <span className="stat-value">{stats.by_status?.rejected || 0}개</span>
          </div>
        </div>
      )}

      <div className="companies-list">
        {filteredCompanies.length === 0 ? (
          <p className="empty-message">
            {companies.length === 0 ? '지원한 회사가 없습니다.' : '검색 결과가 없습니다.'}
          </p>
        ) : (
          filteredCompanies.map((company) => (
            <div key={company.id} className="company-card">
              <div className="company-header">
                <h3>{company.name}</h3>
                <span
                  className="status-badge status-badge-readable"
                  style={getStatusStyle(company.status)}
                >
                  {getStatusLabel(company.status)}
                </span>
              </div>
              <div className="company-info">
                <p>
                  <strong>포지션:</strong> {company.position}
                </p>
                <p>
                  <strong>지원일:</strong>{' '}
                  {new Date(company.applied_date).toLocaleDateString('ko-KR')}
                </p>
                {company.interview_date && (
                  <p>
                    <strong>면접일:</strong>{' '}
                    {new Date(company.interview_date).toLocaleDateString('ko-KR')}
                  </p>
                )}
                {(company.notes || company.memo) && (
                  <p>
                    <strong>메모:</strong> {company.notes || company.memo}
                  </p>
                )}
              </div>
              {isAdmin && (
                <div className="company-actions">
                  <button className="btn-icon" onClick={() => handleEdit(company)}>수정</button>
                  <button className="btn-icon btn-danger" onClick={() => handleDelete(company.id)}>삭제</button>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingCompany ? '회사 수정' : '회사 추가'}</h3>
              <button type="button" className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="form-group">
                  <label>회사명 *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>포지션 *</label>
                  <input
                    type="text"
                    value={formData.position}
                    onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>상태</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    {statusOptions.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>지원일</label>
                  <input
                    type="date"
                    value={formData.applied_date}
                    onChange={(e) => setFormData({ ...formData, applied_date: e.target.value })}
                  />
                </div>
                {(formData.status === 'docs_passed' || formData.status === 'interviewed') && (
                  <div className="form-group">
                    <label>면접일 (서류 합격 시 설정)</label>
                    <input
                      type="date"
                      value={formData.interview_date}
                      onChange={(e) => setFormData({ ...formData, interview_date: e.target.value })}
                    />
                  </div>
                )}
                <div className="form-group">
                  <label>메모</label>
                  <textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    rows={3}
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
                  {editingCompany ? '수정' : '추가'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Companies;
