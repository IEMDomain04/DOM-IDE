import React from 'react';

interface TopnavProps {
  onRunClick: () => void;
}

export default function Topnav({ onRunClick }: TopnavProps) {
  return (
    <div>
      {/* Top Nav */}
      <div className="flex space-x-20 px-10 py-2" style={{ backgroundColor: '#201d38' }}>
        {/* Logo and Title of Compiler */}
        <div className="flex gap-x-2 items-center">
          <img src="/dom-icon.svg" width={30} height={30} alt="Dom icon" />
          <h1>DOM COMPILER</h1>
        </div>

        {/* Saves and runs */}
        <div className="flex gap-x-12">
          <div className="flex w-auto gap-x-2 px-3 py-3 rounded cursor-pointer duration-100 bg-purple-500/10 hover:bg-purple-500/50 hover:scale-110" onClick={onRunClick}>
            <img src={`/run-icon.svg`} alt="" />
            <h1>RUN</h1>
          </div>
        </div>
      </div>
    </div>
  );
}