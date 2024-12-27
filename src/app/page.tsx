'use client';

import React, { useState, useRef, useEffect } from "react";
import axios from 'axios';
import Topnav from "./components/Topnav";

interface Token {
  lexeme: string;
  token: string;
}

export default function Lexeme() {
  const [lineCount, setLineCount] = useState(1);
  const [outputData, setOutputData] = useState<Token[]>([]); // State for table output
  const [terminalOutput, setTerminalOutput] = useState<string>(''); // State for terminal output
  const textareaRef = useRef<HTMLTextAreaElement>(null); // Create reference for the textarea
  const lineNumbersRef = useRef<HTMLDivElement>(null); // Create a reference for the line numbers container

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
    const textarea = textareaRef.current;
    if (textarea) {
      const text = textarea.value;
      console.log('Sending request to /api/run with text:', text); // Add logging
      try {
        const response = await axios.post('/api/run', { text }); // Use relative URL
        console.log('Response from /api/run:', response.data); // Add logging
        const { tokens } = response.data;
        const newOutputData = tokens.map((token: { type: string; value: string }) => ({
          lexeme: token.value,
          token: token.type,
        }));
        setOutputData(newOutputData);
        setTerminalOutput(''); // Clear terminal output if no error
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          console.error('Error:', error.response.data.error);
          setTerminalOutput(error.response.data.error); // Set terminal output to error message
        } else {
          console.error('Error:', error);
          setTerminalOutput('An unexpected error occurred.');
        }
      }
    }
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
    <section className="flex">
      {/*Left Side: Topnav, Textarea, and Terminal */}
      <div className="flex flex-col w-full h-screen">
        <Topnav onRunClick={handleRunClick} />

        {/*Text Area and Line of Numbers*/}
        <div className="flex flex-grow border border-none">

          {/*Line of numbers */}
          <div ref={lineNumbersRef} className="w-fit text-right py-2 px-5 leading-6 border-r-2 border-black" style={{ background: '#181819' }}>
            {[...Array(lineCount)].map((_, i) => (
              <div key={i} className="h-6">
                {i + 1}
              </div>
            ))}
          </div>

          <textarea
            ref={textareaRef}
            className="flex-grow text-sm leading-6 font-mono py-2 px-4 focus:outline-none focus:ring-2 focus:ring-stone-700" 
            style={{ background: '#181819' }}
            placeholder="Coding..."
            onChange={handleTextChange}
            onKeyDown={handleKeyDown}
          ></textarea>
        </div>

        {/* Terminal Section */}
        <div className="">
          <h1 className="py-3 px-16" style={{ background: '#391D1D' }}>Output and Errors</h1>
          <div className="p-4 text-sm font-mono min-h-40" style={{ background: '#181819' }}>
            <div className="overflow-auto" style={{ maxHeight: '120px' }}>
              <pre>{terminalOutput || 'Your terminal output will appear here...'}</pre>
            </div>
          </div>
        </div>

      </div>

      {/* Output Table for Lexeme, Tokens */}
      <div className="flex flex-col w-1/3">
        <table className="min-w-full" style={{ backgroundColor: '#232146'}}>
          <thead style={{
            backgroundColor: '#181819'
          }}>
            <tr>
              <th className="py-3 px-4 text-xl">Lexeme</th>
              <th className="py-3 px-4 text-xl">Tokens</th>
            </tr>
          </thead>
          <tbody>
            {outputData.map((item, index) => (
              <tr key={index}>
                <td className="py-2 px-4 border">{item.lexeme}</td>
                <td className="py-2 px-4 border">{item.token}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}