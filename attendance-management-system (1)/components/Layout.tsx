import React from 'react';
import Navbar from './Navbar';
import MobileBottomNav from './MobileBottomNav';
import { User, Page } from '../types';

interface LayoutProps {
  children: React.ReactNode;
  user: User;
  currentPage: Page;
  onNavigate: (page: Page) => void;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, user, currentPage, onNavigate, onLogout }) => {
  return (
    <div className="min-h-screen font-sans bg-cream">
      <Navbar
        user={user}
        currentPage={currentPage}
        onNavigate={onNavigate}
        onLogout={onLogout}
      />
      <main className="pt-8 px-4 sm:px-6 lg:px-8 md:pt-28 pb-24 md:pb-8">
        <div className="max-w-7xl mx-auto">
            {children}
        </div>
      </main>
      <MobileBottomNav
        currentPage={currentPage}
        onNavigate={onNavigate}
      />
    </div>
  );
};

export default Layout;