import React from 'react';

interface SolidButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  icon?: React.ReactNode;
}

const SolidButton: React.FC<SolidButtonProps> = ({
  children,
  icon,
  className = '',
  ...props
}) => {
  return (
    <button
      className={`relative inline-flex items-center justify-center gap-2 px-6 py-3 text-sm font-semibold text-cream bg-dark-blue rounded-xl overflow-hidden transition-all duration-300 ease-in-out hover:bg-black focus:outline-none focus:ring-4 focus:ring-dark-blue/50 ${className}`}
      {...props}
    >
      {icon && <span className="w-5 h-5">{icon}</span>}
      {children}
    </button>
  );
};

export default SolidButton;