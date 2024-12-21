'use client';  // Add this line at the top of your file

import React, { useState, useEffect, useRef } from "react";

export default function Textbox() {
  const [lineCount, setLineCount] = useState(1);
  const [outputData, setOutputData] = useState([]); // State for table output
  const textareaRef = useRef(null); // Create a reference for the textarea
  const lineNumbersRef = useRef(null); // Create a reference for the line numbers container

  // Handle text change and update line count based on text area's line breaks
  const handleTextChange = (e) => {
    const lines = e.target.value.split("\n").length;
    setLineCount(lines);

    // Example: Mocking lexeme, token, and attribute processing
    const lexeme = "sampleText"; // Replace with actual lexeme logic
    const token = "IDENTIFIER"; // Replace with actual token logic
    const attribute = "string"; // Replace with actual attribute logic

    // Add the processed data to the outputData state
    setOutputData([...outputData, { lexeme, token, attribute }]);
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
    }

    return () => {
      if (textarea) {
        textarea.removeEventListener("scroll", handleScroll);
      }
    };
  }, []); // Empty dependency array ensures this effect runs only once

  return (
    <div className="flex h-screen bg-purple-900 p-4">
      {/* Container */}
      <div className="flex flex-grow border rounded-lg overflow-hidden shadow-lg">
        {/* Line Numbers */}
        <div
          ref={lineNumbersRef}  // Attach ref here
          className="bg-purple-900 text-white text-right py-2 px-4 select-none overflow-y-hidden"
          style={{ minWidth: "40px", lineHeight: "1.5rem", maxHeight: "100%" }}
        >
          {[...Array(lineCount)].map((_, i) => (
            <div key={i} className="h-6">
              {i + 1}
            </div>
          ))}
        </div>

        {/* Text Area */}
        <div className="flex-grow relative">
          <textarea
            ref={textareaRef}  // Attach ref here
            className="w-full h-full bg-purple-900 text-white text-sm font-mono py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{ resize: "none", lineHeight: "1.5rem" }}
            placeholder="Coding.."
            onChange={handleTextChange}
          ></textarea>
        </div>
      </div>

      {/* Output Table for Lexeme, Tokens, Attributes */}
      <div className="mt-4 overflow-x-auto">
        <table className="min-w-full bg-purple-900 text-white border-collapse">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b">Lexeme</th>
              <th className="py-2 px-4 border-b">Tokens</th>
              <th className="py-2 px-4 border-b">Attributes</th>
            </tr>
          </thead>
          <tbody>
            {outputData.map((item, index) => (
              <tr key={index}>
                <td className="py-2 px-4 border-b">{item.lexeme}</td>
                <td className="py-2 px-4 border-b">{item.token}</td>
                <td className="py-2 px-4 border-b">{item.attribute}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
