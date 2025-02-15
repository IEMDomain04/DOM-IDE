"use client";

import React from "react";
import dynamic from "next/dynamic";
const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });
import CustomTheme from "./CustomTheme";

const CodeEditor = () => {
    return (
        <main>
            <CustomTheme />
            <Editor
                className="mt-14"
                height="38rem"
                theme="customTheme"
                defaultLanguage="customLang"
                defaultValue="# code.."
            />
        </main>
    );
};

export default CodeEditor;
