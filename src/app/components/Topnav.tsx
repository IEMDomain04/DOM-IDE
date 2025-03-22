'use client';

import React, { MutableRefObject } from 'react';
import Image from 'next/image';
import * as monaco from 'monaco-editor';

interface TopnavProps {
  onRunClick: () => void;
  onTokenizerClick: () => void;
  onSyntaxClick: () => void;
  onSemanticClick: () => void;
  toggleDarkMode: () => void;
  isDarkMode: boolean;
  codeEditorRef: MutableRefObject<monaco.editor.IStandaloneCodeEditor | null>;
}

interface FilePickerOptions {
  types: {
    description: string;
    accept: { [key: string]: string[] };
  }[];
}

export default function Topnav({ onRunClick, onTokenizerClick, onSyntaxClick, onSemanticClick, toggleDarkMode, isDarkMode, codeEditorRef }: TopnavProps) {

  const handleSaveAsClick = () => {
    const codeeditor = codeEditorRef.current;
    if (codeeditor) {
      const textContent = codeeditor.getValue();  // Get content from Monaco Editor
      const blob = new Blob([textContent], { type: 'text/plain' });

      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);

      if ('showSaveFilePicker' in window) {
        const opts = {
          types: [{
            description: 'DOM Files',
            accept: { 'text/plain': ['.dom'] },
          }],
        };

        (window as unknown as { showSaveFilePicker: (opts: FilePickerOptions) => Promise<FileSystemFileHandle> })
          .showSaveFilePicker(opts)
          .then((handle) => {
            handle.createWritable().then((writable) => {
              writable.write(blob).then(() => {
                writable.close();
              });
            });
          })
          .catch((err) => {
            console.error('Save file failed', err);
          });
      } else {
        link.download = 'code.dom';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }
  };

  const handleOpenClick = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.dom';
    input.onchange = (event) => {
      const file = (event.target as HTMLInputElement)?.files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const codeeditor = codeEditorRef.current;
          if (codeeditor) {
            const content = e.target?.result as string;
            codeeditor.setValue(content);
          }
        };
        reader.readAsText(file);
      }
    };
    input.click();
  };

  const functionButtons = [
    { name: "Save", onClick: handleSaveAsClick },
    { name: "Open", onClick: handleOpenClick },
  ];

  const compilerButtons = [
    { name: "Lexical", onClick: onTokenizerClick },
    { name: "Syntax", onClick: onSyntaxClick },
    { name: "Semantic", onClick: onSemanticClick },
  ];

  return (
    <div className='fixed top-0 w-full z-50 border-b-2 border-dark-background'>
      <div className={`flex justify-between px-10 py-3 ${isDarkMode ? 'bg-dark-foreground' : 'bg-light-foreground'}`}>

        <div className="flex gap-x-2 items-center">

          <Image src="/dom-icon.svg" width={20} height={20} alt="Dom icon" />

          <h1 className='text-xl font-jujutsu pr-5'>DOM COMPILER</h1>

          {functionButtons.map((functionButton, index) => (
            <div key={index} className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950"
              onClick={functionButton.onClick}>
              <h1 className='text-xs'>{functionButton.name}</h1>
            </div>
          ))}

          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950"
            onClick={onRunClick}>
            <Image src="/run-icon.svg" width={20} height={10} alt="Run img" />
            <h1 className='text-xs'>Run</h1>
          </div>
        </div>

        <div className="flex gap-x-5">
          {compilerButtons.map((compilerButtons, index) => (
            <div key={index} className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950"
              onClick={compilerButtons.onClick}>
              <h1 className='text-xs'>{compilerButtons.name}</h1>
            </div>
          ))}
          <Image
            className='px-1 py-1 rounded cursor-pointer hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950'
            src={isDarkMode ? "/lightmode-icon.svg" : "/darkmode-icon.svg"}
            width={25} 
            height={10}
            alt="light-dark icon"
            onClick={toggleDarkMode}
          />
        </div>
      </div>
    </div>
  );
}