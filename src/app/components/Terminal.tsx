import React, { useEffect, useRef, useState } from 'react';

interface TerminalProps {
  terminalOutput: string;
  isDarkMode: boolean;
  onInputSubmit?: (input: string) => void;
  inputPrompt?: string | null;
}

const Terminal: React.FC<TerminalProps> = ({
  terminalOutput,
  isDarkMode,
  onInputSubmit,
  inputPrompt
}) => {
  const [inputValue, setInputValue] = useState('');
  const terminalEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [terminalOutput]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputPrompt && onInputSubmit) {
      onInputSubmit(inputValue);
      setInputValue('');
    }
  };

  return (
    <main>
      <div
        className="w-full flex flex-col overflow-hidden text-wrap"
        style={{ borderRight: '2px solid #131314' }}
      >
        <h1
          className={`sticky top-0 py-3 px-16 z-10 ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground'}`}
        >
          Output and Errors
        </h1>

        <div className="px-4 py-2 text-sm font-mono flex-1 overflow-y-auto">
          <pre
            className={`pb-10 ${isDarkMode ? 'text-white' : 'text-black'}`}
            style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}
          >
            {terminalOutput}
          </pre>

          {/* Input prompt line */}
          {inputPrompt && (
            <div className="flex items-center gap-2 mt-2">
              <span className="text-green-400">{inputPrompt}</span>
              <input
                className="bg-transparent text-white focus:outline-none px-2 py-1"
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                autoFocus
              />
            </div>
          )}
          <div ref={terminalEndRef} />
        </div>
      </div>
    </main>
  );
};

export default Terminal;
