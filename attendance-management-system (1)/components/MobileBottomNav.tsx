import React from 'react';
import { Page } from '../types';
import { DataIcon, HomeIcon, Icon, LogsIcon, UploadIcon, UsersIcon } from '../constants';

interface MobileBottomNavProps {
  currentPage: Page;
  onNavigate: (page: Page) => void;
}

const NavItem: React.FC<{
  page: Page;
  currentPage: Page;
  onClick: (page: Page) => void;
  icon: React.ReactNode;
  label: string;
}> = ({ page, currentPage, onClick, icon, label }) => {
  const isActive = currentPage === page;
  return (
    <a
      href="#"
      onClick={(e) => {
        e.preventDefault();
        onClick(page);
      }}
      className={`flex-1 flex flex-col items-center justify-center pt-2 pb-1 gap-1 transition-colors duration-200 ${
        isActive ? 'text-dark-blue' : 'text-black/70 hover:text-dark-blue'
      }`}
    >
      <div className="w-6 h-6">{icon}</div>
      <span className="text-xs font-semibold">{label}</span>
      {isActive && <div className="w-1.5 h-1.5 bg-dark-blue rounded-full mt-1"></div>}
    </a>
  );
};

const MobileBottomNav: React.FC<MobileBottomNavProps> = ({ currentPage, onNavigate }) => {
  const navItems = [
    { page: Page.Dashboard, icon: <HomeIcon />, label: 'Home' },
    { page: Page.Upload, icon: <UploadIcon />, label: 'Upload' },
    { page: Page.Data, icon: <DataIcon />, label: 'Data' },
    { page: Page.Logs, icon: <LogsIcon />, label: 'Logs' },
    { page: Page.Users, icon: <UsersIcon />, label: 'Users' },
  ];

  return (
    <footer className="md:hidden fixed bottom-0 left-0 right-0 h-20 bg-light-blue border-t border-dark-blue z-50">
      <nav className="flex items-stretch justify-around h-full">
        {navItems.map(item => (
          <NavItem
            key={item.page}
            page={item.page}
            currentPage={currentPage}
            onClick={onNavigate}
            icon={item.icon}
            label={item.label}
          />
        ))}
      </nav>
    </footer>
  );
};

export default MobileBottomNav;