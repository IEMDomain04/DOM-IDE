import React from 'react';

interface TopnavProps {
  onRunClick: () => void;
  onTokenizerClick: () => void;
  onSyntaxClick: () => void;
  onSemanticClick: () => void;
  toggleDarkMode: () => void;
  isDarkMode: boolean;
  textareaRef: React.RefObject<HTMLTextAreaElement | null>;
  updateLineCount: (count: number) => void; // Add the new prop
}

interface FilePickerOptions {
  types: {
    description: string;
    accept: { [key: string]: string[] };
  }[];
}

export default function Topnav({ onRunClick, onTokenizerClick, onSyntaxClick, onSemanticClick, toggleDarkMode, updateLineCount, isDarkMode, textareaRef }: TopnavProps) {
  
  // Function to handle "Save As.." button click
  const handleSaveAsClick = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      const textContent = textarea.value;  // Get content from textarea
      const blob = new Blob([textContent], { type: 'text/plain' });

      // Create a temporary link element
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);

      // Use the File System Access API if available
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
        // Fallback for browsers that do not support the File System Access API
        link.download = 'code.dom';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }
  };

  // Function to handle "Open" button click
    const handleOpenClick = () => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.dom';
      input.onchange = (event) => {
        const file = (event.target as HTMLInputElement)?.files?.[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            const textarea = textareaRef.current;
            if (textarea) {
              const content = e.target?.result as string;
            textarea.value = content;
  
              // Create a new InputEvent for React's state synchronization
              const inputEvent = new Event('input', { bubbles: true, cancelable: true });
  
              // Dispatch the event
              textarea.dispatchEvent(inputEvent);
    
            // Update line count based on content
            const lines = content.split("\n").length;
            updateLineCount(lines);
          }
          };
          reader.readAsText(file);
        }
      };
      input.click();
    };

  return (
    <div className='fixed top-0 w-full z-50 border-b-2 border-dark-background'>
      {/* Top Nav */}
      <div className={`flex justify-between px-10 py-3 ${isDarkMode ? 'bg-dark-foreground' : 'bg-light-foreground'}`}>
        {/* Logo and Title of Compiler */}
        <div className="flex gap-x-2 items-center">
          <img src="/dom-icon.svg" width={20} height={20} alt="Dom icon" />
          <h1 className='text-xl font-jujutsu pr-5'>DOM COMPILER</h1>
        {/* Saves and runs */}
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950" onClick={handleSaveAsClick}>
            <h1 className='text-xs'>Save</h1>
          </div>

          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950" onClick={handleOpenClick}>
            <h1 className='text-xs'>Open</h1>
          </div>
          
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950" onClick={onRunClick}>
            <img className='h-auto w-3' src={`/run-icon.svg`} alt="" />
            <h1 className='text-xs'>Run</h1>
          </div>
        </div>

        <div className="flex gap-x-5">
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950" onClick={onTokenizerClick}>
            <h1 className='text-xs'>Tokenizer</h1>
          </div>

          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950" onClick={onSyntaxClick}>
            <h1 className='text-xs'>Syntax</h1>
          </div>
          
          <div className="flex items-center w-auto gap-x-2 px-3 py-1 rounded cursor-pointer duration-100 hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950" onClick={onSemanticClick}>
            <h1 className='text-xs'>Semantic</h1>
          </div>

          <img
            className='px-1 py-1 rounded cursor-pointer hover:bg-purple-500/50 hover:scale-110 active:bg-violet-950'
            src={isDarkMode ? "/lightmode-icon.svg" : "/darkmode-icon.svg"}
            alt="light-dark icon"
            onClick={toggleDarkMode}
          />
        </div>
      </div>
    </div>
  ); 
}
