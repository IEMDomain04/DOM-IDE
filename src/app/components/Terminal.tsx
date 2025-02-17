import React from 'react';

interface TerminalProps {
  terminalOutput: string;
  isDarkMode: boolean;
}

const Terminal: React.FC<TerminalProps> = ({ terminalOutput, isDarkMode }) => {
  return (
    <main>
      {terminalOutput && (
        <div
        className="w-full h-screen flex flex-col"
        style={{ resize: 'none', borderRight: '2px solid #131314' }}
      >
        <h1
          className={`py-3 px-16 ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground'}`}
        >
          Output and Errors
        </h1>
      
        <div
          className={`px-4 py-2 text-sm font-mono flex-1 ${isDarkMode ? 'text-white' : 'text-black'}`}
        >
          <pre>{terminalOutput}</pre>
        </div>
      </div>
      
      )}
    </main>
  );
};

export default Terminal;
