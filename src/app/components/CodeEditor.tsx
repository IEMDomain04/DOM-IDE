"use client";

import React from "react";
import dynamic from "next/dynamic";
const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });
import CustomTheme from "./CustomTheme";
import * as monaco from 'monaco-editor';

interface CodeEditorProps {
  value?: string;
  onChange?: (value: string) => void;
  onMount?: (editor: monaco.editor.IStandaloneCodeEditor) => void;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ value, onChange, onMount }) => {
  return (
    <main>
      <CustomTheme />
      <Editor
        className="mt-14"
        height="38rem"
        theme="customTheme"
        defaultLanguage="customLang"
        value={value}
        onChange={(newValue) => onChange && onChange(newValue || "")}
        onMount={(editor) => onMount && onMount(editor)}
      />
    </main>
  );
};

export default CodeEditor;