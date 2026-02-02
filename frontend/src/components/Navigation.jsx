import { useAuth } from '../contexts/AuthContext';

const Navigation = ({ currentSection, onSectionChange, onShowAdminLogin }) => {
  const { isAdmin, logout } = useAuth();

  const sections = [
    { id: 'dashboard', name: '대시보드' },
    { id: 'attendance', name: '출석' },
    { id: 'schedule', name: '일정' },
    { id: 'companies', name: '회사 지원' },
    { id: 'coding', name: '코딩테스트' },
  ];

  return (
    <nav className="nav">
      <div className="nav-brand">
        <a href="#" onClick={(e) => { e.preventDefault(); onSectionChange('dashboard'); }}>
          취업 준비
        </a>
      </div>
      
      <ul className="nav-links">
        {sections.map((section) => (
          <li key={section.id}>
            <a
              href={`#${section.id}`}
              className={currentSection === section.id ? 'active' : ''}
              onClick={(e) => {
                e.preventDefault();
                onSectionChange(section.id);
              }}
            >
              {section.name}
            </a>
          </li>
        ))}
      </ul>

      <div className="nav-actions">
        {isAdmin ? (
          <button className="btn-logout" onClick={logout}>로그아웃</button>
        ) : (
          <button className="btn-login" onClick={onShowAdminLogin}>로그인</button>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
