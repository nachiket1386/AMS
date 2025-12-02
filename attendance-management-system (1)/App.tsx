import React, { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import UploadCsvPage from './pages/UploadCsvPage';
import ViewDataPage from './pages/ViewDataPage';
import UploadLogsPage from './pages/UploadLogsPage';
import ManageUsersPage from './pages/ManageUsersPage';
import Layout from './components/Layout';
import { Page, User, UserRole } from './types';
import ExportPage from './pages/ExportPage';

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState<Page>(Page.Dashboard);

  const handleLogin = (username: string) => {
    // Mock login logic
    let role: UserRole = UserRole.User;
    if (username.toLowerCase() === 'root') role = UserRole.Root;
    if (username.toLowerCase() === 'admin') role = UserRole.Admin;
    
    setUser({ username: username, role: role, company: 'Innovate Inc.' });
    setCurrentPage(Page.Dashboard);
  };

  const handleLogout = () => {
    setUser(null);
  };

  const renderPage = () => {
    switch (currentPage) {
      case Page.Dashboard:
        return <DashboardPage user={user!} onNavigate={setCurrentPage} onLogout={handleLogout} />;
      case Page.Upload:
        return <UploadCsvPage />;
      case Page.Data:
        return <ViewDataPage />;
      case Page.Export:
        return <ExportPage />;
      case Page.Logs:
        return <UploadLogsPage />;
      case Page.Users:
        return <ManageUsersPage />;
      default:
        return <DashboardPage user={user!} onNavigate={setCurrentPage} onLogout={handleLogout} />;
    }
  };

  if (!user) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <Layout
      user={user}
      currentPage={currentPage}
      onNavigate={setCurrentPage}
      onLogout={handleLogout}
    >
      {renderPage()}
    </Layout>
  );
};

export default App;