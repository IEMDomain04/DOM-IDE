'use client';

import React, { useState, useRef, useEffect } from "react";
import Topnav from "./components/Topnav";
import { handleTokenizerClick } from "./lexical/lexical";
import { handleSyntaxClick } from "./syntax/syntax"; // Import the function

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

  // Function to handle the semantic button click
  const handleSemanticClick = async () => {
    setOutputData([]);
    setTerminalOutput("\n============= SEMANTIC COMING SOON ==============");
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
        <Topnav onRunClick={handleRunClick} 
                onTokenizerClick={() => textareaRef.current && handleTokenizerClick(textareaRef as React.RefObject<HTMLTextAreaElement>, setOutputData, setTerminalOutput)} 
                onSyntaxClick={() => textareaRef.current && handleSyntaxClick(textareaRef as React.RefObject<HTMLTextAreaElement>, setTerminalOutput)} 
                onSemanticClick={handleSemanticClick} toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} textareaRef={textareaRef} /> 
        {/*Text Area and Line of Numbers*/}
        <div className="flex flex-grow border border-none overflow-hidden">
          {/* Line of numbers and Textarea */}
          <div className="flex flex-grow overflow-hidden">
            {/* Line of numbers */}
            <div ref={lineNumbersRef} className={`w-fit text-right py-2 px-5 leading-6 border-r-2 border-black ${isDarkMode ? 'text-white' : 'text-black'}`} style={{ overflow: 'hidden' }}>
              {[...Array(lineCount)].map((_, i) => (
                <div key={i} className="h-6">
                  {i + 1}
                </div>
              ))}
            </div>

            {/* Textarea */}
            <textarea
              ref={textareaRef}
              className={`flex-grow text-sm leading-6 font-mono py-2 px-4 focus:outline-none focus:ring-2 focus:ring-stone-700 ${isDarkMode ? 'text-white bg-transparent' : 'text-black bg-transparent'}`}
              placeholder="Coding..."
              onChange={handleTextChange}
              onKeyDown={handleKeyDown}
              style={{ resize: 'none', borderRight: '2px solid #131314' }}
              spellCheck="false"
            ></textarea>
          </div>
        </div>

        {/* Terminal Section */}
        {terminalOutput && (
          <div className="flex-shrink-0" style={{ resize: 'none', borderRight: '2px solid #131314' }}>
            <h1 className={`py-3 px-16 ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground'}`}>Output and Errors</h1>
            <div className={`pl-4 py-2 pr-0 text-sm font-mono min-h-40 ${isDarkMode ? 'text-white' : 'text-black'}`}>
              <div className="overflow-auto" style={{ maxHeight: '120px' }}>
                <pre>{terminalOutput}</pre>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Output Table for Lexeme, Tokens */}
      {outputData.length > 0 && (
        <div className="flex flex-col w-5/12 overflow-auto" style={{ maxHeight: '100vh', position: 'relative' }}>
          <table className={`min-w-full table-fixed ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground text-white'}`}>
            <thead className={`${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground text-white'}`} style={{ position: 'sticky', top: 0, zIndex: 1 }}>
              <tr>
                <th className={`py-3 px-4 text-xl border-b-2 ${isDarkMode ? 'border-[#391d1d]' : 'border-[#242a47]'}`}>Lexeme</th>
                <th className={`py-3 px-4 text-xl border-b-2 ${isDarkMode ? 'border-[#391d1d]' : 'border-[#242a47]'}`}>Tokens</th>
              </tr>
            </thead>
            <tbody>
              {outputData.map((item, index) => (
                <tr key={index}>
                  <td className={`py-2 px-4 border-b-2 ${isDarkMode ? 'border-[#2f1919]' : 'border-[#1b1f36]'}`} title={item.lexeme}>
                    {item.lexeme && item.lexeme.length > 15 ? item.lexeme.substring(0, 12) + '...' : item.lexeme}
                  </td>
                  <td className={`py-2 px-4 border-b-2  ${isDarkMode ? 'border-[#2f1919]' : 'border-[#1b1f36]'}`}>{item.token}</td>
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