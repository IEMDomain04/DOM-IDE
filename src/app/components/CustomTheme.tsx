import { useEffect } from "react";
import { useMonaco } from "@monaco-editor/react";

const CustomTheme = ({ isDarkMode }: { isDarkMode: boolean }) => {
    const monaco = useMonaco();

    useEffect(() => {
        if (!monaco) return;

        monaco.languages.register({ id: "customLang" });

        // Define syntax highlighting
        monaco.languages.setMonarchTokensProvider("customLang", {
            tokenizer: {
                root: [
                    // Keywords 
                    [/\b(expansion|curse|domain)\b/, "keywords"],

                    // Data Types
                    [/\b(null|int|float|string|bool)\b/, "data-types"],

                    // Declaration Statements
                    [/\b(restrict|unsigned)\b/, "declaration"],

                    // Input and Output Statements
                    [/\b(invoke|capture)\b/, "io"],

                    // Boolean Statements
                    [/\b(true|false)\b/, "boolean"],

                    // Condition Statements
                    [/\b(vow|else|boogie|woogie)\b/, "conditional"],

                    // Looping Statements
                    [/\b(cycle|sustain|perform)\b/, "loops"],

                    // Loop Control Statements
                    [/\b(dismiss|hop)\b/, "loop-control"],

                    // Return Statements
                    [/\b(recall)\b/, "return"],

                    // Clan Curses
                    [/\b(cleave|dismantle)\b/, "curse"],

                    // Comments (Everything after # is a comment)
                    [/#.*/, "comment"],

                    // // Multi-Line Comment
                    // [/#\$/, "comment", "@multiLineComment"],

                    // Identifiers
                    [/\b([a-zA-Z_][a-zA-Z0-9_]*)\b/, "identifier"],

                    // Operators
                    [/[+\-*/%**!&&||<><=>=]+/, "operators"],

                    // Strings with escape sequences highlighting
                    [/"/, { token: "string", next: "@string" }],
                ],

                // String handling with escape sequences highlighting
                string: [
                    [/[^\\"]+/, "string"], // Match any sequence of characters except backslash (\) or double quote (")
                    [/\\a/, "escape-sequence"], // Match alert escape sequence (\a)
                    [/\\n/, "escape-sequence"], // Match newline escape sequence (\n)
                    [/\\t/, "escape-sequence"], // Match tab escape sequence (\t)
                    [/\\\"/, "escape-sequence"], // Match escaped double quote (\")
                    [/\\./, "string.escape"], // Match any other escaped character (e.g., \b, \r, etc.)
                    [/"/, "string", "@pop"] // Match closing double quote (") and exit string mode
                ]

            },
        });

        // Define Dark Theme
        monaco.editor.defineTheme("customDarkTheme", {
            base: "vs-dark",
            inherit: true,
            rules: [
                { token: "keywords", foreground: "#C19E65" },
                { token: "data-types", foreground: "#FFCC00" },
                { token: "declaration", foreground: "#00BFFF" },
                { token: "io", foreground: "#ffd66e" },
                { token: "boolean", foreground: "#32CD32" },
                { token: "conditional", foreground: "#FFA500" },
                { token: "loops", foreground: "#FA70F6" },
                { token: "loop-control", foreground: "#d65e76" },
                { token: "return", foreground: "#819cfc" },
                { token: "curse", foreground: "#7a5c47" },
                { token: "comment", foreground: "#808080", fontStyle: "italic" },
                { token: "identifier", foreground: "#52b9e3" },
                { token: "string", foreground: "#32CD32" },
                { token: "operators", foreground: "#fa9bac" },
                { token: "escape-sequence", foreground: "#b5b1b1", fontStyle: "bold" },
            ],
            colors: {
                "editor.background": "#00000000",
            },
        });

        // Define Light Theme
        monaco.editor.defineTheme("customLightTheme", {
            base: "vs",
            inherit: true,
            rules: [
                { token: "keywords", foreground: "#0057b7", fontStyle: "bold" },
                { token: "data-types", foreground: "#a31515", fontStyle: "bold" },
                { token: "declaration", foreground: "#0451a5", fontStyle: "bold" },
                { token: "io", foreground: "#795E26", fontStyle: "bold" },
                { token: "boolean", foreground: "#008000", fontStyle: "bold" },
                { token: "conditional", foreground: "#AF00DB", fontStyle: "bold" },
                { token: "loops", foreground: "#D47300", fontStyle: "bold" },
                { token: "loop-control", foreground: "#D70040", fontStyle: "bold" },
                { token: "return", foreground: "#6C2DC7", fontStyle: "bold" },
                { token: "curse", foreground: "#808080", fontStyle: "bold" },
                { token: "comment", foreground: "#008000", fontStyle: "italic" },
                { token: "identifier", foreground: "#1F4E79", fontStyle: "bold" },
                { token: "string", foreground: "#1c612e", fontStyle: "bold" },
            ],
            colors: {
                "editor.background": "#00000000",
            },
        });


        // Intellisense for Dom Language
        monaco.languages.registerCompletionItemProvider("customLang", {
            triggerCharacters: ["."], // Optional: triggers completion on typing '.'
            provideCompletionItems: function (model, position) {
                const word = model.getWordUntilPosition(position);
                const range = new monaco.Range(
                    position.lineNumber,
                    word.startColumn,
                    position.lineNumber,
                    word.endColumn
                );

                return {
                    suggestions: [
                        { label: "expansion (exp)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "expansion;", documentation: "Defines the start of the script.", range },
                        { label: "curse (cur)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "curse", documentation: "Defines a function or domain.", range },
                        { label: "domain (dom)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "domain()", documentation: "Represents a domain definition.", range },

                        // Data Types
                        { label: "null (nul)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "null", documentation: "Represents a null value.", range },
                        { label: "int (int)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "int", documentation: "Represents an integer type.", range },
                        { label: "float (flo)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "float", documentation: "Represents a floating-point number.", range },
                        { label: "string (str)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "string", documentation: "Represents a string type.", range },
                        { label: "bool (boo)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "bool", documentation: "Represents a boolean type.", range },

                        // Declaration Statements
                        { label: "restrict (res)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "restrict", documentation: "Declares a restricted scope.", range },
                        { label: "unsigned (uns)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "unsigned", documentation: "Declares an unsigned type.", range },

                        // Input & Output Statements
                        { label: "invoke (inv)", kind: monaco.languages.CompletionItemKind.Function, insertText: "invoke();", documentation: "Calls a function.", range },
                        { label: "capture (cap)", kind: monaco.languages.CompletionItemKind.Function, insertText: "capture();", documentation: "Captures input or data.", range },

                        // Boolean Statements
                        { label: "true (tru)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "true", documentation: "Boolean true value.", range },
                        { label: "false (fal)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "false", documentation: "Boolean false value.", range },

                        // Conditional Statements
                        { label: "vow (vow)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "vow()", documentation: "Defines a condition block.", range },
                        { label: "else (els)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "else", documentation: "Defines the alternative condition.", range },
                        { label: "boogie (boog)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "boogie()", documentation: "Defines a specific condition.", range },
                        { label: "woogie (woo)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "woogie", documentation: "Defines an alternative condition.", range },
                        { label: "default", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "default", documentation: "Defines the default selection in a boogie woogie", range },

                        // Looping Statements
                        { label: "cycle (cyc)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "cycle()", documentation: "Begins a loop cycle.", range },
                        { label: "sustain (sus)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "sustain()", documentation: "Maintains a looping process.", range },
                        { label: "perform (per)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "perform", documentation: "Executes a repeated action.", range },

                        // Loop Control Statements
                        { label: "dismiss (dis)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "dismiss", documentation: "Exits a loop.", range },
                        { label: "hop (hop)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "hop", documentation: "Jumps to another part of the loop.", range },

                        // Return Statements
                        { label: "recall (rec)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "recall", documentation: "Returns a value from a function.", range },

                        // Clan Curses
                        { label: "cleave (cle)", kind: monaco.languages.CompletionItemKind.Function, insertText: "cleave", documentation: "Executes a destruction operation.", range },
                        { label: "dismantle (dsm)", kind: monaco.languages.CompletionItemKind.Function, insertText: "dismantle", documentation: "Breaks down an entity.", range },
                        { label: "len (len)", kind: monaco.languages.CompletionItemKind.Function, insertText: "len", documentation: "This will return the length of a string or array.", range },
                    ]
                };
            },
        });

        // Automatic pairs
        monaco.languages.setLanguageConfiguration("customLang", {
            autoClosingPairs: [
                { open: "{", close: "}" },
                { open: "(", close: ")" },
                { open: "[", close: "]" },
                { open: '"', close: '"' },
                { open: "'", close: "'" },
            ],
            brackets: [
                ["{", "}"],
                ["[", "]"],
                ["(", ")"],
            ],
            onEnterRules: [
                {
                    beforeText: /^\s*\{[^}]*$/,
                    action: {
                        indentAction: monaco.languages.IndentAction.Indent,
                        appendText: "",
                    },
                },
                {
                    beforeText: /^\s*\}$/,
                    action: {
                        indentAction: monaco.languages.IndentAction.Outdent,
                    },
                },
            ],
        });

        monaco.editor.setTheme("customLang");


        monaco.editor.setTheme(isDarkMode ? "customDarkTheme" : "customLightTheme");
    }, [monaco, isDarkMode]);

    return null; // This component only runs setup
};

export default CustomTheme;
