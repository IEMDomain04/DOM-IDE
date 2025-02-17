"use client";

import React from "react";
import dynamic from "next/dynamic";
const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });
import CustomTheme from "./CustomTheme";
import { editor } from 'monaco-editor';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  isDarkMode: boolean;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ value, onChange, isDarkMode }) => {
  return (
    <main>
      <CustomTheme />
      <Editor
        className="mt-14"
        height="38rem"
        theme="customTheme"
        defaultLanguage="customLang"
        value={value}
        onChange={(newValue) => onChange(newValue || "")}
      />
    </main>
  );
};

export default CodeEditor;