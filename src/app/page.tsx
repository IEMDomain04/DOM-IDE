'use client';

import Topnav from "./components/Topnav";
import CodeEditor from "./components/CodeEditor";
import React, { useState, useRef, useEffect } from "react";
import { handleTokenizerClick } from "./lexical/lexical";
import { handleSyntaxClick } from "./syntax/syntax"; 
import { handleSemanticClick } from "./semantic/semantic";

interface Token {
  lexeme: string;
  token: string;
}

export default function Lexeme() {
  const [lineCount, setLineCount] = useState(1);
  const [outputData, setOutputData] = useState<Token[]>([]); // State for table output
  const [terminalOutput, setTerminalOutput] = useState<string>(''); // State for terminal output
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null); // Create a reference for the line numbers container
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
    } else {
      document.documentElement.classList.add('dark');
    }
  };

  // Initial code snippet
  const initialCode = `expansion;

curse domain(){
    invoke("Hello, World!");
}`;

  const updateLineCount = (count: number) => {
    setLineCount(count);
  };

  // Handle text change and update line count based on text area's line breaks
  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const lines = e.target.value.split("\n").length;
    setLineCount(lines);
  };

  // Handle key down event to insert tab character
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (textarea) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const value = textarea.value;

        // Modify the textarea value to include a tab character
        textarea.value = value.substring(0, start) + '\t' + value.substring(end);

        // Update the selection to be after the tab character
        textarea.selectionStart = textarea.selectionEnd = start + 1;

        // Create a synthetic change event to pass to handleTextChange
        const event = new Event('input', { bubbles: true }) as unknown as React.ChangeEvent<HTMLTextAreaElement>;
        Object.defineProperty(event, 'target', { value: textarea, writable: false });
        handleTextChange(event); // Pass the synthetic event
      }
    }
  };

  // Function to handle the run button click
  const handleRunClick = async () => {
    setOutputData([]);
    setTerminalOutput("\n============= COMPILER COMING SOON ==============");
  };

  // Sync the scroll position between the textarea and line numbers container
  const handleScroll = () => {
    const textarea = textareaRef.current;
    const lineNumbers = lineNumbersRef.current;
    if (textarea && lineNumbers) {
      // Sync scroll position
      lineNumbers.scrollTop = textarea.scrollTop;
    }
  };

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.addEventListener("scroll", handleScroll);
      textarea.value = initialCode; // Set initial code
      handleTextChange({ target: textarea } as React.ChangeEvent<HTMLTextAreaElement>); // Update line count
    }

    return () => {
      if (textarea) {
        textarea.removeEventListener("scroll", handleScroll);
      }
    };
  }, []);

  return (
    <section className={`flex w-screen h-screen ${isDarkMode ? 'dark' : ''}`} style={{ backgroundImage: `url(${isDarkMode ? '/bg-dark.png' : '/bg-light.png'})`, backgroundSize: 'cover', backgroundRepeat: 'no-repeat' }}>
      {/*Left Side: Topnav, Textarea, and Terminal */}
      <div className="flex flex-col w-full h-screen">
        <Topnav
          onRunClick={handleRunClick}
          onTokenizerClick={() => textareaRef.current && handleTokenizerClick(textareaRef as React.RefObject<HTMLTextAreaElement>, setOutputData, setTerminalOutput)}
          onSyntaxClick={() => textareaRef.current && handleSyntaxClick(textareaRef as React.RefObject<HTMLTextAreaElement>, setTerminalOutput)}
          onSemanticClick={() => textareaRef.current && handleSemanticClick(textareaRef as React.RefObject<HTMLTextAreaElement>, setTerminalOutput)}
          toggleDarkMode={toggleDarkMode}
          isDarkMode={isDarkMode}
          textareaRef={textareaRef}
          updateLineCount={updateLineCount} // Pass the function as a prop
        />
        
        <CodeEditor />

        {/* Terminal Section */}
        {terminalOutput && (
          <div className="flex-shrink-0" style={{ resize: 'none', borderRight: '2px solid #131314' }}>
            <h1 className={`py-3 px-16 ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground'}`}>Output and Errors</h1>
            <div className={`pl-4 py-2 pr-0 text-sm font-mono min-h-40 ${isDarkMode ? 'text-white' : 'text-black'}`}>
              <div className="overflow-y-auto " style={{ maxHeight: '120px' }}>
                <pre className="whitespace-pre-wrap">{terminalOutput}</pre>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Output Table for Lexeme, Tokens */}
      {outputData.length > 0 && (
        <div className="flex flex-col w-5/12 overflow-auto pt-12" style={{ maxHeight: '100vh', position: 'relative' }}>
          <table className={`min-w-full table-fixed ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground text-white'}`}>
            <thead className={`${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground text-white'}`} style={{ position: 'sticky', top: 0, zIndex: 1 }}>
              <tr>
                <th className={`py-3 px-4 text-xl border-b-2 ${isDarkMode ? 'border-[#391d1d]' : 'border-[#242a47]'}`}>Lexeme</th>
                <th className={`py-3 px-4 text-xl border-b-2 ${isDarkMode ? 'border-[#391d1d]' : 'border-[#242a47]'}`}>Tokens</th>
              </tr>
            </thead>
            <tbody>
              {outputData.map((item, index) => (
              <tr key={index} className={index % 2 === 0 ? isDarkMode ? 'bg-[#412121]': 'bg-[#2d3456]' : ''}>
                <td className={`py-2 px-4 border-b-2 ${isDarkMode ? 'border-[#412121]' : 'border-[#2C3358]'}`} title={item.lexeme}>
                {item.lexeme && item.lexeme.length > 15 ? item.lexeme.substring(0, 12) + '...' : item.lexeme}
                </td>
                <td className={`py-2 px-4 border-b-2  ${isDarkMode ? 'border-[#412121]' : 'border-[#2C3358]'}`}>{item.token}</td>
              </tr>
              ))}
            </tbody>
          </table>
          <button onClick={() => setOutputData([])} className="fixed right-5 bottom-0 mb-4 ml-4 w-12 h-12  bg-purple-300/10 text-white rounded-full shadow-lg flex items-center justify-center">
            <img src="/eye.svg" alt="Hide Table" className="w-6 h-6" style={{ filter: 'invert(1)' }} />
          </button>
        </div>
      )}
    </section>
  );
}