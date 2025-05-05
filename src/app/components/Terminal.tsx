import React, { useEffect, useRef, useState } from 'react';

interface TerminalProps {
  terminalOutput: string;
  isDarkMode: boolean;
  onInputSubmit: (input: string) => void;
  inputMode: boolean;
}

const Terminal: React.FC<TerminalProps> = ({
  terminalOutput,
  isDarkMode,
  onInputSubmit,
  inputMode
}) => {
  const [inputValue, setInputValue] = useState('');
  const terminalEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [visibleInput, setVisibleInput] = useState<string>('');
  
  // Scroll to bottom on output change
  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    
    // Focus input field when input is needed
    if (inputMode && inputRef.current) {
      inputRef.current.focus();
    }
    
    // Reset visible input when input mode is turned off
    if (!inputMode) {
      setVisibleInput('');
    }
  }, [terminalOutput, inputMode]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputMode) {
      setVisibleInput(inputValue); 
      onInputSubmit(inputValue);
      setInputValue('');
    }
  };

  return (
    <main className={`h-full text-sm font-mono bg-transparent ${isDarkMode ? `text-white` : 'text-black'}`}>
      <div className="flex flex-col h-full px-4 py-2 overflow-hidden">
        <div className={`font-jujutsu font-semibold p-2 tracking-widest ${isDarkMode ? 'text-blue-400' : 'text-black'}`}>TERMINAL</div>

        <div className="flex-1 overflow-y-auto">
          {terminalOutput && <span className="whitespace-pre-wrap">{terminalOutput}</span>}
          
          {/* Show last submitted input when input mode was just turned off */}
          {!inputMode && visibleInput && <span>{visibleInput}</span>}
          
          {/* Show input field when in input mode */}
          {inputMode && (
            <input
              ref={inputRef}
              className="bg-transparent focus:outline-none border-none w-5/6"
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              autoFocus
            />
          )}
          
          <div ref={terminalEndRef} />
        </div>
      </div>
    </main>
  );
};

export default Terminal;