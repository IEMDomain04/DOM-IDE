##############
# IMPORTS
##############
from lexer import run as lexer_run
from lexer import string_with_arrows 
from semantic import semantic_run

############## 
# CONSTANTS 
##############


CFG = {
    "<program>": [              
        ["expansion", ";", "<program_tail>"] ########### 1 
    ],
    "<program_tail>": [           
        ["<global>", "<program_tail>"],
        []
    ],
    
    "<global>": [
        ["<datatype>", "<curse_or_var>"], ########### 
        ["curse", "<init_void_curse>"], ###########
        ["restrict", "<datatype>", "id", "<type_choice>"], ###########
    ],

    "<curse_or_var>": [
        ["curse", "id", "<nonvoid_curse_dec>"],
        ["id", "<type_choice>"]
    ],

    # "<restrict>": [
    #     ["restrict"], ###########
    #     []  
    # ], 

    "<nonvoid_curse_dec>": [
        ["(", "<param>", ")", "{", "<body>", "}"], ########### 31
    ],

    "<type_choice>": [
        ["<var_dec>", ";"], ########### 
        ["<clan_dec>", ";"], ###########    
        [";"]
    ],

    "<var_dec>": [
        ["<assign>", "<multi-assign>"], ########### 
    ],

    "<assign>": [
        ["=", "<expression>"], ########### 
        []
    ],

    "<multi-assign>": [
        [",", "id", "<assign>", "<multi-assign>"],  ########### 29
        []                                   ########### 30
    ],

    "<init_void_curse>": [
        ["id", "(", "<param>", ")", "{", "<body>", "}"],
        ["domain", "(", ")", "{", "<body>", "}"]
    ],

    "<param>": [
        ["<datatype>", "id", "<more_param>"],
        []
    ],  

    "<more_param>": [
        [",", "<datatype>", "id", "<more_param>"],
        []
    ],

    "<clan_dec>": [
        ["<clan_size>", "<clan_assign>"]    ########### 
    ],

    "<clan_size>": [
        ["[", "<expression>", "]", "<two_dimensional>"],  
        ["[...]"]  
    ],

    "<two_dimensional>": [
        ["[", "<expression>", "]"], ########### 46
        []                                   ########### 47
    ],

    "<clan_assign>": [
        ["=", "<clan_literal>"],                ########### 48
        []                                   ########### 49
    ],

    "<clan_literal>": [
        ["{", "<clan_item>", "}"],               ########### 50
        ["dismantle", "(", "<arguments>", ")"],
        ["cleave", "(", "<arguments>", ")"]
    ],

    "<clan_item>": [
        ["<expression>", "<clan_multi_item>", "<clan_item>"],  ########### 51
        ["{", "<expression>", "<clan_multi_item>", "}", "<more_item>"],  ########### 52
        []                                   ########### 53
    ],

    "<more_item>": [                            
        [",", "<clan_item>"],                   ########### 54
        []                                   ########### 55
    ],

    "<clan_multi_item>": [      
        [",", "<expression>", "<clan_multi_item>"],########### 56
        []                                   ########### 57
    ],

    "<expression>": [
        ["(", "<expression>", "<more_logic>", ")", "<more_logic>"],
        ["<operand>","<more_logic>"],
        ["<not_op>", "<expression>", "<more_logic>"]
    ],

    "<operand>": [
        ["<pre>", "<value>"],
        ["<value>", "<post>"],
        ["<not_op>", "<value>"]
    ],

    "<more_logic>": [
        ["<operator>", "<expression>"],
        []
    ],

    "<value>": [
        ["<literal>"],
        ["id", "<curse_or_clan>"],
        ["<invoke>", "(","<arguments>",")"],
        ["capture", "(", "id", ")"],
        ["cleave", "(", "<arguments>", ")"],
        ["dismantle", "(", "<arguments>", ")"],
        ["len", "(", "<arguments>", ")"],
    ],

    "<curse_or_clan>": [
        ["(", "<arguments>", ")"],
        ["[", "<expression>", "]", "<more_clan>"],
        []
    ],

    "<more_clan>": [    
        ["[", "<expression>", "]", "<more_clan>"],
        []
    ],

    "<operator>": [
        ["<arith_op>"],
        ["<relational_op>"],
        ["<logic_op>"]
    ],

    "<body>": [               
        ["<statement>", "<body>"],          ########### 4
        []                                      ########### 5
    ],

    "<statement>": [
        ["<local>"],                ###########
        ["id", "<id_call>", ";"],            ###########
        ["invoke", "(", "<arguments>", ")", ";"], ###########
        ["cleave", "(", "<arguments>", ")", ";"],    ###########
        ["dismantle", "(", "<arguments>", ")", ";"], ###########
        ["capture", "(", "id", ")", ";"],    ###########
        ["len", "(", "<arguments>", ")", ";"],    ###########
        ["<recall_stm>"],        ###########
        ["<conditional_stm>"],            ###########
        ["<looping_stm>"],                ###########
        []

    ],

    "<local>": [
        ["<datatype>", "<curse_or_var>"], ###########
        ["curse", "<local_void_curse>"], ###########
        ["restrict", "<datatype>", "id", "<type_choice>"] ###########
    ],

    "<local_void_curse>": [
        ["id", "(", "<param>", ")", "{", "<body>", "}"], ###########
    ],

    "<recall_stm>": [
        ["recall", "<recall_val>", ";"],
    ],

    "<recall_val>": [
        ["<expression>"],
        []
    ],

    "<id_call>": [
        ["<assign_op>", "<expression>"], ###########
        ["[", "<expression>", "]", "<two_dimensional>", "<assign_op>", "<expression>"], ###########
        ["(", "<arguments>", ")"], ###########
        ["++"], 
        ["--"], 
    ],

    "<arguments>": [
        ["<expression>", "<more_arguments>"], ###########
        []
    ],

    "<more_arguments>": [
        [",", "<arguments>"], ###########
        []
    ],

    "<conditional_stm>": [
        ["<vow_statement>"], ###########
        ["boogie", "<boogie_tail>"] ###########
    ],

    "<vow_statement>": [
        ["vow", "(", "<expression>", ")", "{", "<con_loop_body>", "}", "<vow_next>"], ###########
    ],

    "<vow_next>": [
        ["else", "<vow_tail>"],
        []
    ],

    "<vow_tail>": [
        ["{", "<con_loop_body>", "}",],
        ["vow", "(", "<expression>", ")", "{", "<con_loop_body>", "}", "<vow_next>"],
        []
    ],

    "<boogie_tail>": [
        ["(", "id", ")", "{", "woogie", "<literal>", ":", "<con_loop_body>", "<more_woogie>", "default", ":", "<con_loop_body>", "}"],
        ["{", "woogie", "<expression>", ":", "<con_loop_body>", "<more_true_woogie>", "default", ":", "<con_loop_body>", "}"],
    ],

    "<more_woogie>": [
        ["woogie", "<literal>", ":", "<con_loop_body>", "<more_woogie>"],
        []
    ],

    "<more_true_woogie>": [
        ["woogie", "(", "<expression>", ")", ":", "<con_loop_body>", "<more_true_woogie>"],
        []
    ],

    "<looping_stm>": [
        ["<cycle-loop>"],
        ["<sustain-loop>"],
        ["<persustain-loop>"]
    ],

    "<cycle-loop>": [
        ["cycle", "(", "<cycle_initialize>", ";", "<cycle_condition>", ";", "<iteration>", ")", "{", "<con_loop_body>", "}"]
    ],

    "<cycle_initialize>": [
        ["id", "<id_call>"],
        ["<datatype>", "id", "=", "<expression>"]
    ],

    "<cycle_condition>": [
        ["<expression>"]
    ],

    "<iteration>": [
        ["<pre>", "id"],
        ["id", "<iteration_tail>"]
    ],

    "<iteration_tail>": [
        ["++"],
        ["--"],
        ["<assign_op>", "<ite_val>"]
    ],

    "<ite_val>": [
        ["id", "<val_tail>"],
        ["int_literal"],
        ["float_literal"]
    ],

    "<val_tail>": [
        ["<arith_op>", "<ite_val>"],
        []
    ],

    "<sustain-loop>": [
        ["sustain", "(", "<expression>", ")", "{", "<con_loop_body>", "}"]
    ],

    "<persustain-loop>": [
        ["perform", "{", "<con_loop_body>", "}", "sustain", "(", "<expression>", ")", ";"]
    ],

    "<con_loop_body>": [
        ["<local>", "<con_loop_body>"],                            ########### 0
        ["id", "<id_call>", ";", "<con_loop_body>"],                   ########### 1
        ["invoke", "(", "<arguments>", ")", ";", "<con_loop_body>"],   ########### 2
        ["cleave", "(", "<arguments>", ")", ";", "<con_loop_body>"],   ########### 3
        ["dismantle", "(", "<arguments>", ")", ";", "<con_loop_body>"],########### 4
        ["capture", "(", "id", ")", ";", "<con_loop_body>"],           ########### 5
        ["len", "(", "<arguments>", ")", ";", "<con_loop_body>"],      ########### 6
        ["<recall_stm>", "<con_loop_body>"],                           ########### 7 
        ["<conditional_stm>", "<con_loop_body>"],                      ###########
        ["<looping_stm>", "<con_loop_body>"],                          ###########
        ["dismiss", ";", "<con_loop_body>"],                            ###########
        ["hop", ";", "<con_loop_body>"],                               ###########
        []
    ], 

    "<literal>": [
        ["int_literal"],                            ########### 
        ["float_literal"],                          ########### 228
        ["string_literal"],                         ########### 226
        ["bool_literal"],                           ########### 227
        ["null_literal"],                           ########### 229
    ],

    "<datatype>": [
        ["int"],                                    ########### 254
        ["float"],                                  ########### 255
        ["string"],                                 ########### 256
        ["bool"]                                    ########### 257 
    ],

    "<arith_op>": [
        ["+"],                                      ########### 
        ["-"],                                      ########### 
        ["*"],                                      ########### 
        ["/"],                                      ########### 
        ["%"],                                      ########### 
        ["**"]                                      ########### 
    ],

    "<relational_op>": [
        ["=="],                                     ########### 
        ["!="],                                     ########### 
        [">"],                                      ###########
        ["<"],                                      ###########
        [">="],                                     ########### 
        ["<="]                                      ########### 
    ],

    "<logic_op>": [
        ["&&"],                                     ########### 
        ["||"],                                     ########### 
    ],

    "<not_op>": [
        ["!"],                                      ###########
    ],

    "<more_not_op>": [
        ["!"],                                      ###########
        []                                          ###########
    ],

    "<assign_op>": [
        ["="],                                      ###########
        ["+="],                                     ###########
        ["-="],                                     ###########
        ["*="],                                     ###########
        ["/="],                                     ###########
        ["%="]                                      ###########
    ],

    "<pre>": [
        ["++"],                                     ########### 
        ["--"],                                     ########### 
        ["-"]
    ],

    "<post>": [
        ["++"],                                     ########### 239
        ["--"],                         ########### 240
        []
    ],



    
}

PREDICT_SET = {
    "<program>": { ############# verified
        "expansion": ["<program>", 0]
    },

    "<program_tail>": { ############# verified
        "int": ["<program_tail>", 0],
        "float": ["<program_tail>", 0],
        "string": ["<program_tail>", 0],
        "bool": ["<program_tail>", 0],    
        "curse": ["<program_tail>",0],
        "restrict": ["<program_tail>", 0],
        "λ": ["<program_tail>", 1]
    }, 

    "<global>": { ############# verified
        "int": ["<global>", 0],
        "float": ["<global>", 0],
        "string": ["<global>", 0],
        "bool": ["<global>", 0],
        "curse": ["<global>", 1],
        "restrict": ["<global>", 2]
    },

    "<curse_or_var>": { ############# verified
        "curse": ["<curse_or_var>", 0],
        "id": ["<curse_or_var>", 1]
    },
 
    "<nonvoid_curse_dec>": { ############# verified
        "(": ["<nonvoid_curse_dec>", 0]
    },

    "<type_choice>": { ############# verified
        "=": ["<type_choice>", 0],
        ",": ["<type_choice>", 0],
        "[": ["<type_choice>", 1],
        "[...]": ["<type_choice>", 1],
        ";": ["<type_choice>", 2]
    },

    "<var_dec>": {  ############# verified
        "=": ["<var_dec>", 0],
        "," : ["<var_dec>", 0],
    },

    "<assign>": { ############# verified
        "=": ["<assign>", 0],
        ",": ["<assign>", 1],
        ";": ["<assign>", 1]
    },

    "<multi-assign>": { ############# verified
        ",": ["<multi-assign>", 0],
        ";": ["<multi-assign>", 1],
    },
    
    "<init_void_curse>": { ############# verified
        "id": ["<init_void_curse>", 0],
        "domain": ["<init_void_curse>", 1]
    },

    "<param>": { ############# verified
        "int": ["<param>", 0],
        "float": ["<param>", 0],
        "string": ["<param>", 0],
        "bool": ["<param>", 0],
        ")": ["<param>", 1],
    },

    "<more_param>": { ############# verified
        ",": ["<more_param>", 0],
        ")": ["<more_param>", 1],
    },

    "<clan_dec>": { ############# verified
        "[": ["<clan_dec>", 0],
        "[...]": ["<clan_dec>", 0]
    },

    "<clan_size>": { ############# verified
        "[": ["<clan_size>", 0],
        "[...]": ["<clan_size>", 1]
    },
    
    "<two_dimensional>": { ############# verified
        "[": ["<two_dimensional>", 0],
        "=": ["<two_dimensional>", 1],
        ";": ["<two_dimensional>", 1],
        '+=': ["<two_dimensional>", 1],
        '-=': ["<two_dimensional>", 1],
        '*=': ["<two_dimensional>", 1],
        '/=': ["<two_dimensional>", 1],
        '%=': ["<two_dimensional>", 1],
    },

    "<clan_assign>": { ############# verified
        "=": ["<clan_assign>", 0],
        "λ": ["<clan_assign>", 1],
        ";": ["<clan_assign>", 1]
    },

    "<clan_literal>": { ############# verified
        "{": ["<clan_literal>", 0],
        "dismantle": ["<clan_literal>", 1],
        "cleave": ["<clan_literal>", 2]
    },

    "<clan_item>": { ############# verified
        "(": ["<clan_item>", 0],
        "id": ["<clan_item>", 0],
        "int_literal": ["<clan_item>", 0],
        "string_literal": ["<clan_item>", 0],
        "bool_literal": ["<clan_item>", 0],
        "float_literal": ["<clan_item>", 0],
        "null_literal": ["<clan_item>", 0],
        "++": ["<clan_item>", 0],
        "--": ["<clan_item>", 0],
        "invoke": ["<clan_item>", 0],
        "capture": ["<clan_item>", 0],
        "cleave": ["<clan_item>", 0],
        "dismantle": ["<clan_item>", 0],
        "len": ["<clan_item>", 0],
        "!": ["<clan_item>", 0],
        "-": ["<clan_item>", 0],
        "{": ["<clan_item>", 1],
        "}": ["<clan_item>", 2]
    },

    "<more_item>": { ############# verified
        ",": ["<more_item>", 0],
        "}": ["<more_item>", 1]
    },

    "<clan_multi_item>": { ############# verified
        ",": ["<clan_multi_item>", 0],
        "(" : ["<clan_multi_item>", 1],
        "id": ["<clan_multi_item>", 1],
        "int_literal": ["<clan_multi_item>", 1],
        "string_literal": ["<clan_multi_item>", 1],
        "bool_literal": ["<clan_multi_item>", 1],
        "float_literal": ["<clan_multi_item>", 1],
        "null_literal": ["<clan_multi_item>", 1],
        "++": ["<clan_multi_item>", 1],
        "--": ["<clan_multi_item>", 1],
        "invoke": ["<clan_multi_item>", 1],
        "capture": ["<clan_multi_item>", 1],
        "cleave": ["<clan_multi_item>", 1],
        "dismantle": ["<clan_multi_item>", 1],
        "len": ["<clan_multi_item>", 1],
        "!": ["<clan_multi_item>", 1],
        "{": ["<clan_multi_item>", 1],
        "}": ["<clan_multi_item>", 1]
    },

    "<expression>": { ############# verified
        "(": ["<expression>", 0],
        "id": ["<expression>", 1],
        "int_literal": ["<expression>", 1],
        "string_literal": ["<expression>", 1],
        "bool_literal": ["<expression>", 1],
        "float_literal": ["<expression>", 1],
        "null_literal": ["<expression>", 1],
        "++": ["<expression>", 1],
        "--": ["<expression>", 1],
        "invoke": ["<expression>", 1],
        "capture": ["<expression>", 1],
        "cleave": ["<expression>", 1],
        "dismantle": ["<expression>", 1],
        "len": ["<expression>", 1],
        "-": ["<expression>", 1],
        "!": ["<expression>", 2]
    },

    "<operand>": { ############# verified
        "++": ["<operand>", 0],
        "--": ["<operand>", 0],
        "-": ["<operand>", 0],
        "id": ["<operand>", 1],
        "string_literal": ["<operand>", 1],
        "float_literal": ["<operand>", 1],
        "null_literal": ["<operand>", 1],
        "bool_literal": ["<operand>", 1],
        "int_literal": ["<operand>", 1],
        "dismantle": ["<operand>", 1],
        "capture": ["<operand>", 1],
        "invoke": ["<operand>", 1],
        "cleave": ["<operand>", 1],
        "len": ["<operand>", 1],
        "!": ["<operand>", 2],
    },

    "<value>": { ############# verified
        "string_literal": ["<value>", 0],
        "float_literal": ["<value>", 0],
        "null_literal": ["<value>", 0],
        "bool_literal": ["<value>", 0],
        "int_literal": ["<value>", 0],
        "id": ["<value>", 1],
        "invoke": ["<value>", 2],
        "capture": ["<value>", 3],
        "cleave": ["<value>", 4],
        "dismantle": ["<value>", 5],
        "len": ["<value>", 6],
    },

    "<curse_or_clan>": { ############# verified
        "(" : ["<curse_or_clan>", 0],
        "[": ["<curse_or_clan>", 1],
        ",": ["<curse_or_clan>", 2],
        ";": ["<curse_or_clan>", 2],
        "]": ["<curse_or_clan>", 2],
        ")": ["<curse_or_clan>", 2],
        "id": ["<curse_or_clan>", 2],
        "int_literal": ["<curse_or_clan>", 2],
        "string_literal": ["<curse_or_clan>", 2],
        "bool_literal": ["<curse_or_clan>", 2],
        "float_literal": ["<curse_or_clan>", 2],
        "null_literal": ["<curse_or_clan>", 2],
        "++": ["<curse_or_clan>", 2],
        "--": ["<curse_or_clan>", 2],
        "invoke": ["<curse_or_clan>", 2],
        "capture": ["<curse_or_clan>", 2],
        "cleave": ["<curse_or_clan>", 2],
        "dismantle": ["<curse_or_clan>", 2],
        "len": ["<curse_or_clan>", 2],
        "!": ["<curse_or_clan>", 2],
        "{": ["<curse_or_clan>", 2],
        "}": ["<curse_or_clan>", 2],
        "+": ["<curse_or_clan>", 2],
        "-": ["<curse_or_clan>", 2],
        "*": ["<curse_or_clan>", 2],
        "**": ["<curse_or_clan>", 2],
        "/": ["<curse_or_clan>", 2],
        "%": ["<curse_or_clan>", 2],
        "==": ["<curse_or_clan>", 2],
        "!=": ["<curse_or_clan>", 2],
        ">": ["<curse_or_clan>", 2],
        "<": ["<curse_or_clan>", 2],
        ">=": ["<curse_or_clan>", 2],
        "<=": ["<curse_or_clan>", 2],
        "&&": ["<curse_or_clan>", 2],
        "||": ["<curse_or_clan>", 2],
        ":" : ["<curse_or_clan>", 2]
    },

    "<more_clan>": { ############# verified
        "[": ["<more_clan>", 0],
        "," : ["<more_clan>", 1],
        ";": ["<more_clan>", 1],
        "]": ["<more_clan>", 1],
        "(" : ["<more_clan>", 1],
        ")": ["<more_clan>", 1],
        "id": ["<more_clan>", 1],
        "int_literal": ["<more_clan>", 1],
        "string_literal": ["<more_clan>", 1],
        "bool_literal": ["<more_clan>", 1],
        "float_literal": ["<more_clan>", 1],
        "null_literal": ["<more_clan>", 1],
        "++": ["<more_clan>", 1],
        "--": ["<more_clan>", 1],
        "invoke": ["<more_clan>", 1],
        "capture": ["<more_clan>", 1],
        "cleave": ["<more_clan>", 1],
        "dismantle": ["<more_clan>", 1],
        "len": ["<more_clan>", 1],
        "!": ["<more_clan>", 1],
        "{": ["<more_clan>", 1],
        "}": ["<more_clan>", 1],
        "+": ["<more_clan>", 1],
        "-": ["<more_clan>", 1],
        "*": ["<more_clan>", 1],
        "**": ["<more_clan>", 1],
        "/": ["<more_clan>", 1],
        "%": ["<more_clan>", 1],
        "==": ["<more_clan>", 1],
        "!=": ["<more_clan>", 1],
        ">": ["<more_clan>", 1],
        "<": ["<more_clan>", 1],
        ">=": ["<more_clan>", 1],
        "<=": ["<more_clan>", 1],
        "&&": ["<more_clan>", 1],
        "||": ["<more_clan>", 1],
        ":" : ["<more_clan>", 1]
    },

    "<more_logic>": { ############ Not sure if ambiguous
        "+": ["<more_logic>", 0], 
        "-": ["<more_logic>", 0], 
        "*": ["<more_logic>", 0], 
        "/": ["<more_logic>", 0], 
        "%": ["<more_logic>", 0], 
        "**": ["<more_logic>", 0], 
        "==": ["<more_logic>", 0], 
        "!=": ["<more_logic>", 0], 
        ">": ["<more_logic>", 0], 
        "<": ["<more_logic>", 0], 
        ">=": ["<more_logic>", 0], 
        "<=": ["<more_logic>", 0], 
        "&&": ["<more_logic>", 0], 
        "||": ["<more_logic>", 0], 
        "!": ["<more_logic>", 0], 
        ")": ["<more_logic>", 1],  
        ",": ["<more_logic>", 1], 
        "(": ["<more_logic>", 1],  
        "}": ["<more_logic>", 1],
        ";": ["<more_logic>", 1], 
        ":": ["<more_logic>", 1], 
        "]": ["<more_logic>", 1],
        ":": ["<more_logic>", 1],
        ",": ["<more_logic>", 1],
        "id": ["<more_logic>", 1],
        "int_literal": ["<more_logic>", 1],
        "string_literal": ["<more_logic>", 1],
        "bool_literal": ["<more_logic>", 1],
        "float_literal": ["<more_logic>", 1],
        "null_literal": ["<more_logic>", 1],
        "++": ["<more_logic>", 1],
        "--": ["<more_logic>", 1],
        "invoke": ["<more_logic>", 1],
        "capture": ["<more_logic>", 1],
        "cleave": ["<more_logic>", 1],
        "dismantle": ["<more_logic>", 1],
        "len": ["<more_logic>", 1]
    },

    "<operator>": { ############# verified
        "+": ["<operator>", 0],
        "-": ["<operator>", 0],
        "*": ["<operator>", 0],
        "**": ["<operator>", 0],
        "/": ["<operator>", 0],
        "%": ["<operator>", 0],
        "==": ["<operator>", 1],
        "!=": ["<operator>", 1],
        ">": ["<operator>", 1],
        "<": ["<operator>", 1],
        ">=": ["<operator>", 1],
        "<=": ["<operator>", 1],
        "&&": ["<operator>", 2],
        "||": ["<operator>", 2],
        "!": ["<operator>", 2],
    },

    "<body>": { ############# verified
        "int": ["<body>", 0],
        "string": ["<body>", 0],
        "float": ["<body>", 0],
        "bool": ["<body>", 0],
        "curse": ["<body>", 0],
        "id": ["<body>", 0],
        "invoke": ["<body>", 0],
        "capture": ["<body>", 0],
        "vow": ["<body>", 0],
        "boogie": ["<body>", 0],
        "cycle": ["<body>", 0],
        "sustain": ["<body>", 0],
        "perform": ["<body>", 0],
        "recall": ["<body>", 0],
        "restrict": ["<body>", 0],
        "}": ["<body>", 1],
        "λ": ["<body>", 1]
    },
        
    "<statement>": { ############# verified
        "int": ["<statement>", 0],
        "string": ["<statement>", 0],
        "float": ["<statement>", 0],
        "bool": ["<statement>", 0],
        "curse": ["<statement>", 0],
        "restrict": ["<statement>", 0],
        "id": ["<statement>", 1],
        "invoke": ["<statement>", 2],
        "cleave": ["<statement>", 3],
        "dismantle": ["<statement>", 4],
        "capture": ["<statement>", 5],
        "len": ["<statement>", 6],
        "recall": ["<statement>", 7],
        "vow": ["<statement>", 8],
        "boogie": ["<statement>", 8],
        "cycle": ["<statement>", 9],
        "sustain": ["<statement>"   , 9],
        "perform": ["<statement>", 9],
        "}": ["<statement>", 10],
        "λ": ["<statement>", 10]
    },

    "<local>": { ############# verified
        "int": ["<local>", 0],
        "float": ["<local>", 0],
        "string": ["<local>", 0],
        "bool": ["<local>", 0],
        "curse": ["<local>", 1],
        "restrict": ["<local>", 2]
    },

    "<local_void_curse>": { ############# verified
        "id": ["<local_void_curse>", 0]
    },

    "<recall_stm>": { ############# verified
        "recall": ["<recall_stm>", 0],
    },

    "<recall_val>": { ############# verified
        "(" : ["<recall_val>", 0],
        "id": ["<recall_val>", 0],
        "int_literal": ["<recall_val>", 0],
        "string_literal": ["<recall_val>", 0],
        "bool_literal": ["<recall_val>", 0],
        "float_literal": ["<recall_val>", 0],
        "null_literal": ["<recall_val>", 0],
        "++": ["<recall_val>", 0],
        "--": ["<recall_val>", 0],
        "invoke": ["<recall_val>", 0],
        "capture": ["<recall_val>", 0],
        "cleave": ["<recall_val>", 0],
        "dismantle": ["<recall_val>", 0],
        "len": ["<recall_val>", 0],
        "!": ["<recall_val>", 0],
        "-": ["<recall_val>", 0],
        ";": ["<recall_val>", 1]
    },

    "<id_call>": { ############# verified
        "=": ["<id_call>", 0],
        "+=": ["<id_call>", 0],
        "-=": ["<id_call>", 0],
        "*=": ["<id_call>", 0],
        "/=": ["<id_call>", 0],
        "%=": ["<id_call>", 0],
        "[": ["<id_call>", 1],
        "(": ["<id_call>", 2],
        "++": ["<id_call>", 3],
        "--": ["<id_call>", 4]
    },

    "<arguments>": { ############# verified
        "(" : ["<arguments>", 0],
        "id": ["<arguments>", 0],
        "int_literal": ["<arguments>", 0],
        "string_literal": ["<arguments>", 0],
        "bool_literal": ["<arguments>", 0],
        "float_literal": ["<arguments>", 0],
        "null_literal": ["<arguments>", 0],
        "++": ["<arguments>", 0],
        "--": ["<arguments>", 0],
        "invoke": ["<arguments>", 0],
        "capture": ["<arguments>", 0],
        "cleave": ["<arguments>", 0],
        "dismantle": ["<arguments>", 0],
        "len": ["<arguments>", 0],
        "!": ["<arguments>", 0],
        "-": ["<arguments>", 0],
        ")": ["<arguments>", 1]
    },

    "<more_arguments>": { ############# verified
        ",": ["<more_arguments>", 0],
        ")": ["<more_arguments>", 1]
    },

    "<conditional_stm>": { ############# verified
        "vow": ["<conditional_stm>", 0],
        "boogie": ["<conditional_stm>", 1]
    },

    "<vow_statement>": { ############# verified
        "vow": ["<vow_statement>", 0]
    },

    "<vow_next>": { ############# verified
        "else": ["<vow_next>", 0],
        "int": ["<vow_next>", 1],
        "string": ["<vow_next>", 1],
        "float": ["<vow_next>", 1],
        "bool": ["<vow_next>", 1],
        "curse": ["<vow_next>", 1],
        "id": ["<vow_next>", 1],
        "invoke": ["<vow_next>", 1],
        "cleave": ["<vow_next>", 1],
        "dismantle": ["<vow_next>", 1],
        "capture": ["<vow_next>", 1],
        "len": ["<vow_next>", 1],
        "recall": ["<vow_next>", 1],
        "vow": ["<vow_next>", 1],
        "boogie": ["<vow_next>", 1],
        "cycle": ["<vow_next>", 1],
        "sustain": ["<vow_next>", 1],
        "perform": ["<vow_next>", 1],
        "}": ["<vow_next>", 1],
        "woogie": ["<vow_next>", 1],
        "default": ["<vow_next>", 1],
        "dismiss": ["<vow_next>", 1],
        "hop": ["<vow_next>", 1]
    },

    "<vow_tail>": { ############# verified 
        "{": ["<vow_tail>", 0],
        "vow": ["<vow_tail>", 1],
        "int": ["<vow_tail", 2],
        "string": ["<vow_tail", 2],
        "float": ["<vow_tail", 2],
        "bool": ["<vow_tail", 2],
        "curse": ["<vow_tail", 2],
        "id": ["<vow_tail", 2],
        "invoke": ["<vow_tail", 2],
        "cleave": ["<vow_tail", 2],
        "dismantle": ["<vow_tail", 2],
        "capture": ["<vow_tail", 2],
        "len": ["<vow_tail", 2],
        "recall": ["<vow_tail", 2],
        "boogie": ["<vow_tail", 2],
        "cycle": ["<vow_tail", 2],
        "sustain": ["<vow_tail", 2],
        "perform": ["<vow_tail", 2],
        "}": ["<vow_tail", 2],
        "woogie": ["<vow_tail", 2],
        "default": ["<vow_tail", 2],
        "dismiss": ["<vow_tail", 2],
        "hop": ["<vow_tail", 2]
    },

    "<boogie_tail>": { ############# verified
        "(": ["<boogie_tail>", 0],
        "{": ["<boogie_tail>", 1]
    },

    "<more_woogie>": { ############# verified
        "woogie": ["<more_woogie>", 0],
        "default": ["<more_woogie>", 1],
    },
 
    "<more_true_woogie>": { ############# verified
        "woogie": ["<more_true_woogie>", 0],
        "default": ["<more_true_woogie>", 1],
    },

    "<looping_stm>": { ############# verified
        "cycle": ["<looping_stm>", 0],
        "sustain": ["<looping_stm>", 1],
        "perform": ["<looping_stm>", 2]
    },
    
    "<cycle-loop>": { ############# verified
        "cycle": ["<cycle-loop>", 0]
    },

    "<cycle_initialize>": { ############# verified
        "id": ["<cycle_initialize>", 0],
        "int": ["<cycle_initialize>", 1],
        "float": ["<cycle_initialize>", 1],
        "string": ["<cycle_initialize>", 1],
        "bool": ["<cycle_initialize>", 1]
    },

     "<cycle_condition>": { ############# verified
        "(": ["<cycle_condition>", 0],
        "id": ["<cycle_condition>", 0],
        "int_literal": ["<cycle_condition>", 0],
        "string_literal": ["<cycle_condition>", 0],
        "bool_literal": ["<cycle_condition>", 0],
        "float_literal": ["<cycle_condition>", 0],
        "null_literal": ["<cycle_condition>", 0],
        "++": ["<cycle_condition>", 0],
        "--": ["<cycle_condition>", 0],
        "invoke": ["<cycle_condition>", 0],
        "capture": ["<cycle_condition>", 0],
        "cleave": ["<cycle_condition>", 0],
        "dismantle": ["<cycle_condition>", 0],
        "len": ["<cycle_condition>", 0],
        "-": ["<cycle_condition>", 0],
        "!": ["<cycle_condition>", 0],
    },

    "<iteration>": { ############# verified
        "++": ["<iteration>", 0],
        "--": ["<iteration>", 0],
        "id": ["<iteration>", 1],
        "-":  ["<iteration>", 0]
    },

    "<iteration_tail>": { ############# verified
        "++": ["<iteration_tail>", 0],
        "--": ["<iteration_tail>", 1],
        "=": ["<iteration_tail>", 2],
        "+=": ["<iteration_tail>", 2],
        "-=": ["<iteration_tail>", 2],
        "*=": ["<iteration_tail>", 2],
        "/=": ["<iteration_tail>", 2],
        "%=": ["<iteration_tail>", 2]
    },

    "<ite_val>": { ############# verified
        "id": ["<ite_val>", 0],
        "int_literal": ["<ite_val>", 1],
        "float_literal": ["<ite_val>", 2],
    }, 

    "<val_tail>": { ############# verified
        "+": ["<val_tail>", 0],
        "-": ["<val_tail>", 0],
        "*": ["<val_tail>", 0],
        "**": ["<val_tail>", 0],
        "/": ["<val_tail>", 0],
        "%": ["<val_tail>", 0],
        ")": ["<val_tail>", 1]
    },

    "<sustain-loop>": { ############# verified
        "sustain": ["<sustain-loop>", 0]
    },

    "<persustain-loop>": { ############# verified
        "perform": ["<persustain-loop>", 0]
    },

    "<con_loop_body>": { ############# verified
        "int": ["<con_loop_body>", 0],
        "string": ["<con_loop_body>", 0],
        "float": ["<con_loop_body>", 0],
        "bool": ["<con_loop_body>", 0],
        "curse": ["<con_loop_body>", 0],
        "restrict": ["<con_loop_body>", 0],
        "id": ["<con_loop_body>", 1],
        "invoke": ["<con_loop_body>", 2],
        "cleave": ["<con_loop_body>", 3],
        "dismantle": ["<con_loop_body>", 4],
        "capture": ["<con_loop_body>", 5],
        "len": ["<con_loop_body>", 6],
        "recall": ["<con_loop_body>", 7],
        "vow": ["<con_loop_body>", 8],      
        "boogie": ["<con_loop_body>", 8],
        "cycle": ["<con_loop_body>", 9],
        "sustain": ["<con_loop_body>", 9],
        "perform": ["<con_loop_body>", 9],
        "dismiss": ["<con_loop_body>", 10],
        "hop": ["<con_loop_body>", 11],
        "}": ["<con_loop_body>", 12],
        "woogie": ["<con_loop_body>", 12],
        "default": ["<con_loop_body>", 12],
    },

    "<literal>": {  ############# verified
        "int_literal": ["<literal>", 0],
        "float_literal": ["<literal>", 1],
        "string_literal": ["<literal>", 2],
        "bool_literal": ["<literal>", 3],
        "null_literal": ["<literal>", 4]
    },

    "<datatype>": { ############# verified
        "int": ["<datatype>", 0],
        "float": ["<datatype>", 1],
        "string": ["<datatype>", 2],
        "bool": ["<datatype>", 3]
    },

    "<arith_op>": { ############# verified
        "+": ["<arith_op>", 0],
        "-": ["<arith_op>", 1],
        "*": ["<arith_op>", 2],
        "/": ["<arith_op>", 3],
        "%": ["<arith_op>", 4],
        "**": ["<arith_op>", 5]
    },

    "<relational_op>": { ############# verified
        "==": ["<relational_op>", 0],
        "!=": ["<relational_op>", 1],
        ">": ["<relational_op>", 2],
        "<": ["<relational_op>", 3],
        ">=": ["<relational_op>", 4],
        "<=": ["<relational_op>", 5]
    },

    "<logic_op>": { ############# verified
        "&&": ["<logic_op>", 0],
        "||": ["<logic_op>", 1]
    },
 
    "<not_op>": { ############# verified
        "!": ["<not_op>", 0]
    },

    "<more_not_op>": { ############# verified
        "!": ["<more_not_op>", 0],
        "(": ["<more_not_op>", 1],
        "id": ["<more_not_op>", 1],
        "int_literal": ["<more_not_op>", 1],
        "string_literal": ["<more_not_op>", 1],
        "bool_literal": ["<more_not_op>", 1],
        "float_literal": ["<more_not_op>", 1],
        "null_literal": ["<more_not_op>", 1],
        "++": ["<more_not_op>", 1],
        "--": ["<more_not_op>", 1],
        "invoke": ["<more_not_op>", 1],
        "capture": ["<more_not_op>", 1],
        "cleave": ["<more_not_op>", 1],
        "dismantle": ["<more_not_op>", 1],
        "len": ["<more_not_op>", 1],
        "λ": ["<more_not_op>", 1]
    },

    "<assign_op>": { ############# verified
        "=": ["<assign_op>", 0],
        "+=": ["<assign_op>", 1],
        "-=": ["<assign_op>", 2],
        "*=": ["<assign_op>", 3],
        "/=": ["<assign_op>", 4],
        "%=": ["<assign_op>", 5]
    },

    "<pre>": { ############# verified
        "++": ["<pre>", 0],
        "--": ["<pre>", 1],
        "-" : ["<pre>", 2]
    },

    "<post>": { ############# verified
        "++": ["<post>", 0],
        "--": ["<post>", 1],
        ",": ["<post>", 2],
        ";": ["<post>", 2],
        "]": ["<post>", 2],
        "id": ["<post>", 2],
        "int_literal": ["<post>", 2],
        "string_literal": ["<post>", 2],
        "bool_literal": ["<post>", 2],
        "float_literal": ["<post>", 2],
        "null_literal": ["<post>", 2],
        "invoke": ["<post>", 2],
        "capture": ["<post>", 2],
        "cleave": ["<post>", 2],
        "dismantle": ["<post>", 2],
        "len": ["<post>", 2],
        "!": ["<post>", 2],
        "{": ["<post>", 2],
        "}": ["<post>", 2],
        ")": ["<post>", 2],
        "(": ["<post>", 2],
        "+": ["<post>", 2],
        "-": ["<post>", 2],
        "*": ["<post>", 2],
        "**": ["<post>", 2],
        "/": ["<post>", 2],
        "%": ["<post>", 2],
        "==": ["<post>", 2],
        "!=": ["<post>", 2],
        ">": ["<post>", 2],
        "<": ["<post>", 2],
        ">=": ["<post>", 2],
        "<=": ["<post>", 2],
        "&&": ["<post>", 2],
        "||": ["<post>", 2],
        ":": ["<post>", 2]
    }
}


##############
# ERRORS
############## 
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile: {self.pos_start.fn}, line {self.pos_start.ln + 1}\n'
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end) + '\n'
        return result
    
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Syntax Error', details)

def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)

    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n' 
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0 : idx_end = len(text)

    return result.replace('\t', ' ')

###################
# Syntax Analyzer 
###################

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()
        self.semantic_errors = []

    def advance(self):
        while True:
            self.token_idx += 1
            if self.token_idx < len(self.tokens):
                self.current_token = self.tokens[self.token_idx]
                if self.current_token.type not in ['\n', '\t', ' ', '\\n', '\\t', 'space']:
                    break
            else:
                self.current_token = None
                break
        return self.current_token
    
    def reset(self):
        self.token_idx = -1
        self.advance()

    def peek(self):
        current_idx = self.token_idx
        while True:
            current_idx += 1
            if current_idx < len(self.tokens):
                next_token = self.tokens[current_idx]
                if next_token.type not in ['\n', '\t', ' ', '\\n', '\\t', 'space']:
                    return next_token
            else:
                return None

    def syntax_analyzer(self):
        stack = ["<program>"]
        error = None

        while stack:
            top = stack[-1]
            #print(f"1. New Stack: {stack}\n2. Current Token: {self.current_token.type}")  
            if self.current_token is None or self.current_token.type == 'EOF':
                self.current_token = type('Token', (object,), {
                    'type': 'λ',
                    'pos_start': self.tokens[-1].pos_end if self.tokens else None,
                    'pos_end': self.tokens[-1].pos_end if self.tokens else None
                })()

            if is_non_terminal(top):
                if top in PREDICT_SET and self.current_token.type in PREDICT_SET[top]:
                    production_key = PREDICT_SET[top][self.current_token.type]
                    production = CFG[production_key[0]][production_key[1]]
                    #print(f"3. Production found for {top}: {self.current_token.type}")  
                    stack.pop()
                    stack.extend(reversed(production))
                else:
                    expected_tokens = list(PREDICT_SET[top].keys())
                    error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                               f"Unexpected token '{self.current_token.type}' here. Expected one of {expected_tokens}\n[FOR DEV: No prediction for {self.current_token.type} in {top}]")
                    break
            else:
                if top == self.current_token.type:
                    #print(f"3. Matched terminal {self.current_token.type}")  
                    stack.pop()
                    self.advance()
                else:
                    error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                               f"Expected '{top}', got '{self.current_token.type}'")
                    break

        if error:
            return error
        return []

def is_non_terminal(text): # (boolean) checks if the given string is a non-terminal
    return text.startswith('<') and text.endswith('>')

def parse_run(tokens):
    syntax_analysis = SyntaxAnalyzer(tokens)
    error = syntax_analysis.syntax_analyzer()

    if error:
        print(error)
        return "Failure from Syntax Analyzer", error.as_string()
    return "Successful from Syntax Analyzer", None