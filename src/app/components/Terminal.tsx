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
          className="bg-black w-full h-full"
          style={{ resize: 'none', borderRight: '2px solid #131314' }}
        >
          <h1
            className={`py-3 px-16 ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground'}`}
          >
            Output and Errors
          </h1>
          <div
            className={`pl-4 py-2 pr-0 text-sm font-mono min-h-96 ${isDarkMode ? 'text-white' : 'text-black'}`}
          >
            <div className="w-full relative rounded-md night-bg-content transition-all h-full flex flex-col night-text overflow-x-hidden overflow-y-hidden max-h-[120px]">
              <pre className="whitespace-pre-wrap">{terminalOutput}</pre>
            </div>
          </div>
        </div>
      )}
    </main>
  );
};

export default Terminal;
