import { useEffect } from "react";
import { useMonaco } from "@monaco-editor/react";

const CustomTheme = () => {
    const monaco = useMonaco();

    useEffect(() => {
        if (!monaco) return;

        // Extend JavaScript syntax highlighting
        monaco.languages.setMonarchTokensProvider("javascript", {
            tokenizer: {
                root: [
                    // Keywords 
                    [/\bexpansion\b/, "keywords"],
                    [/\bcurse\b/, "keywords"],
                    [/\bdomain\b/, "keywords"],

                    // Data Types
                    [/\bnull\b/, "data-types"],
                    [/\bint\b/, "data-types"],
                    [/\bfloat\b/, "data-types"],
                    [/\bstring\b/, "data-types"],
                    [/\bbool\b/, "data-types"],

                    // Declaration Statement
                    [/\brestrict\b/, "declaration"],
                    [/\bunsigned\b/, "declaration"],

                    // Input and Output Statements
                    [/\binvoke\b/, "io"],
                    [/\bcapture\b/, "io"],

                    // Boolean Statements
                    [/\btrue\b/, "boolean"],
                    [/\bfalse\b/, "boolean"],

                    // Condition Statements
                    [/\bvow\b/, "conditional"],
                    [/\belse\b/, "conditional"],
                    [/\bboogie\b/, "conditional"],
                    [/\bwoogie\b/, "conditional"],

                    // Looping Statements
                    [/\bcycle\b/, "loops"],
                    [/\bsustain\b/, "loops"],
                    [/\bperform\b/, "loops"],

                    // Loop Control Statements
                    [/\bdismiss\b/, "loop-control"],
                    [/\bhop\b/, "loop-control"],

                    // Return Statements
                    [/\brecall\b/, "return"],

                    // Clan Curses
                    [/\bcleave\b/, "curse"],
                    [/\bdismantle\b/, "curse"],
                ],
            },
        });

        // Define custom theme with color changes
        monaco.editor.defineTheme("customTheme", {
            base: "vs-dark",
            inherit: true,
            rules: [
                { token: "keywords", foreground: "#C19E65" }, // Keywords
                { token: "data-types", foreground: "#FFCC00" }, // Data Types
                { token: "declaration", foreground: "#00BFFF" }, // Declarations
                { token: "io", foreground: "#ffd66e" }, // Input/Output
                { token: "boolean", foreground: "#32CD32" }, // Boolean
                { token: "conditional", foreground: "#FFA500" }, // Conditionals
                { token: "loops", foreground: "#FA70F6" }, // Loops
                { token: "loop-control", foreground: "#d65e76" }, // Loop Control
                { token: "return", foreground: "#7638fc" }, // Return Statements
                { token: "curse", foreground: "#7a5c47" }, // Clan Curses
            ],
            colors: {
                'editor.background': '#181819',
            },
        });

        monaco.languages.registerCompletionItemProvider("javascript", {
            triggerCharacters: ["."], // Optional: triggers completion on typing '.'

            resolveCompletionItem: function (item) {
                return item;
            },

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
                        { label: "vow (vow)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "vow", documentation: "Defines a condition block.", range },
                        { label: "else (els)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "else", documentation: "Defines the alternative condition.", range },
                        { label: "boogie (boo)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "boogie", documentation: "Defines a specific condition.", range },
                        { label: "woogie (woo)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "woogie", documentation: "Defines an alternative condition.", range },

                        // Looping Statements
                        { label: "cycle (cyc)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "cycle", documentation: "Begins a loop cycle.", range },
                        { label: "sustain (sus)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "sustain", documentation: "Maintains a looping process.", range },
                        { label: "perform (per)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "perform", documentation: "Executes a repeated action.", range },

                        // Loop Control Statements
                        { label: "dismiss (dis)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "dismiss", documentation: "Exits a loop.", range },
                        { label: "hop (hop)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "hop", documentation: "Jumps to another part of the loop.", range },

                        // Return Statements
                        { label: "recall (rec)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "recall", documentation: "Returns a value from a function.", range },

                        // Clan Curses
                        { label: "cleave (cle)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "cleave", documentation: "Executes a destruction operation.", range },
                        { label: "dismantle (dsm)", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "dismantle", documentation: "Breaks down an entity.", range },
                    ]
                };
            }
        });

    }, [monaco]);

    return null; // This component only runs setup
};

export default CustomTheme;
