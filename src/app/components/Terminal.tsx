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
    <main className="h-full text-sm font-mono text-white bg-transparent">
      <div className="flex flex-col h-full px-4 py-2 overflow-hidden">
        <div className={`font-jujutsu font-semibold p-2 tracking-widest ${isDarkMode ? 'text-blue-400' : 'text-black'}`}>TERMINAL</div>

        <div className="flex-1 overflow-y-auto whitespace-pre-wrap">
          <pre>{terminalOutput}</pre>
          {inputPrompt && (
            <div className="flex items-center gap-2 mt-2">
              <span className="text-green-400">{inputPrompt}</span>
              <input
                className="bg-transparent border-b border-gray-500 focus:outline-none px-2 py-1 w-1/2"
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
