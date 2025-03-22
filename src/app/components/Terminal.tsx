import React from 'react';

interface TerminalProps {
  terminalOutput: string;
  isDarkMode: boolean;
}

const Terminal: React.FC<TerminalProps> = ({ terminalOutput, isDarkMode }) => {
  return (
    <main>
      <div
        className="w-full h-screen flex flex-col overflow-hidden text-wrap"
        style={{ borderRight: '2px solid #131314' }}
      >
        {/* Sticky Header */}
        <h1
          className={`sticky top-0 py-3 px-16 z-10 ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground'}`}
        >
          Output and Errors
        </h1>

        {/* Scrollable Terminal Output */}
        <div
          className={`px-4 py-2 text-sm font-mono flex-1 overflow-y-auto`}
        >
          <pre
            className={`pb-44 ${isDarkMode ? 'text-white' : 'text-black'}`}
            style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}
          >
            {terminalOutput}
          </pre>
        </div>
      </div>
    </main>
  );
};

export default Terminal;
