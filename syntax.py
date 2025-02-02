##############
# IMPORTS
##############
from lexer import run as lexer_run
from lexer import string_with_arrows 

############## 
# CONSTANTS 
##############

CFG = {
    "<program>": [              
        ["expansion", ";", "<global_dec>"] ########### 1 
    ],
    "<global_dec>": [           
        ["<global_type_dec>", "<global_dec>"],
        []
    ],
    
    "<global_type_dec>": [
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
        ["{", "<clan_item>", "}"]               ########### 50
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
        [",", "<literal>", "<clan_multi_item>"],########### 56
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
        ["<capture>", "(", "<id>", ")"],
        ["<cleave>", "(", "<arguments>", ")"],
        ["<dismantle>", "(", "<arguments>", ")"],
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
        ["<local_dec>"],                ###########
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

    "<local_dec>": [
        ["<datatype>", "<curse_or_var>"], ###########
        ["curse", "<local_void_curse>"], ###########
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
        ["[", "<value>", "]", "<assign_op>", "<expression>"], ###########
        ["(", "<arguments>", ")"] ###########
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
        ["{", "<statement>", "}",],
        ["vow", "(", "<expression>", ")", "{", "<con_loop_body>", "}", "<vow_next>"],
        []
    ],

    "<boogie_tail>": [
        ["(", "id", ")", "{", "woogie", "<literal>", ":", "<con_loop_body>", "<more_woogie>", "default", ":", "<statement>", "}"],
        ["{", "woogie", "<expression>", ":", "<con_loop_body>", "<more_true_woogie>", "default", ":", "<statement>", "}"],
    ],

    "<more_woogie>": [
        ["woogie", "<literal>", ":", "<con_loop_body>", "<more_woogie>"],
        []
    ],

    "<more_true_woogie>": [
        ["woogie", "(", "<expression>", ")", ":", "<con_loop_body>", "<more_true_woogie>"],
        []
    ],

    # "<conditional_looping_conditions>": [
    #     ["id"],
    #     ["<expression>"]
    # ],

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

    # "<cycle_ini_val>": [
    #     ["id"],
    #     ["int_literal"],
    #     ["<expression>"]
    # ],

    "<cycle_condition>": [
        ["<expression>"],
        ["<not_op>", "(", "<cycle_condition>", ")"]
    ],

    "<iteration>": [
        ["<pre>", "id"],
        ["id", "<post>"]
    ],

    "<sustain-loop>": [
        ["sustain", "(", "<expression>", ")", "{", "<con_loop_body>", "}"]
    ],

    "<persustain-loop>": [
        ["perform", "{", "<con_loop_body>", "}", "sustain", "(", "<expression>", ")", ";"]
    ],

    "<con_loop_body>": [
        ["<local_dec>", "<con_loop_body>"],                            ########### 0
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

    "<string_concat>": [
        ["string_literal", "+", "<string_concat>"], ########### 224
        ["string_literal"]                          ########### 225
    ],

    "<clan_access>": [
        ["id", "[", "<index>", "<more_index>", "]"]     ########### 237
    ],
    "<string_access>": [
        ["id", "[", "<index>", "]"]                 ########### 238
    ],
    "<index>": [
        ["id"],                                     ########### 239
        ["int_literal"]                             ########### 240
    ],
    "<more_index>": [
        [",", "<index>"],                           ########### 241
        []                                       ########### 242
    ],
    "<length>": [
        ["len", "(", "id", ")", ";"],               ########### 243
        ["len", "(", "<literal>", ")", ";"]         ########### 244    
    ],  
    "<cleave>": [
        ["cleave", "(", "<cleave_string>", ",", "<starting_index>", ",", "<number_of_letters>", ")"]    ########### 245
    ],
    "<cleave_string>": [
        ["id"]                                      ########### 246
    ], 
    "<starting_index>": [
        ["int_literal"]                             ########### 247
    ],
    "<number_of_letters>": [
        ["int_literal"]                             ########### 248
    ],
    "<dismantle>": [
        ["dismantle", "(", "<dismantle_string>", ",", "<dismantle_delimeter>", ")"]   ########### 249
    ],
    "<dismantle_string>": [
        ["id"],                                     ########### 250
        ["string_literal"],                         ########### 251
        ["<curse_call>"]                            ########### 252
    ],
    "<dismantle_delimeter>": [
        ["string_literal"]                          ########### 253
    ],

    "<literal>": [
        ["int_literal"],                            ########### 
        ["string_literal"],                         ########### 226
        ["bool_literal"],                           ########### 227
        ["float_literal"],                          ########### 228
        ["null_literal"],                           ########### 229
        []                                       ########### 230
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
        []                                       ###########
    ],

    "<assign_op>": [
        ["="],                                      ###########
        ["+="],                                     ###########
        ["-="],                                     ###########
        ["*="],                                     ###########
        ["/="]              ,                        ###########
        ["%="]                                      ###########
    ],

    "<pre>": [
        ["++"],                                     ########### 
        ["--"]                                      ########### 
    ],

    "<post>": [
        ["++"],                                     ########### 239
        ["--"],                         ########### 240
        []
    ],



    
}

PREDICT_SET = {
    "<program>": {
        "expansion": ["<program>", 0]
    },

    "<global_dec>": {
        "int": ["<global_dec>", 0],
        "string": ["<global_dec>", 0],
        "float": ["<global_dec>", 0],
        "bool": ["<global_dec>", 0],    
        "curse": ["<global_dec>",0],
        "restrict": ["<global_dec>", 0],
        "Ø": ["<global_dec>", 1]
    }, 

    "<global_type_dec>": {
        "int": ["<global_type_dec>", 0],
        "float": ["<global_type_dec>", 0],
        "string": ["<global_type_dec>", 0],
        "bool": ["<global_type_dec>", 0],
        "curse": ["<global_type_dec>", 1],
        "restrict": ["<global_type_dec>", 2]
    },

    "<curse_or_var>": {
        "curse": ["<curse_or_var>", 0],
        "id": ["<curse_or_var>", 1]
    },

    # "<restrict>": {
    #     "restrict": ["<restrict>", 0],
    #     "id": ["<restrict>", 1]
    # },

    "<nonvoid_curse_dec>": {
        "(": ["<nonvoid_curse_dec>", 0]
    },

    "<type_choice>": {
        "=": ["<type_choice>", 0],
        ",": ["<type_choice>", 0],
        "[": ["<type_choice>", 1],
        "[...]": ["<type_choice>", 1],
        ";": ["<type_choice>", 2]
    },

    "<var_dec>": {
        "=": ["<var_dec>", 0],
        ",": ["<var_dec>", 0]
    },

    "<assign>": {
        "=": ["<assign>", 0],
        ";": ["<assign>", 1],
        ",": ["<assign>", 1]
    },

    "<multi-assign>": {
        ",": ["<multi-assign>", 0],
        ";": ["<multi-assign>", 1],
    },
    
    "<init_void_curse>": {
        "id": ["<init_void_curse>", 0],
        "domain": ["<init_void_curse>", 1]
    },

    "<param>": {
        "int": ["<param>", 0],
        "float": ["<param>", 0],
        "string": ["<param>", 0],
        "bool": ["<param>", 0],
        ")": ["<param>", 1],
    },

    "<more_param>": {
        ",": ["<more_param>", 0],
        ")": ["<more_param>", 1],
    },

    "<clan_dec>": { #############
        "[": ["<clan_dec>", 0],
        "[...]": ["<clan_dec>", 0]
    },

    "<clan_size>": { #############
        "[": ["<clan_size>", 0],
        "[...]": ["<clan_size>", 1]
    },
    
    "<two_dimensional>": { #############
        "[": ["<two_dimensional>", 0],
        "=": ["<two_dimensional>", 1],
        ";": ["<two_dimensional>", 1],
    },

    "<clan_assign>": { #############
        "=": ["<clan_assign>", 0],
        ";": ["<clan_assign>", 1],
        "Ø": ["<clan_assign>", 1]
    },

    "<clan_literal>": { #############
        "{": ["<clan_literal>", 0]
    },

    "<clan_item>": { #############
        "int_literal": ["<clan_item>", 0],
        "string_literal": ["<clan_item>", 0],
        "bool_literal": ["<clan_item>", 0],
        "float_literal": ["<clan_item>", 0],
        "id": ["<clan_item>", 0],
        "++": ["<clan_item>", 0],
        "--": ["<clan_item>", 0],
        "invoke": ["<clan_item>", 0],
        "capture": ["<clan_item>", 0],
        "cleave": ["<clan_item>", 0],
        "dismantle": ["<clan_item>", 0],
        "len": ["<clan_item>", 0],
        "!": ["<clan_item>", 0],
        "(": ["<clan_item>", 0],
        "{": ["<clan_item>", 1],
        "}": ["<clan_item>", 2]
    },

    "<more_item>": { #############
        ",": ["<more_item>", 0],
        "}": ["<more_item>", 1]
    },

    "<clan_multi_item>": { #############
        ",": ["<clan_multi_item>", 0],
        "}": ["<clan_multi_item>", 1]
    },

    "<expression>": { #############
        "(": ["<expression>", 0],
        "id": ["<expression>", 1],
        "int_literal": ["<expression>", 1],
        "string_literal": ["<expression>", 1],
        "bool_literal": ["<expression>", 1],
        "float_literal": ["<expression>", 1],
        "++": ["<expression>", 1],
        "--": ["<expression>", 1],
        "invoke": ["<expression>", 1],
        "capture": ["<expression>", 1],
        "cleave": ["<expression>", 1],
        "dismantle": ["<expression>", 1],
        "len": ["<expression>", 1],
        "!": ["<expression>", 2],
    },

    "<operand>": { #############
        "++": ["<operand>", 0],
        "--": ["<operand>", 0],
        "id": ["<operand>", 1],
        "string_literal": ["<operand>", 1],
        "float_literal": ["<operand>", 1],
        "bool_literal": ["<operand>", 1],
        "int_literal": ["<operand>", 1],
        "dismantle": ["<operand>", 1],
        "capture": ["<operand>", 1],
        "invoke": ["<operand>", 1],
        "cleave": ["<operand>", 1],
        "len": ["<operand>", 1],
        "!": ["<operand>", 2],
    },

    "<value>": { #############
        "string_literal": ["<value>", 0],
        "float_literal": ["<value>", 0],
        "bool_literal": ["<value>", 0],
        "int_literal": ["<value>", 0],
        "id": ["<value>", 1],
        "invoke": ["<value>", 2],
        "capture": ["<value>", 3],
        "cleave": ["<value>", 4],
        "dismantle": ["<value>", 5],
        "len": ["<value>", 6],
    },

    "<curse_or_clan>": { #############
        "(" : ["<curse_or_clan>", 0],
        "[": ["<curse_or_clan>", 1],
        "+": ["<curse_or_clan>", 2],
        "-": ["<curse_or_clan>", 2],
        "*": ["<curse_or_clan>", 2],
        "/": ["<curse_or_clan>", 2],
        "%": ["<curse_or_clan>", 2],
        "!=": ["<curse_or_clan>", 2],
        "**": ["<curse_or_clan>", 2],
        "==": ["<curse_or_clan>", 2],
        ">": ["<curse_or_clan>", 2],
        "<": ["<curse_or_clan>", 2],
        ">=": ["<curse_or_clan>", 2],
        "<=": ["<curse_or_clan>", 2],
        "&&": ["<curse_or_clan>", 2],
        "||": ["<curse_or_clan>", 2],
        "!": ["<curse_or_clan>", 2],
        ")": ["<curse_or_clan>", 2],
        ";": ["<curse_or_clan>", 2],
        "++": ["<curse_or_clan>", 2],
        "--": ["<curse_or_clan>", 2],
        ",": ["<curse_or_clan>", 2],
        "]": ["<curse_or_clan>", 2]
    },

    "<more_clan>": { #############
        "[": ["<more_clan>", 0],
        "+": ["<more_clan>", 1],
        "-": ["<more_clan>", 1],
        "*": ["<more_clan>", 1],
        "/": ["<more_clan>", 1],
        "%": ["<more_clan>", 1],
        "**": ["<more_clan>", 1],
        "==": ["<more_clan>", 1],
        "!=": ["<more_clan>", 1],
        ">": ["<more_clan>", 1],
        "<": ["<more_clan>", 1],
        ">=": ["<more_clan>", 1],
        "<=": ["<more_clan>", 1],
        "&&": ["<more_clan>", 1],
        "||": ["<more_clan>", 1],
        "!": ["<more_clan>", 1],
        ";": ["<more_clan>", 1],
        ")": ["<more_clan>", 1],
    },

    "<more_logic>": { #############
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
        ";": ["<more_logic>", 1],
        "(": ["<more_logic>", 1],
        ":": ["<more_logic>", 1],
        "]": ["<more_logic>", 1]
    },

    "<operator>": { #############
        "+": ["<operator>", 0],
        "-": ["<operator>", 0],
        "*": ["<operator>", 0],
        "/": ["<operator>", 0],
        "%": ["<operator>", 0],
        "**": ["<operator>", 0],
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

    "<body>": { #############
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
        "}": ["<body>", 1],
        "Ø": ["<body>", 1]
    },
        
    "<statement>": { #############
        "int": ["<statement>", 0],
        "string": ["<statement>", 0],
        "float": ["<statement>", 0],
        "bool": ["<statement>", 0],
        "curse": ["<statement>", 0],
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
        "Ø": ["<statement>", 10]
    },

    "<local_dec>": {
        "int": ["<local_dec>", 0],
        "string": ["<local_dec>", 0],
        "float": ["<local_dec>", 0],
        "bool": ["<local_dec>", 0],
        "curse": ["<local_dec>", 1]
    },

    "<local_void_curse>": {
        "id": ["<local_void_curse>", 0]
    },

    "<recall_stm>": {
        "recall": ["<recall_stm>", 0],
    },

    "<recall_val>": {
        "(" : ["<recall_val>", 0],
        "++": ["<recall_val>", 0],
        "--": ["<recall_val>", 0],
        "id": ["<recall_val>", 0],
        "int_literal": ["<recall_val>", 0],
        "string_literal": ["<recall_val>", 0],
        "bool_literal": ["<recall_val>", 0],
        "float_literal": ["<recall_val>", 0],
        "dismantle": ["<recall_val>", 0],
        "cleave": ["<recall_val>", 0],
        "len": ["<recall_val>", 0],
        "!": ["<recall_val>", 0],
        "capture": ["<recall_val>", 0],
        "invoke": ["<recall_val>", 0],
        ";": ["<recall_val>", 1]
    },

    "<id_call>": {
        "=": ["<id_call>", 0],
        "+=": ["<id_call>", 0],
        "-=": ["<id_call>", 0],
        "*=": ["<id_call>", 0],
        "/=": ["<id_call>", 0],
        "%=": ["<id_call>", 0],
        "[": ["<id_call>", 1],
        "(": ["<id_call>", 2]
    },

    "<arguments>": {
        "(" : ["<arguments>", 0],
        "++": ["<arguments>", 0],
        "--": ["<arguments>", 0],
        "id": ["<arguments>", 0],
        "int_literal": ["<arguments>", 0],
        "string_literal": ["<arguments>", 0],
        "bool_literal": ["<arguments>", 0],
        "float_literal": ["<arguments>", 0],
        "dismantle": ["<arguments>", 0],
        "cleave": ["<arguments>", 0],
        "len": ["<arguments>", 0],
        "!": ["<arguments>", 0],
        "capture": ["<arguments>", 0],
        "invoke": ["<arguments>", 0],
        ")": ["<arguments>", 1]
    },

    "<more_arguments>": {
        ",": ["<more_arguments>", 0],
        ")": ["<more_arguments>", 1]
    },

    "<conditional_stm>": {
        "vow": ["<conditional_stm>", 0],
        "boogie": ["<conditional_stm>", 1]
    },

    "<vow_statement>": {
        "vow": ["<vow_statement>", 0]
    },

    "<vow_next>": {
        "else": ["<vow_next>", 0],
        "}": ["<vow_next>", 1],
        "int": ["<vow_next>", 1],
        "float": ["<vow_next>", 1],
        "string": ["<vow_next>", 1],
        "bool": ["<vow_next>", 1],
        "curse": ["<vow_next>", 1],
        "id": ["<vow_next>", 1],
        "invoke": ["<vow_next>", 1],
        "capture": ["<vow_next>", 1],
        "cleave": ["<vow_next>", 1],
        "dismantle": ["<vow_next>", 1],
        "len": ["<vow_next>", 1],
        "recall": ["<vow_next>", 1],
        "vow": ["<vow_next>", 1],
        "boogie": ["<vow_next>", 1],
        "cycle": ["<vow_next>", 1],
        "sustain": ["<vow_next>", 1],
        "perform": ["<vow_next>", 1],
        "dismiss": ["<vow_next>", 1],
        "hop": ["<vow_next>", 1]
    },

    "<vow_tail>": {
        "{": ["<vow_tail>", 0],
        "vow": ["<vow_tail>", 1],
        "}": ["<vow_tail>", 2],
    },

    "<boogie_tail>": {
        "(": ["<boogie_tail>", 0],
        "{": ["<boogie_tail>", 1]
    },

    "<more_woogie>": {
        "woogie": ["<more_woogie>", 0],
        "default": ["<more_woogie>", 1],
    },

    "<more_true_woogie>": {
        "woogie": ["<more_true_woogie>", 0],
        "default": ["<more_true_woogie>", 1],
    },

    "<conditional_looping_conditions>": {
        "id": ["<conditional_looping_conditions>", 1],
        "(": ["<conditional_looping_conditions>", 1],
        "int_literal": ["<conditional_looping_conditions>", 1],
        "string_literal": ["<conditional_looping_conditions>", 1],
        "bool_literal": ["<conditional_looping_conditions>", 1],
        "float_literal": ["<conditional_looping_conditions>", 1],
        "len": ["<conditional_looping_conditions>", 1],
        "!": ["<conditional_looping_conditions>", 1],
        "invoke": ["<conditional_looping_conditions>", 1],
        "capture": ["<conditional_looping_conditions>", 1],
        "cleave": ["<conditional_looping_conditions>", 1],
        "dismantle": ["<conditional_looping_conditions>", 1],
        "++": ["<conditional_looping_conditions>", 1],
        "--": ["<conditional_looping_conditions>", 1],
    },

    "<looping_stm>": {
        "cycle": ["<looping_stm>", 0],
        "sustain": ["<looping_stm>", 1],
        "perform": ["<looping_stm>", 2]
    },
    
    "<cycle-loop>": {
        "cycle": ["<cycle-loop>", 0]
    },

    "<cycle_initialize>": {
        "id": ["<cycle_initialize>", 0],
        "int": ["<cycle_initialize>", 1],
        "float": ["<cycle_initialize>", 1],
        "string": ["<cycle_initialize>", 1],
        "bool": ["<cycle_initialize>", 1]
    },

     "<cycle_condition>": {
        "id": ["<cycle_condition>", 0],
        "int_literal": ["<cycle_condition>", 0],
        "string_literal": ["<cycle_condition>", 0],
        "bool_literal": ["<cycle_condition>", 0],
        "float_literal": ["<cycle_condition>", 0],
        "(": ["<cycle_condition>", 0],
        "++": ["<cycle_condition>", 0],
        "--": ["<cycle_condition>", 0],
        "!": ["<cycle_condition>", 1],
    },

    "<iteration>": {
        "++": ["<iteration>", 0],
        "--": ["<iteration>", 0],
        "id": ["<iteration>", 1]
    },

    "<sustain-loop>": {
        "sustain": ["<sustain-loop>", 0]
    },

    "<persustain-loop>": {
        "perform": ["<persustain-loop>", 0]
    },

    "<con_loop_body>": {
        "int": ["<con_loop_body>", 0],
        "string": ["<con_loop_body>", 0],
        "float": ["<con_loop_body>", 0],
        "bool": ["<con_loop_body>", 0],
        "curse": ["<con_loop_body>", 0],
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

    "<literal>": {  #############
        "int_literal": ["<literal>", 0],
        "string_literal": ["<literal>", 1],
        "bool_literal": ["<literal>", 2],
        "float_literal": ["<literal>", 3],
        "null_literal": ["<literal>", 4],
        ";": ["<literal>", 5],
        ",": ["<literal>", 5],
        "Ø": ["<literal>", 5]
    },

    "<datatype>": { ############# 97 in first set
        "int": ["<datatype>", 0],
        "float": ["<datatype>", 1],
        "string": ["<datatype>", 2],
        "bool": ["<datatype>", 3]
    },

    "<arith_op>": { #############
        "+": ["<arith_op>", 0],
        "-": ["<arith_op>", 1],
        "*": ["<arith_op>", 2],
        "/": ["<arith_op>", 3],
        "%": ["<arith_op>", 4],
        "**": ["<arith_op>", 5]
    },

    "<relational_op>": { #############
        "==": ["<relational_op>", 0],
        "!=": ["<relational_op>", 1],
        ">": ["<relational_op>", 2],
        "<": ["<relational_op>", 3],
        ">=": ["<relational_op>", 4],
        "<=": ["<relational_op>", 5]
    },

    "<logic_op>": { #############
        "&&": ["<logic_op>", 0],
        "||": ["<logic_op>", 1]
    },

    "<not_op>": { #############
        "!": ["<not_op>", 0]
    },

    "<more_not_op>": { #############
        "!": ["<more_not_op>", 0],
        "id": ["<more_not_op>", 1],
        "invoke": ["<more_not_op>", 1],
        "capture": ["<more_not_op>", 1],
        "cleave": ["<more_not_op>", 1],
        "dismantle": ["<more_not_op>", 1],
        "len": ["<more_not_op>", 1],
        "int_literal": ["<more_not_op>", 1],
        "string_literal": ["<more_not_op>", 1],
        "bool_literal": ["<more_not_op>", 1],
        "float_literal": ["<more_not_op>", 1],
        "(": ["<more_not_op>", 1],
        "Ø": ["<more_not_op>", 1]
    },

    "<assign_op>": { #############
        "=": ["<assign_op>", 0],
        "+=": ["<assign_op>", 1],
        "-=": ["<assign_op>", 2],
        "*=": ["<assign_op>", 3],
        "/=": ["<assign_op>", 4],
        "%=": ["<assign_op>", 5]
    },

    "<pre>": {
        "++": ["<pre>", 0],
        "--": ["<pre>", 1]
    },

    "<post>": {
        "++": ["<post>", 0],
        "--": ["<post>", 1],
        "+": ["<post>", 2],
        "-": ["<post>", 2],
        "*": ["<post>", 2],
        "/": ["<post>", 2],
        "%": ["<post>", 2],
        "**": ["<post>", 2],
        "==": ["<post>", 2],
        "!=": ["<post>", 2],
        ">": ["<post>", 2],
        "<": ["<post>", 2],
        ">=": ["<post>", 2],
        "<=": ["<post>", 2],
        "&&": ["<post>", 2],
        "||": ["<post>", 2],
        "!": ["<post>", 2],
        ")": ["<post>", 2],
        ",": ["<post>", 2],
        ";": ["<post>", 2],
        "(": ["<post>", 2],
        "=": ["<post>", 2],
        "+=": ["<post>", 2],
        "-=": ["<post>", 2],
        "*=": ["<post>", 2],
        "%=": ["<post>", 2],
        "]": ["<post>", 2]
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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        while True:
            self.token_idx += 1
            if self.token_idx < len(self.tokens):
                self.current_token = self.tokens[self.token_idx]
                if self.current_token.type not in ['\n', '\t', ' ', '\\n', '\\t', 'space', 'EOF']:
                    break
            else:
                self.current_token = None
                break
        return self.current_token

    def parse(self):
        stack = ["<program>"]
        error = "";

        while stack:
            top = stack[-1]
            print(f"1. Stack: {stack}")
            if self.current_token is None:
                self.current_token = type('Token', (object,), {'type': 'Ø'})()
                
            print(f"2. Current Token: {self.current_token.type}")
            if self.current_token.type in ['id', 'int_literal', 'string_literal', 'bool_literal', 'float_literal']:
                print(f"2. Token Value: {self.current_token.value}")

            if is_non_terminal(top):
                # Check what production to use by checking the top of the stack and the current token
                if top in PREDICT_SET and self.current_token.type in PREDICT_SET[top]:
                    production_key = PREDICT_SET[top][self.current_token.type]
                else:
                    if self.current_token.type == 'Ø':
                        break
                    else: 
                        error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                               f"Invalid key '{self.current_token.type}' for production '{top}'").as_string()
                        print(self.current_token.pos_start.idx, self.current_token.pos_start.col)
                        break
                print(f"3. Production Key: {production_key}")

                if production_key[0] in CFG:
                    production = CFG[production_key[0]][production_key[1]]
                    stack.pop()  # Remove the non-terminal from the stack
                    print(f"4. Using Production: {production}")

                    # Check if the production exists as a key in CFG
                    if production_key[0] in CFG:
                        # Append/push its values in reverse order into the stack
                        for symbol in reversed(CFG[production_key[0]][production_key[1]]):
                            stack.append(symbol)
                            print(f"5. Symbol Pushed: {symbol}")
                    else:
                        if self.current_token.type == 'Ø':
                            break
                        else:
                            error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                                    f"No production rule for '{production}'").as_string()
                            break
                else:
                    if self.current_token.type == 'Ø':
                        break
                    else: 
                        error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                               f"Syntax Error: No   prediction for '{production_key}'").as_string()
                        break
            else:
                # Check if the top of the stack is equal to the current token
                if top == self.current_token.type:
                    stack.pop()  # Remove the terminal from the stack
                    print(f"2. Matched Terminal: {top}")
                    self.advance()  # Move to the next token
                else:
                    if self.current_token.type == 'Ø':
                        break
                    else:
                        error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                                f"Expected '{top}', got '{self.current_token.type}'").as_string()
                        break

        if error:
            return error
        return []
 
def is_non_terminal(text): # (boolean) checks if the given string is a non-terminal
    return text.startswith('<') and text.endswith('>')

def parse_run(tokens):
    parser = Parser(tokens)
    error = parser.parse()
    if error:
        print(error)
        return error
    return "Successful from Syntax Analyzer"