import { useState, useEffect } from 'react';
import { AuthProvider } from './contexts/AuthContext';
import Navigation from './components/Navigation';
import AdminLogin from './components/AdminLogin';
import Dashboard from './components/Dashboard';
import Attendance from './components/Attendance';
import Schedule from './components/Schedule';
import Companies from './components/Companies';
import CodingTest from './components/CodingTest';
import './App.css';

const VALID_SECTIONS = ['dashboard', 'attendance', 'schedule', 'companies', 'coding'];

const getSectionFromHash = () => {
  const hash = window.location.hash.replace(/^#/, '');
  return VALID_SECTIONS.includes(hash) ? hash : 'dashboard';
};

function App() {
  const [currentSection, setCurrentSection] = useState(getSectionFromHash);
  const [showAdminLogin, setShowAdminLogin] = useState(false);

  useEffect(() => {
    const onHashChange = () => setCurrentSection(getSectionFromHash());
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const setSection = (id) => {
    window.location.hash = id;
    setCurrentSection(id);
  };

  const renderSection = () => {
    const goTo = (id) => setSection(id);
    switch (currentSection) {
      case 'dashboard':
        return <Dashboard onNavigate={goTo} />;
      case 'attendance':
        return <Attendance />;
      case 'schedule':
        return <Schedule />;
      case 'companies':
        return <Companies />;
      case 'coding':
        return <CodingTest />;
      default:
        return <Dashboard onNavigate={goTo} />;
    }
  };

  return (
    <AuthProvider>
      <div className="app">
        <Navigation
          currentSection={currentSection}
          onSectionChange={setSection}
          onShowAdminLogin={() => setShowAdminLogin(true)}
        />
        
        <main className="main-content">
          {renderSection()}
        </main>

        {showAdminLogin && <AdminLogin onClose={() => setShowAdminLogin(false)} />}
      </div>
    </AuthProvider>
  );
}

export default App;
