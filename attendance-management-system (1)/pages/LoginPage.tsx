import React, { useState } from 'react';
import Card from '../components/Card';
import SolidButton from '../components/GradientButton';
import { CalendarIcon, LockIcon, UserIcon } from '../constants';

interface LoginPageProps {
  onLogin: (username: string) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (username) {
      onLogin(username);
    }
  };

  const setDemoCredentials = (user: string) => {
    setUsername(user);
    setPassword('password123');
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-4 bg-cream">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
            <div className="inline-block p-4 rounded-2xl bg-cream border-2 border-light-blue mb-4">
                <CalendarIcon className="w-8 h-8 text-dark-blue" />
            </div>
            <h1 className="text-5xl font-extrabold text-black">Welcome Back</h1>
            <p className="text-black/70 mt-2">Sign in to your account to continue</p>
        </div>

        <Card>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="text-sm font-semibold text-black/80">Username</label>
              <div className="relative mt-2">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/50">
                  <UserIcon className="w-5 h-5" />
                </span>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g., admin"
                  className="w-full pl-10 pr-4 py-3 bg-cream text-black border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition placeholder:text-black/50"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-semibold text-black/80">Password</label>
              <div className="relative mt-2">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/50">
                    <LockIcon className="w-5 h-5" />
                </span>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-3 bg-cream text-black border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition placeholder:text-black/50"
                />
              </div>
            </div>
            <SolidButton type="submit" className="w-full !py-4 text-base">
              Sign In
            </SolidButton>
          </form>
        </Card>

        <div className="mt-6 text-center text-sm text-black/70">
          <p>Or use one of the demo accounts:</p>
          <div className="flex justify-center gap-2 mt-2 font-semibold">
            <button onClick={() => setDemoCredentials('root')} className="px-3 py-1 text-black bg-light-blue/50 rounded-lg hover:bg-light-blue transition">root</button>
            <button onClick={() => setDemoCredentials('admin')} className="px-3 py-1 text-black bg-light-blue/50 rounded-lg hover:bg-light-blue transition">admin</button>
            <button onClick={() => setDemoCredentials('user1')} className="px-3 py-1 text-black bg-light-blue/50 rounded-lg hover:bg-light-blue transition">user1</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;