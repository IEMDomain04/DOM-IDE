'use client';

import React, { useState, useRef, useEffect } from "react";
import axios from 'axios';
import Topnav from "./components/Topnav";

interface Token {
  lexeme: string;
  token: string;
  attribute: string;
}

export default function Lexeme() {
  const [lineCount, setLineCount] = useState(1);
  const [outputData, setOutputData] = useState<Token[]>([]); // State for table output
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
          attribute: token.value
        }));
        setOutputData(newOutputData);
      } catch (error) {
        console.error('Error:', error);
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
    <div className="flex flex-col h-screen overflow-hidden" style={{backgroundColor: '#18162d'}}>
      <Topnav onRunClick={handleRunClick} />
      <div className="flex flex-grow p-4">
        {/* Text Area Container */}
        <div className="flex flex-grow border rounded-lg overflow-hidden shadow-lg mr-4">
          {/* Line Numbers and Text Area */}
          <div className="flex flex-grow overflow-hidden">
            {/* Line Numbers */}
            <div
              ref={lineNumbersRef} 
              className="text-white text-right py-2 px-4 select-none overflow-hidden"
              style={{ minWidth: "40px", lineHeight: "1.5rem", backgroundColor: "#232146"}}
            >
              {[...Array(lineCount)].map((_, i) => (
                <div key={i} className="h-6">
                  {i + 1}
                </div>
              ))}
            </div>

            {/* Text Area */}
            <div className="flex-grow relative overflow-hidden">
              <textarea
                ref={textareaRef}  
                className="w-full h-full text-white text-sm font-mono py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500 overflow-auto" 
                style={{ resize: "none", lineHeight: "1.5rem", backgroundColor: '#232146' }}
                placeholder="Coding.."
                onChange={handleTextChange}
                onKeyDown={handleKeyDown}
              ></textarea>
            </div>
          </div>
        </div>

        {/* Output Table for Lexeme, Tokens, Attributes */}
        <div className="flex flex-col w-1/3">
          <div className="overflow-x-auto table-container" style={{ maxHeight: "calc(100vh - 100px)"  }}>
            <table className="min-w-full text-white" style={{backgroundColor: '#232146', borderRadius: "9px"}}>
              <thead style={{ backgroundColor: '#232146' }}>
                <tr>
                  <th className="py-2 px-4 border">Lexeme</th>
                  <th className="py-2 px-4 border">Tokens</th>
                  <th className="py-2 px-4 border">Attributes</th>
                </tr>
              </thead>
              <tbody>
                {outputData.map((item, index) => (
                  <tr key={index}>
                    <td className="py-2 px-4 border">{item.lexeme}</td>
                    <td className="py-2 px-4 border">{item.token}</td>
                    <td className="py-2 px-4 border">{item.attribute}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}