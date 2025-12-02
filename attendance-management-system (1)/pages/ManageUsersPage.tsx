import React from 'react';
import Card from '../components/Card';
import SolidButton from '../components/GradientButton';
import Badge from '../components/Badge';
import { MOCK_USERS } from '../constants';
import { UserRole } from '../types';
import { UsersIcon, UserPlusIcon, UserIcon, LockIcon, UserTagIcon, BuildingIcon } from '../constants';

const roleStyles: { [key in UserRole]: { style: string; emoji: string } } = {
    [UserRole.Root]: { style: 'bg-black text-cream', emoji: '👑' },
    [UserRole.Admin]: { style: 'bg-dark-blue text-cream', emoji: '🛡️' },
    [UserRole.User]: { style: 'bg-light-blue text-black', emoji: '👤' },
};

const statusStyles = {
    Active: 'bg-dark-blue text-cream',
    Inactive: 'bg-cream text-black border border-black',
};

const ManageUsersPage: React.FC = () => {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl md:text-4xl font-extrabold text-black flex items-center gap-3">
                    <UsersIcon className="w-8 h-8"/>
                    Manage Users
                </h1>
                <p className="text-black/70 mt-1 hidden md:block">Create and manage user accounts.</p>
            </div>

            <Card>
                <h2 className="text-xl font-bold text-black flex items-center gap-3 mb-6">
                    <UserPlusIcon className="w-6 h-6"/>
                    Create New User
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-end">
                    <div className="relative">
                        <label className="text-sm font-semibold text-black/80">Username</label>
                        <UserIcon className="w-5 h-5 absolute bottom-3 left-3 text-black/40"/>
                        <input type="text" placeholder="newuser" className="w-full mt-2 pl-10 pr-4 py-2.5 bg-cream border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black placeholder:text-black/50" />
                    </div>
                    <div className="relative">
                        <label className="text-sm font-semibold text-black/80">Password</label>
                        <LockIcon className="w-5 h-5 absolute bottom-3 left-3 text-black/40"/>
                        <input type="password" placeholder="••••••••" className="w-full mt-2 pl-10 pr-4 py-2.5 bg-cream border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black placeholder:text-black/50" />
                    </div>
                    <div className="relative">
                        <label className="text-sm font-semibold text-black/80">Role</label>
                        <UserTagIcon className="w-5 h-5 absolute bottom-3 left-3 text-black/40"/>
                        <select className="w-full mt-2 pl-10 pr-4 py-2.5 bg-cream border border-light-blue rounded-xl appearance-none focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black">
                            <option>User1</option>
                            <option>Admin</option>
                            <option>Root</option>
                        </select>
                    </div>
                    <div className="relative">
                        <label className="text-sm font-semibold text-black/80">Company</label>
                        <BuildingIcon className="w-5 h-5 absolute bottom-3 left-3 text-black/40"/>
                        <select className="w-full mt-2 pl-10 pr-4 py-2.5 bg-cream border border-light-blue rounded-xl appearance-none focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black">
                            <option>Innovate Inc.</option>
                            <option>Tech Solutions</option>
                            <option>Future Corp</option>
                        </select>
                    </div>
                </div>
                <SolidButton className="mt-6 w-full md:w-auto">Create User</SolidButton>
            </Card>

            <Card padding="p-0">
                <div className="p-6">
                    <h2 className="text-xl font-bold text-black flex items-center gap-3">
                       <UsersIcon className="w-6 h-6"/>
                        Existing Users
                    </h2>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left text-black mobile-card-view">
                        <thead className="text-xs text-black uppercase bg-light-blue">
                            <tr>
                                <th scope="col" className="px-6 py-4">Username</th>
                                <th scope="col" className="px-6 py-4">Role</th>
                                <th scope="col" className="px-6 py-4">Company</th>
                                <th scope="col" className="px-6 py-4">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {MOCK_USERS.map(user => (
                                <tr key={user.id} className="bg-cream border-b border-light-blue hover:bg-light-blue/40 transition-colors">
                                    <td data-label="Username" className="px-6 py-4 font-semibold text-black">{user.username}</td>
                                    <td data-label="Role" className="px-6 py-4">
                                        <Badge className={`${roleStyles[user.role].style} whitespace-nowrap`}>
                                            {roleStyles[user.role].emoji} {user.role}
                                        </Badge>
                                    </td>
                                    <td data-label="Company" className="px-6 py-4">
                                        <Badge className="bg-light-blue text-black">{user.company}</Badge>
                                    </td>
                                    <td data-label="Status" className="px-6 py-4">
                                        <Badge className={statusStyles[user.status]}>
                                            {user.status}
                                        </Badge>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    );
};

export default ManageUsersPage;