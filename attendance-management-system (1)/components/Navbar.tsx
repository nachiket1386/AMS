import React from 'react';
import { User, Page } from '../types';
import { CalendarIcon, DataIcon, ExportIcon, HomeIcon, Icon, LogsIcon, LogoutIcon, UploadIcon, UsersIcon } from '../constants';

interface NavbarProps {
  user: User;
  currentPage: Page;
  onNavigate: (page: Page) => void;
  onLogout: () => void;
}

const NavLink: React.FC<{
  page: Page;
  currentPage: Page;
  onClick: (page: Page) => void;
  icon: React.ReactNode;
  children: React.ReactNode;
}> = ({ page, currentPage, onClick, icon, children }) => {
  const isActive = currentPage === page;
  return (
    <a
      href="#"
      onClick={(e) => {
        e.preventDefault();
        onClick(page);
      }}
      className={`relative flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-colors duration-200 ${
        isActive ? 'text-dark-blue font-bold' : 'text-black hover:bg-black/10'
      }`}
    >
      <span className="z-10">{icon}</span>
      <span className="z-10">{children}</span>
    </a>
  );
};

const Navbar: React.FC<NavbarProps> = ({ user, currentPage, onNavigate, onLogout }) => {
  const navItems = [
    { page: Page.Dashboard, icon: <Icon><HomeIcon /></Icon>, label: 'Dashboard' },
    { page: Page.Upload, icon: <Icon><UploadIcon /></Icon>, label: 'Upload' },
    { page: Page.Data, icon: <Icon><DataIcon /></Icon>, label: 'Data' },
    { page: Page.Export, icon: <Icon><ExportIcon /></Icon>, label: 'Export' },
    { page: Page.Logs, icon: <Icon><LogsIcon /></Icon>, label: 'Logs' },
    { page: Page.Users, icon: <Icon><UsersIcon /></Icon>, label: 'Users' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-light-blue border-b border-dark-blue hidden md:block">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-dark-blue text-cream">
                <Icon className="w-6 h-6"><CalendarIcon/></Icon>
            </div>
            <span className="text-xl font-bold text-black hidden sm:block">Attendance System</span>
          </div>
          
          <nav className="flex items-center gap-2">
            {navItems.map(item => (
                <NavLink key={item.page} page={item.page} currentPage={currentPage} onClick={onNavigate} icon={item.icon}>{item.label}</NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-cream/50 p-2 rounded-full">
              <div className="w-8 h-8 rounded-full bg-dark-blue flex items-center justify-center text-cream font-bold text-sm">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <div className="hidden lg:block">
                <p className="text-sm font-semibold text-black">{user.username}</p>
                <p className="text-xs text-black/70">{user.role}</p>
              </div>
            </div>
            <button
              onClick={onLogout}
              className="flex items-center justify-center w-10 h-10 rounded-full text-black hover:bg-black hover:text-cream transition-colors"
              title="Logout"
            >
              <Icon><LogoutIcon/></Icon>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;