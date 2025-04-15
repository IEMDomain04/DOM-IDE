'use client';

import React, { useState, useRef, useEffect } from "react";
import Image from "next/image";
import Topnav from "./components/Topnav";
import CodeEditor from "./components/CodeEditor";
// import { useRouter } from "next/navigation";
import { handleTokenizerClick } from "./lexical/lexical";
import { handleSyntaxClick } from "./syntax/syntax";
import { handleSemanticClick } from "./semantic/semantic";
import { handleRunClick } from "./interpreter/interpreter";
import Terminal from "./components/Terminal";
import * as monaco from 'monaco-editor';
import { io, Socket } from "socket.io-client";

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
  const codeEditorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    if (socket) {
      console.log("WebSocket connection established:", socket);
    }
  }, [socket]);

  const [inputPrompt, setInputPrompt] = useState<string | null>(null);
  const pendingInputRef = useRef<{ var_name: string } | null>(null);

  useEffect(() => {
    const socketInstance = io(
      window.location.hostname === 'localhost'
        ? 'http://127.0.0.1:5000'
        : ''
    );

    setSocket(socketInstance);

    socketInstance.on("capture_input", (data: { var_name: string }) => {
      setInputPrompt(`Enter value for ${data.var_name}:`);
      pendingInputRef.current = data;
    });

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  const handleInputSubmit = (input: string) => {
    if (socket && pendingInputRef.current) {
      socket.emit("capture_input", {
        var_name: pendingInputRef.current.var_name,
        input: input
      });

      // Append to terminal output
      setTerminalOutput(prev => prev + `\n> ${input}`);

      setInputPrompt(null);
      pendingInputRef.current = null;
    }
  };


  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
    } else {
      document.documentElement.classList.add('dark');
    }
  };

  const handleEditorDidMount = (editor: monaco.editor.IStandaloneCodeEditor) => {
    codeEditorRef.current = editor;
  };


  const Interpreter = async () => {
    setOutputData([]);
    setTerminalOutput(''); // Clears the terminal before running
    await handleRunClick(code, setTerminalOutput);
  };

  const SyntaxAnalyzer = async () => {
    handleSyntaxClick(code, setTerminalOutput);
  };

  const SemanticAnalyzer = async () => {
    handleSemanticClick(code, setTerminalOutput);
  };

  const Tokenizer = async () => {
    handleTokenizerClick(code, setOutputData, setTerminalOutput);
  };

  const [height, setHeight] = useState(400); // Initial height of the div
  const divRef = useRef<HTMLDivElement>(null);
  const dragRef = useRef<number | null>(null);

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    dragRef.current = e.clientY;
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (dragRef.current !== null) {
      const deltaY = e.clientY - dragRef.current;
      setHeight((prevHeight) => Math.max(100, prevHeight + deltaY));
      dragRef.current = e.clientY;
    }
  };

  const handleMouseUp = () => {
    dragRef.current = null;
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  };

  return (
    <section
      className={`flex w-screen h-screen font-mono ${isDarkMode ? 'dark' : ''}`}
      style={{
        backgroundImage: `url(${isDarkMode ? '/bg-dark.png' : '/bg-light.png'})`,
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
      }}
    >
      <div className="flex flex-col w-full h-full overflow-hidden bg-light-background/0 dark:bg-dark-foreground/30">

        {/* 🧭 Topnav and Editor Panel */}
        <div ref={divRef} className="relative w-full overflow-hidden flex-shrink-0" style={{ height: `${height}px` }}>
          <Topnav
            onRunClick={Interpreter}
            onTokenizerClick={Tokenizer}
            onSyntaxClick={SyntaxAnalyzer}
            onSemanticClick={SemanticAnalyzer}
            toggleDarkMode={toggleDarkMode}
            isDarkMode={isDarkMode}
            codeEditorRef={codeEditorRef}
          />
          <CodeEditor value={code} onChange={setCode} onMount={handleEditorDidMount} isDarkMode={isDarkMode} />
          <div className={`absolute bottom-0 left-0 w-full h-[6px] cursor-row-resize ${isDarkMode ? 'bg-dark-foreground' : 'bg-light-foreground'}`} onMouseDown={handleMouseDown} />
        </div>

        {/* 🖥️ Terminal Panel */}
        <div className="relative w-full" style={{ height: `calc(100vh - ${height}px)` }}>
          <div className={`absolute top-0 left-0 w-full h-[5px] cursor-row-resize ${isDarkMode ? 'bg-dark-foreground' : 'bg-light-foreground'} z-10`} onMouseDown={handleMouseDown} />
          <Terminal
            terminalOutput={terminalOutput}
            isDarkMode={isDarkMode}
            onInputSubmit={handleInputSubmit}
            inputPrompt={inputPrompt}
          />
        </div>
      </div>

      {/* 🧾 Token Table */}
      {outputData.length > 0 && (
        <div className="flex flex-col w-3/12 overflow-auto pt-12 max-sm:w-10/12" style={{ maxHeight: '100vh', position: 'absolute', right: 0, zIndex: 10 }}>
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
          <button onClick={() => setOutputData([])} className="fixed right-5 bottom-0 mb-4 ml-4 w-12 h-12 bg-purple-300/10 text-white rounded-full shadow-lg flex items-center justify-center duration-150 hover:bg-purple-300/40 hover:w-14 hover:h-14 active:bg-purple-300/10">
            <Image src="/eye.svg" alt="Hide Table" width={24} height={24} style={{ filter: 'invert(1)' }} />
          </button>
        </div>
      )}
    </section>


  );
}