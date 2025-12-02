import React from 'react';

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
}

const StatCard: React.FC<StatCardProps> = ({ icon, label, value }) => {
  return (
    <div className={`bg-light-blue p-6 rounded-2xl text-black flex flex-col justify-between h-full`}>
      <div className="w-12 h-12 bg-cream rounded-xl flex items-center justify-center border border-light-blue">
        <span className="w-7 h-7 text-dark-blue">{icon}</span>
      </div>
      <div>
        <p className="text-3xl lg:text-4xl font-extrabold">{value}</p>
        <p className="text-sm font-medium opacity-80 mt-1">{label}</p>
      </div>
    </div>
  );
};

export default StatCard;