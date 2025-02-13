import React from "react";
import { Editor } from "@monaco-editor/react";
import CustomTheme from "./CustomTheme";

const CodeEditor = () => {
    return (
        <main>
            {/* Run CustomTheme setup */}
            <CustomTheme />

            {/* Monaco Editor */}
            <Editor
                className="mt-14"
                height="100vh"
                theme="customTheme"
                defaultLanguage="customLang"
                defaultValue="# code.."
            />

        </main>
    );
};

export default CodeEditor;
