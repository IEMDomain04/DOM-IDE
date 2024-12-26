import React from 'react';

interface TopnavProps {
  onRunClick: () => void;
}

export default function Topnav({ onRunClick }: TopnavProps) {
  return (
    <div>
      {/* Top Nav */}
      <div className="flex justify-around px-10 py-2 bg-purple-950">
        {/* Logo and Title of Compiler */}
        <div className="flex gap-x-2 items-center">
          <img src="/dom-icon.svg" width={20} height={20} alt="Dom icon" />
          <h1 className='text-xsfont-bold'>DOM COMPILER</h1>
        </div>

        {/* Saves and runs */}
        <div className="flex gap-x-5">
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110">
            <h1 className='text-xs'>Save as...</h1>
          </div>

          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110">
            <h1 className='text-xs'>Open</h1>
          </div>
          
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110" onClick={onRunClick}>
            <img className='h-auto w-3' src={`/run-icon.svg`} alt="" />
            <h1 className='text-xs'>Run</h1>
          </div>
        </div>

        <div className="flex gap-x-5">
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110">
            <h1 className='text-xs'>Tokenizer</h1>
          </div>

          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110">
            <h1 className='text-xs'>Syntax</h1>
          </div>
          
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110">
            <h1 className='text-xs'>Semantic</h1>
          </div>
        </div>
      </div>
    </div>
  );
}