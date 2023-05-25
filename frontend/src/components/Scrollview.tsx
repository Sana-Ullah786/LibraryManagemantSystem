import React from "react";

interface ScrollViewProps {
  children: React.ReactNode;
}

const ScrollView: React.FC<ScrollViewProps> = ({ children }) => {
  return (
    <div
      style={{
        overflowY: "scroll",
        height: "300px",
        width: "30vw",
        scrollbarWidth: "thin",
        scrollbarColor: "transparent transparent", // Hide scrollbar
      }}
    >
      {children}
    </div>
  );
};

export default ScrollView;
