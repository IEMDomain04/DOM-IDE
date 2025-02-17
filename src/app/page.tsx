'use client';

import Topnav from "./components/Topnav";
import CodeEditor from "./components/CodeEditor";
import React, { useState } from "react";
import { handleTokenizerClick } from "./lexical/lexical";
import Terminal from "./components/Terminal";
import { handleSyntaxClick } from "./syntax/syntax";
import { handleSemanticClick } from "./semantic/semantic";

interface Token {
  lexeme: string;
  token: string;
}

export default function Lexeme() {
  const [outputData, setOutputData] = useState<Token[]>([]); // State for table output
  const [terminalOutput, setTerminalOutput] = useState<string>(''); // State for terminal output
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [code, setCode] = useState<string>(`expansion;

curse domain(){
  invoke("Hello, World!");
}`);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
    } else {
      document.documentElement.classList.add('dark');
    }
  };

  // Function to handle the run button click
  const handleRunClick = async () => {
    setOutputData([]);
    setTerminalOutput("\n============= COMPILER COMING SOON ==============");
  };

  const SyntaxAnalyzer = async () => {
    handleSyntaxClick(code, setTerminalOutput);
  };

  const SemanticAnalyzer = async () => {
    handleSemanticClick(code, setTerminalOutput)
  };

  const Tokenizer = async () => {
    handleTokenizerClick(code, setOutputData, setTerminalOutput);
  };

  return (
    <section className={`flex w-screen h-screen ${isDarkMode ? 'dark' : ''}`} style={{ backgroundImage: `url(${isDarkMode ? '/bg-dark.png' : '/bg-light.png'})`, backgroundSize: 'cover', backgroundRepeat: 'no-repeat' }}>
      {/*Left Side: Topnav, Textarea, and Terminal */}
      <div className="flex flex-col w-full h-screen">
        <div className="relative select-auto w-auto max-h-[38rem] min-h-[10rem] box-border flex-shrink-0 resize-y overflow-hidden">
          <Topnav
            onRunClick={handleRunClick}
            onTokenizerClick={Tokenizer}
            onSyntaxClick={SyntaxAnalyzer}
            onSemanticClick={SemanticAnalyzer}
            toggleDarkMode={toggleDarkMode}
            isDarkMode={isDarkMode}
          />
          <CodeEditor value={code} onChange={setCode} isDarkMode={isDarkMode} />
        </div>

        {terminalOutput.length > 0 && (
          <Terminal terminalOutput={terminalOutput} isDarkMode={isDarkMode} />
        )}
      </div>

      {/* Output Table for Lexeme, Tokens */}
      {outputData.length > 0 && (
        <div className="flex flex-col w-3/12 overflow-auto pt-12" style={{ maxHeight: '100vh', position: 'absolute', right: 0 }}>
          <table className={`min-w-full table-fixed ${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground text-white'}`}>
            <thead className={`${isDarkMode ? 'bg-dark-foreground text-white' : 'bg-light-foreground text-white'}`} style={{ position: 'sticky', top: 0, zIndex: 1 }}>
              <tr>
                <th className={`py-3 px-4 text-xl border-b-2 ${isDarkMode ? 'border-[#391d1d]' : 'border-[#242a47]'}`}>Lexeme</th>
                <th className={`py-3 px-4 text-xl border-b-2 ${isDarkMode ? 'border-[#391d1d]' : 'border-[#242a47]'}`}>Tokens</th>
              </tr>
            </thead>
            <tbody>
              {outputData.map((item, index) => (
                <tr key={index} className={index % 2 === 0 ? isDarkMode ? 'bg-[#412121]' : 'bg-[#2d3456]' : ''}>
                  <td className={`py-2 px-4 border-b-2 ${isDarkMode ? 'border-[#412121]' : 'border-[#2C3358]'}`} title={item.lexeme}>
                    {item.lexeme && item.lexeme.length > 15 ? item.lexeme.substring(0, 12) + '...' : item.lexeme}
                  </td>
                  <td className={`py-2 px-4 border-b-2  ${isDarkMode ? 'border-[#412121]' : 'border-[#2C3358]'}`}>{item.token}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={() => setOutputData([])} className="fixed right-5 bottom-0 mb-4 ml-4 w-12 h-12 bg-purple-300/10 text-white rounded-full shadow-lg flex items-center justify-center">
            <img src="/eye.svg" alt="Hide Table" className="w-6 h-6" style={{ filter: 'invert(1)' }} />
          </button>
        </div>
      )}
    </section>
  );
}