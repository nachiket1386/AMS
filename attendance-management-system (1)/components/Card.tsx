import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: string;
}

const Card: React.FC<CardProps> = ({ children, className = '', padding = 'p-6 md:p-8' }) => {
  return (
    <div className={`bg-cream border border-light-blue rounded-2xl ${padding} ${className}`}>
      {children}
    </div>
  );
};

export default Card;