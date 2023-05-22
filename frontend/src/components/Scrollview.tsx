import React from 'react';

interface ScrollViewProps {
  children: React.ReactNode;
}

const ScrollView: React.FC<ScrollViewProps> = ({ children }) => {
  return (
    <div
    style={{
      overflowY: 'scroll',
      maxHeight: '300px',
      scrollbarWidth: 'thin',
      scrollbarColor: 'transparent transparent', // Hide scrollbar
    }}
  >
      {children}
    </div>
  );
};

export default ScrollView;
