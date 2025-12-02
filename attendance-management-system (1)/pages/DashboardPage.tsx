import React from 'react';
import Card from '../components/Card';
import StatCard from '../components/StatCard';
import { Page, User } from '../types';
import { ClipboardListIcon, BuildingIcon, UserShieldIcon, BoltIcon, MapMarkerIcon, UploadIcon, DataIcon, ExportIcon, UsersIcon, LogoutIcon, Icon } from '../constants';
import SolidButton from '../components/GradientButton';

interface DashboardPageProps {
  user: User;
  onNavigate: (page: Page) => void;
  onLogout?: () => void;
}

const DashboardPage: React.FC<DashboardPageProps> = ({ user, onNavigate, onLogout }) => {
  return (
    <div className="space-y-8">
      {/* Mobile Header */}
      <div className="md:hidden flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-black">Hello, {user.username}</h1>
          <p className="text-sm text-black/70">Here's your overview.</p>
        </div>
        <button
          onClick={onLogout}
          className="flex items-center justify-center w-10 h-10 rounded-full text-black bg-light-blue/50 hover:bg-light-blue transition-colors"
          title="Logout"
        >
          <Icon><LogoutIcon/></Icon>
        </button>
      </div>

      {/* Desktop Header */}
      <div className="hidden md:block">
        <h1 className="text-3xl md:text-4xl font-extrabold text-black">
          Dashboard
        </h1>
        <p className="text-black/70 mt-1">Welcome back, {user.username}! Here's your overview.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard icon={<ClipboardListIcon />} label="Total Attendance Records" value="1,879" />
        <StatCard icon={<BuildingIcon />} label="Active Companies" value="3" />
        <StatCard icon={<UserShieldIcon />} label="Your Role" value={user.role} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-6">
                <BoltIcon className="w-6 h-6 text-dark-blue" />
                <h2 className="text-xl font-bold text-black">Quick Actions</h2>
            </div>
            <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
               <SolidButton onClick={() => onNavigate(Page.Upload)} icon={<UploadIcon/>}>Upload CSV</SolidButton>
               <SolidButton onClick={() => onNavigate(Page.Data)} icon={<DataIcon/>}>View Data</SolidButton>
               <SolidButton onClick={() => onNavigate(Page.Export)} icon={<ExportIcon/>}>Export Data</SolidButton>
               <SolidButton onClick={() => onNavigate(Page.Users)} icon={<UsersIcon/>}>Manage Users</SolidButton>
            </div>
        </Card>
        <Card>
             <div className="flex items-center gap-3 mb-4">
                <BuildingIcon className="w-6 h-6 text-dark-blue" />
                <h2 className="text-xl font-bold text-black">Company Info</h2>
            </div>
            <div className="space-y-3">
                <p className="font-semibold text-black">{user.company}</p>
                <div className="flex items-start gap-2 text-sm text-black/80">
                    <MapMarkerIcon className="w-5 h-5 mt-0.5 flex-shrink-0 text-dark-blue" />
                    <span>123 Innovation Drive, Suite 456, Tech City, 78910</span>
                </div>
            </div>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;