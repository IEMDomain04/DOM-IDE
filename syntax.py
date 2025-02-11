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
        ["<expression>"],
        ["<not_op>", "(", "<cycle_condition>", ")"]
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
    "<program>": { ############# verified
        "expansion": ["<program>", 0]
    },

    "<global_dec>": { ############# verified
        "int": ["<global_dec>", 0],
        "float": ["<global_dec>", 0],
        "string": ["<global_dec>", 0],
        "bool": ["<global_dec>", 0],    
        "curse": ["<global_dec>",0],
        "restrict": ["<global_dec>", 0],
        "Ø": ["<global_dec>", 1]
    }, 

    "<global_type_dec>": { ############# verified
        "int": ["<global_type_dec>", 0],
        "float": ["<global_type_dec>", 0],
        "string": ["<global_type_dec>", 0],
        "bool": ["<global_type_dec>", 0],
        "curse": ["<global_type_dec>", 1],
        "restrict": ["<global_type_dec>", 2]
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
    },

    "<clan_assign>": { ############# verified
        "=": ["<clan_assign>", 0],
        "Ø": ["<clan_assign>", 1],
        ";": ["<clan_assign>", 1]
    },

    "<clan_literal>": { ############# verified
        "{": ["<clan_literal>", 0]
    },

    "<clan_item>": { ############# verified
        "(": ["<clan_item>", 0],
        "id": ["<clan_item>", 0],
        "int_literal": ["<clan_item>", 0],
        "string_literal": ["<clan_item>", 0],
        "bool_literal": ["<clan_item>", 0],
        "float_literal": ["<clan_item>", 0],
        "++": ["<clan_item>", 0],
        "--": ["<clan_item>", 0],
        "invoke": ["<clan_item>", 0],
        "capture": ["<clan_item>", 0],
        "cleave": ["<clan_item>", 0],
        "dismantle": ["<clan_item>", 0],
        "len": ["<clan_item>", 0],
        "!": ["<clan_item>", 0],
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
        "++": ["<expression>", 1],
        "--": ["<expression>", 1],
        "invoke": ["<expression>", 1],
        "capture": ["<expression>", 1],
        "cleave": ["<expression>", 1],
        "dismantle": ["<expression>", 1],
        "len": ["<expression>", 1],
        "!": ["<expression>", 2],
    },

    "<operand>": { ############# verified
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

    "<value>": { ############# verified
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
        "}": ["<body>", 1],
        "Ø": ["<body>", 1]
    },
        
    "<statement>": { ############# verified
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

    "<local_dec>": { ############# verified
        "int": ["<local_dec>", 0],
        "float": ["<local_dec>", 0],
        "string": ["<local_dec>", 0],
        "bool": ["<local_dec>", 0],
        "curse": ["<local_dec>", 1]
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
        "++": ["<recall_val>", 0],
        "--": ["<recall_val>", 0],
        "invoke": ["<recall_val>", 0],
        "capture": ["<recall_val>", 0],
        "cleave": ["<recall_val>", 0],
        "dismantle": ["<recall_val>", 0],
        "len": ["<recall_val>", 0],
        "!": ["<recall_val>", 0],
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
        "++": ["<arguments>", 0],
        "--": ["<arguments>", 0],
        "invoke": ["<arguments>", 0],
        "capture": ["<arguments>", 0],
        "cleave": ["<arguments>", 0],
        "dismantle": ["<arguments>", 0],
        "len": ["<arguments>", 0],
        "!": ["<arguments>", 0],
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
        "++": ["<cycle_condition>", 0],
        "--": ["<cycle_condition>", 0],
        "invoke": ["<cycle_condition>", 0],
        "capture": ["<cycle_condition>", 0],
        "cleave": ["<cycle_condition>", 0],
        "dismantle": ["<cycle_condition>", 0],
        "len": ["<cycle_condition>", 0],
        "!": ["<cycle_condition>", 1],
    },

    "<iteration>": { ############# verified
        "++": ["<iteration>", 0],
        "--": ["<iteration>", 0],
        "id": ["<iteration>", 1]
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
        "++": ["<more_not_op>", 1],
        "--": ["<more_not_op>", 1],
        "invoke": ["<more_not_op>", 1],
        "capture": ["<more_not_op>", 1],
        "cleave": ["<more_not_op>", 1],
        "dismantle": ["<more_not_op>", 1],
        "len": ["<more_not_op>", 1],
        "Ø": ["<more_not_op>", 1]
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
        "--": ["<pre>", 1]
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
# AST Nodes
###################

class ASTNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3 
        prefix = spaces + "ᴸ---" if self.parent else spaces
        print(prefix + str(self.data))
        if self.children:
            for child in self.children:
                child.print_tree()

class NumNode(ASTNode): # for numbers
    def __init__(self, value):
        super().__init__(f"Number: {value}")
        self.value = value

class BinOpNode(ASTNode): # binary operation
    def __init__(self, left, op, right):
        super().__init__(f"Binary Operation: {op.type}")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class RelOpNode(ASTNode): # relational operation
    def __init__(self, left, op, right):
        super().__init__(f"Relational Operation: {op.type}")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class LogOpNode(ASTNode): # logical operation
    def __init__(self, left, op, right):
        super().__init__(f"Logical Operation: {op.type}")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class UnaryOpNode(ASTNode): # unary operation
    def __init__(self, op, expr, pre=False, post=False):
        super().__init__("Unary Operation")
        self.op = UnaryOperator(op)
        self.expr = expr
        self.pre = pre
        self.post = post
        if pre: self.add_child(self.op)
        self.add_child(expr)
        if post: self.add_child(self.op)

    def __repr__(self):
        if self.pre:
            return f"{self.op}{self.expr}"
        elif self.post:
            return f"{self.expr}{self.op}"
        else:
            return f"{self.op} {self.expr}"
    
class UnaryOperator(ASTNode): # unary operator
    def __init__(self, op):
        super().__init__(f"Unary Operator: {op.type}")
        self.op = op.type

class RestrictNode(ASTNode): # for restrict keyword
    def __init__(self):
        super().__init__("Restrict")

class DatatypeNode(ASTNode): # for datatype keywords
    def __init__(self, datatype):
        super().__init__(f"Datatype: {datatype}")
        self.datatype = datatype

class IdNode(ASTNode): # for identifier names
    def __init__(self, name):
        super().__init__(f"Identifier: {name}")
        self.name = name

class VarNode(ASTNode): # for variables
    def __init__(self, name):
        super().__init__(f"Variable: {name}")
        self.name = name

    def __repr__(self):
        return f"{self.name}"

class VarDecNode(ASTNode): # for variable assignments
    def __init__(self, restrict, datatype, name, value):
        super().__init__("Variable Declaration")
        self.restrict = restrict
        self.datatype = datatype
        self.name = name
        self.value = value
        if restrict:
            self.add_child(RestrictNode())
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))
        self.add_child(value)

    def __repr__(self):
        restrict_str = " restrict" if self.restrict else ""
        return f"{self.datatype} {self.name} = {self.value}{restrict_str}"

class VarAssignNode(ASTNode): # for variable assignments
    def __init__(self, name, value):
        super().__init__("Variable Assignment")
        self.name = name
        self.value = value
        self.add_child(IdNode(name))
        self.add_child(value)

    def __repr__(self):
        return f"{self.name} = {self.value}"

class ClanDecNode(ASTNode): # for arrays
    def __init__(self, restrict, datatype, name, size, initial_values=None):
        super().__init__("Clan Declaration")
        self.restrict = restrict
        self.datatype = datatype
        self.name = name
        self.size = size
        self.initial_values = initial_values or []
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))
        self.add_child(size)
        if initial_values:
            self.add_child(ClanLiteralNode(initial_values))

    def __repr__(self):
        if self.initial_values:
            return f"{self.datatype} {self.name}[{self.size}] = {self.initial_values}"
        else:
            return f"{self.datatype} {self.name}[{self.size}]"

class ClanLiteralNode(ASTNode): # for clan literals
    def __init__(self, values):
        super().__init__(f"Clan Literal: {{{', '.join(str(value.data) for value in values)}}}")
        self.values = values
        for value in values:
            self.add_child(value)
    
class ClanIndexNode(ASTNode): # for array indexing
    def __init__(self, index):
        super().__init__("Clan Index")
        self.index = index
        self.add_child(index)

    def __repr__(self):
        return f"{self.index}"

class ClanSizeNode(ASTNode): # for array size
    def __init__(self, size):
        super().__init__("Clan Size")
        self.size = size
        self.add_child(size)
    
class ClanAccessNode(ASTNode): # for array access
    def __init__(self, name, index):
        super().__init__("Clan Access")
        self.name = name
        self.index = index
        self.add_child(IdNode(name))
        self.add_child(index)

class ClanIndexAssignNode(ASTNode): # for array index assignments
    def __init__(self, name, index, values):
        super().__init__("Clan Index Assign")
        self.name = name
        self.index = index
        self.values = values
        self.add_child(IdNode(name))
        self.add_child(index)
        for value in values:
            self.add_child(value)

    def __repr__(self):
        return f"{self.name}[{self.index}] = {self.values}"
    
class ClanAssignNode(ASTNode): # for assigning the whole array
    def __init__(self, name, values):
        super().__init__("Clan Assign")
        self.name = name
        self.values = values
        self.add_child(IdNode(name))
        self.add_child(ClanLiteralNode(values))

    def __repr__(self):
        return f"{self.name} = {self.values}"

class CurseDecNode(ASTNode): # for functions
    def __init__(self, datatype, name, parameters, body):
        super().__init__("Curse Declaration")
        self.datatype = datatype
        self.name = name
        self.parameters = parameters
        self.body = body
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))
        for param in parameters:
            self.add_child(param)
        self.add_child(body)

    def __repr__(self):
        return f"{self.datatype} {self.name}({self.parameters}) {self.body}"

class CurseDomainNode(ASTNode): # for function domain
    def __init__(self, body):
        super().__init__("Main Curse")
        self.body = body
        self.add_child(body)

    def __repr__(self):
        return f"{self.body}"

class ParamNode(ASTNode): # for function parameters
    def __init__(self, datatype, name):
        super().__init__("Parameter")
        self.datatype = datatype
        self.name = name
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))

class ArgNode(ASTNode): # for function arguments
    def __init__(self, value):
        super().__init__("Argument")
        self.value = value
        self.add_child(value)

class BodyNode(ASTNode): # for body of functions and vows and boogies and cycles and sustains and perform-sustains
    def __init__(self):
        super().__init__("Body")

class CurseCallNode(ASTNode): # for curse calls
    def __init__(self, name, arguments):
        super().__init__("Curse Call")
        self.name = name
        self.arguments = arguments
        self.add_child(IdNode(name))
        if arguments:
            args_node = ASTNode("Arguments")
            for arg in arguments:
                args_node.add_child(arg)
            self.add_child(args_node)

class StringNode(ASTNode): # for strings
    def __init__(self, value):
        super().__init__(f"String: {value}")
        self.value = value

class StringConcatNode(ASTNode): # for string concatenations
    def __init__(self, left, op, right):
        super().__init__("String Concatenation")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

class InvokeNode(ASTNode): # for printing invoke("Hello, World!")
    def __init__(self, value):
        super().__init__("Invoke Statement")
        self.value = value
        self.add_child(value)

class CaptureNode(ASTNode): # for user input, capture(id)
    def __init__(self, name):
        super().__init__("Capture Statement")
        self.name = name
        self.add_child(name)

class CleaveNode(ASTNode): # for cleave statements, cleave(id, index1Start, index2End)
    def __init__(self, name, index1, index2):
        super().__init__("Cleave Statement")
        self.name = name
        self.index1 = index1
        self.index2 = index2
        self.add_child(name)
        self.add_child(index1)
        self.add_child(index2)

class DismantleNode(ASTNode): # for dismantle statements, dismantle(id, delimiter)
    def __init__(self, name, delimiter):
        super().__init__("Dismantle Statement")
        self.name = name
        self.delimiter = delimiter
        self.add_child(name)
        self.add_child(delimiter)

class LenNode(ASTNode): # for len statements, len(id)
    def __init__(self, name):
        super().__init__("Len Statement")
        self.name = name
        self.add_child(name)

class RecallNode(ASTNode): # for return statements
    def __init__(self, value):
        super().__init__("Recall Statement")
        self.value = value
        self.add_child(value)

class DismissNode(ASTNode): # for break statements
    def __init__(self):
        super().__init__("Dismiss")

class HopNode(ASTNode): # for continue statements
    def __init__(self):
        super().__init__("Hop")
    
class WoogieNode(ASTNode): # for normal switch-case statements
    def __init__(self, expression, woogie, default_case=None):
        super().__init__("Woogie Statement")
        self.expression = expression
        self.woogie = woogie
        self.default_case = default_case
        self.add_child(expression)
        for case_expr, case_body in woogie:
            self.add_child(case_expr)
            self.add_child(case_body)
        if default_case:
            self.add_child(default_case)

class WoogieTrueNode(ASTNode): # for switch true (woogie true)
    def __init__(self, expression, woogie, default_case=None):
        super().__init__("Woogie")
        self.expression = expression
        self.woogie = woogie
        self.default_case = default_case
        self.add_child(expression)
        for case_expr, case_body in woogie:
            self.add_child(case_expr)
            self.add_child(case_body)
        if default_case:
            self.add_child(default_case)

class WoogieStatementNode(ASTNode): # for cases
    def __init__(self, expression, body):
        super().__init__("Woogie Statement")
        self.expression = expression
        self.body = body
        self.add_child(expression)
        self.add_child(body)

class DefaultCaseNode(ASTNode): # for default cases
    def __init__(self, body):
        super().__init__("Default Case")
        self.body = body
        self.add_child(body)

class VowNode(ASTNode): # if-else (vow-else)
    def __init__(self, condition, body, else_vows=None, else_body=None):
        super().__init__("Vow Statement")
        self.condition = condition
        self.body = body
        self.else_vows = else_vows or []
        self.else_body = else_body
        self.add_child(condition)
        self.add_child(body)
        for else_vow in self.else_vows:
            self.add_child(else_vow)
        if else_body:
            self.add_child(else_body)

    def __repr__(self):
        return f"VowNode({self.condition}, {self.body}, {self.else_body})"

class ElseVow(ASTNode):
    def __init__(self, condition, body):
        super().__init__("Else Vow")
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

class ElseNode(ASTNode):
    def __init__(self, body):
        super().__init__("Else")
        self.body = body
        self.add_child(body)

class BoogieNode(ASTNode): # switch-case (boogie)
    def __init__(self, expression, cases):
        super().__init__("Boogie Statement")
        self.expression = expression
        self.cases = cases
        self.add_child(expression)
        for case_expr, case_body in cases:
            self.add_child(case_expr)
            self.add_child(case_body)

    def __repr__(self):
        return f"BoogieNode({self.expression}, {self.cases})"

class SustainNode(ASTNode): # while loop (sustain)
    def __init__(self, condition, body):
        super().__init__("Sustain Statement")
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

    def __repr__(self):
        return f"SustainNode({self.condition}, {self.body})"

class PerformSustainNode(ASTNode): # do-while loop (perform-sustain)
    def __init__(self, body, condition):
        super().__init__("PerformSustain Statement")
        self.body = body
        self.condition = condition
        self.add_child(body)
        self.add_child(condition)

    def __repr__(self):
        return f"PerformSustainNode({self.body}, {self.condition})"

class CycleNode(ASTNode): # for-loop (cycle)
    def __init__(self, init, condition, increment, body):
        super().__init__("Cycle Statement")
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body
        self.add_child(init)
        self.add_child(condition)
        self.add_child(increment)
        self.add_child(body)

    def __repr__(self):
        return f"CycleNode({self.init}, {self.condition}, {self.increment}, {self.body})"
    
##################
## AST Traverser
##################

class Interpreter: 
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    ##############################

    def visit_ASTNode(self, node):
        pass

    def visit_NumNode(self, node):
        print("Found num node!")

    def visit_BinOpNode(self, node):
        print("Found bin op node!")
        self.visit(node.left_node)
        self.visit(node.right_node)

    def visit_UnaryOpNode(self, node):
        print("Found unary op node!")
        self.visit(node.node)

###################
# Symbol Table
###################

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

###################
# Syntax Analyzer 
###################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()
        self.semantic_errors = []
        self.symbol_table = SymbolTable()

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

###################
## Syntax Analyzer
###################

    def syntax_analyzer(self):
        stack = ["<program>"]
        error = "";

        while stack:
            top = stack[-1]
            print(f"1. Stack: {stack}")
            if self.current_token is None or self.current_token.type == 'EOF':
                self.current_token = type('Token', (object,), {
                    'type': 'Ø',
                    'pos_start': self.tokens[-1].pos_end if self.tokens else None,
                    'pos_end': self.tokens[-1].pos_end if self.tokens else None
                })()
                
            if self.current_token.type in ['id', 'int_literal', 'bool_literal', 'float_literal']:
                print(f"2. Current Token: {self.current_token.type} '{self.current_token.value}'")
            else: 
                print(f"2. Current Token: {self.current_token.type}")

            if is_non_terminal(top):
                # Check what production to use by checking the top of the stack and the current token
                if top in PREDICT_SET and self.current_token.type in PREDICT_SET[top]:
                    production_key = PREDICT_SET[top][self.current_token.type]
                else:
                        if self.current_token.type == 'Ø':
                            error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                               f"Unexpected File termination here\n[FOR DEV: Invalid key '{self.current_token.type}' for production '{top}']").as_string()
                        else:
                            error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, 
                                               f"Unexpected token '{self.current_token.type}' \n[FOR DEV: Invalid key '{self.current_token.type}' for production '{top}']").as_string()
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
                                               f"Syntax Error: No prediction for '{production_key}'").as_string()
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

###################
# AST Builder
###################

    def build_ast(self):
        self.reset()
        root = ASTNode("Program")
        while self.current_token is not None and self.current_token.type != 'EOF':
            if self.current_token is not None and self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                declaration = self.parseDeclaration()
                if declaration:
                    root.add_child(declaration)
            elif self.current_token is not None and self.current_token.type == 'id':
                assignment = self.parseIdCall()
                if assignment:
                    root.add_child(assignment)
            else: 
                self.advance()
        return root

    def parseFactor(self):
        tok = self.current_token

        if tok.type in ('int_literal', 'float_literal'):
            self.advance()
            return NumNode(tok.value)
        elif tok.type == 'id':
            self.advance()
            if self.current_token.type in ('++', '--'):
                op = self.current_token
                self.advance()
                return UnaryOpNode(op, VarNode(tok.value), post=True)
            return VarNode(tok.value)
        elif tok.type == '(':
            self.advance()
            expr = self.parseExpr()
            if self.current_token.type == ')':
                self.advance()
                return expr
            else:
                raise InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'")
        elif tok.type in ('+', '-'):
            self.advance()
            factor = self.parseFactor()
            return UnaryOpNode(tok, factor)
        elif tok.type in ('++', '--'):
            op = tok
            self.advance()
            factor = self.parseFactor()
            return UnaryOpNode(op, factor, pre=True)
        elif tok.type == '!':
            op = tok
            self.advance()
            factor = self.parseFactor()
            return UnaryOpNode(op, factor, pre=True)
        else:
            raise InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, identifier, or '('")

    def parseTerm(self):
        return self.parseBinOp(self.parseFactor, ['*', '/', '%'], BinOpNode)

    def parseArithExpr(self):
        return self.parseBinOp(self.parseTerm, ['+', '-'], BinOpNode)

    def parseRelExpr(self):
        return self.parseBinOp(self.parseArithExpr, ['<', '>', '<=', '>=', '==', '!='], RelOpNode)

    def parseLogExpr(self):
        return self.parseBinOp(self.parseRelExpr, ['&&', '||'], LogOpNode)

    def parseExpr(self):
        return self.parseLogExpr()

    def parseBinOp(self, func, ops, node_class):
        left = func()
        while self.current_token.type in ops:
            op = self.current_token
            self.advance()
            right = func()
            left = node_class(left, op, right)
        return left
    
    def parseIdCall(self):
        if self.current_token.type == 'id':
            name = self.current_token.value
            self.advance()
            if self.current_token.type in ['=', '+=', '-=', '*=', '/=', '%=']:
                op = self.current_token.type
                self.advance()
                if self.current_token.type == '{': # check later for previous node type
                    self.advance()
                    values = []
                    while self.current_token.type != '}':
                        values.append(self.parseExpr())
                        if self.current_token.type == ',':
                            self.advance()
                    self.advance()
                    return ClanAssignNode(name, values)
                elif self.current_token.type == 'id' and self.tokens[self.token_idx + 1].type == '(':
                    value = self.parseIdCall()
                    return VarAssignNode(name, value)
                elif self.current_token.type == 'id' and self.tokens[self.token_idx + 1].type == '[':
                    clan_id = self.current_token.value
                    self.advance()
                    self.advance() # self advanced two times to reach the actual index value
                    index = self.parseExpr()
                    index_node = ClanIndexNode(index)
                    value = ClanAccessNode(clan_id, index_node)
                    return VarAssignNode(name, value)
                elif self.current_token.type == 'cleave':
                    self.advance()
                    if self.current_token.type == '(':
                        self.advance()
                        cleave_id = IdNode(self.current_token.value) # check node types after advancing
                        self.advance() 
                        if self.current_token.type == ',':
                            self.advance()
                            index1 = self.parseExpr()
                            if self.current_token.type == ',':
                                self.advance()
                                index2 = self.parseExpr()
                                if self.current_token.type == ')':
                                    self.advance()
                                    return VarAssignNode(name, CleaveNode(cleave_id, index1, index2))
                elif self.current_token.type == 'dismantle':
                    self.advance()
                    if self.current_token.type == '(':
                        self.advance()
                        dismantle_id = IdNode(self.current_token.value) # check node types after advancing
                        self.advance()
                        if self.current_token.type == ',':
                            self.advance()
                            delimiter = StringNode(self.current_token.value)
                            self.advance()
                            if self.current_token.type == ')':
                                self.advance()
                                return VarAssignNode(name, DismantleNode(dismantle_id, delimiter))
                elif self.current_token.type == 'len':
                    self.advance()
                    if self.current_token.type == '(':
                        self.advance()  
                        len_id = IdNode(self.current_token.value)
                        self.advance()
                        if self.current_token.type == ')': # check if no more than 2 args
                            self.advance()
                            return VarAssignNode(name, LenNode(len_id))
                else:
                    value = self.parseExpr()
                    if op == '=':
                        return VarAssignNode(name, value)
                    else:
                        # Transform shorthand assignment into equivalent expression
                        bin_op = op[0]  # Get the operator part of the shorthand assignment
                        left = VarNode(name)
                        right = value
                        bin_op_node = BinOpNode(left, type('Token', (object,), {'type': bin_op})(), right)
                        return VarAssignNode(name, bin_op_node)
            elif self.current_token.type == '[':
                self.advance()
                index = self.parseExpr()
                index_node = ClanIndexNode(index)
                if self.current_token.type == ']':
                    self.advance()
                    if self.current_token.type == '=':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            values = []
                            while self.current_token.type != '}':
                                values.append(self.parseExpr())
                                if self.current_token.type == ',':
                                    self.advance()
                            return ClanIndexAssignNode(name, index_node, values)
            elif self.current_token.type == '(':
                self.advance()
                args = []
                while self.current_token.type != ')':
                    if self.current_token.type == 'string_literal':
                        args.append(StringNode(self.current_token.value))
                        self.advance()
                    elif self.current_token.type == 'id':
                        value = self.parseIdCall()
                        args.append(value)
                    else:
                        args.append(self.parseExpr())
                    if self.current_token.type == ',':
                        self.advance()
                self.advance()
                return CurseCallNode(name, args)
        return None
    

    def parseDeclaration(self):
        if self.current_token.type in ['int', 'float', 'string', 'bool']:
            datatype = self.current_token.type
            self.advance()

            if self.current_token.type == 'id':
                name = self.current_token.value
                self.advance()
                if self.current_token.type == '=':
                    self.advance()
                    if self.current_token.type == 'id' and self.peek().type == '(':
                        value = self.parseIdCall()
                        return VarDecNode(None, datatype, name, value)
                    elif self.current_token.type == 'id' and self.peek().type == '[':
                        clan_id = self.current_token.value
                        self.advance()
                        self.advance()
                        index = self.parseExpr()
                        index_node = ClanIndexNode(index)
                        value = ClanAccessNode(clan_id, index_node)
                        return VarDecNode(None, datatype, name, value)
                    elif self.current_token.type == 'cleave':
                        self.advance()
                        if self.current_token.type == '(':
                            self.advance()
                            cleave_id = IdNode(self.current_token.value) # check node types after advancing
                            self.advance()
                            if self.current_token.type == ',':
                                self.advance()
                                index1 = self.parseExpr()
                                if self.current_token.type == ',':
                                    self.advance()
                                    index2 = self.parseExpr()
                                    if self.current_token.type == ')':
                                        self.advance()
                                        return VarDecNode(None, datatype, name, CleaveNode(cleave_id, index1, index2))
                    elif self.current_token.type == 'dismantle':
                        self.advance()
                        if self.current_token.type == '(':
                            self.advance()
                            dismantle_id = IdNode(self.current_token.value)
                            self.advance()
                            if self.current_token.type == ',':
                                self.advance()
                                delimiter = StringNode(self.current_token.value)
                                self.advance()
                                if self.current_token.type == ')':
                                    self.advance()
                                    return VarDecNode(None, datatype, name, DismantleNode(dismantle_id, delimiter))
                    elif self.current_token.type == 'len':
                        self.advance()
                        if self.current_token.type == '(':
                            self.advance()
                            len_id = IdNode(self.current_token.value)
                            self.advance()
                            if self.current_token.type == ')':
                                self.advance()
                                return VarDecNode(None, datatype, name, LenNode(len_id))
                    else:
                        value = self.parseExpr()
                        return VarDecNode(None, datatype, name, value)
                elif self.current_token.type == '[':
                    self.advance()
                    size = self.parseExpr()
                    clan_size_node = ClanSizeNode(size)
                    if self.current_token.type == ']':
                        self.advance()
                        initial_values = []
                        if self.current_token.type == '=':
                            self.advance()
                            if self.current_token.type == '{':
                                self.advance()
                                while self.current_token.type != '}':
                                    initial_values.append(self.parseExpr())
                                    if self.current_token.type == ',':
                                        self.advance()
                                self.advance()
                        return ClanDecNode(None, datatype, name, clan_size_node, initial_values)
                elif self.current_token.type == '[...]':
                    self.advance()
                    size = self.parseExpr()
                    clan_size_node = ClanSizeNode(size)
                    initial_values = []
                    if self.current_token.type == '=':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            while self.current_token.type != '}':
                                initial_values.append(self.parseExpr())
                                if self.current_token.type == ',':
                                    self.advance()
                            self.advance()
                    return ClanDecNode(None, datatype, name, clan_size_node, initial_values)
                else:
                    return VarNode(name)
        elif self.current_token.type == 'curse':
            self.advance()
            if self.current_token.type == 'id':
                name = self.current_token.value
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    parameters = []
                    while self.current_token.type != ')':
                        param_type = self.current_token.type
                        self.advance()
                        param_name = self.current_token.value
                        self.advance()
                        param_node = ParamNode(param_type, param_name)
                        parameters.append(param_node)
                        if self.current_token.type == ',':
                            self.advance()
                    self.advance()
                    if self.current_token.type == '{':
                        self.advance()
                        body = self.parseBody()
                        return CurseDecNode(None, name, parameters, body)
            elif self.current_token.type == 'domain':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            body = self.parseBody()
                            return CurseDomainNode(body)
        elif self.current_token.type == 'restrict':
            self.advance()
            if self.current_token.type in ['int', 'float', 'string', 'bool']:
                datatype = self.current_token.type
                self.advance()
                if self.current_token.type == 'id':
                    name = self.current_token.value
                    self.advance()
                    if self.current_token.type == '=':
                        self.advance()
                        value = self.parseExpr()
                        return VarDecNode('restrict', datatype, name, value)
        return None
    
    def parseBody(self):
        body = BodyNode()
        while self.current_token.type != '}':
            if self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                declaration = self.parseDeclaration()
                if declaration:
                    body.add_child(declaration)
            elif self.current_token.type == 'id':
                assignment = self.parseIdCall()
                if assignment:
                    body.add_child(assignment)
            elif self.current_token.type == 'invoke':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    value = self.parseInvokeArgument()
                    if self.current_token.type == ')':
                        self.advance()
                        body.add_child(InvokeNode(value))
            elif self.current_token.type == 'capture':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    if self.current_token.type == 'id':
                        name = IdNode(self.current_token.value)
                        self.advance()
                        if self.current_token.type == ')':
                            self.advance()
                            body.add_child(CaptureNode(name))
            elif self.current_token.type == 'dismiss':
                self.advance()
                body.add_child(DismissNode())
            elif self.current_token.type == 'hop':
                self.advance()
                body.add_child(HopNode())
            elif self.current_token.type == 'recall': # check later for all possibilities
                self.advance()
                value = self.parseExpr()
                body.add_child(RecallNode(value))
            elif self.current_token.type == 'vow':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    condition = self.parseExpr()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            body_node = self.parseBody()
                            self.advance()  # advance past the closing brace '}'
                            else_vows = []
                            while self.current_token.type == 'else' and self.peek().type == 'vow':
                                self.advance()
                                self.advance()
                                if self.current_token.type == '(':
                                    self.advance()
                                    else_condition = self.parseExpr()
                                    if self.current_token.type == ')':
                                        self.advance()
                                        if self.current_token.type == '{':
                                            self.advance()
                                            else_body_node = self.parseBody()
                                            self.advance()  # Advance past the closing '}'
                                            else_vows.append(ElseVow(else_condition, else_body_node))
                            if self.current_token.type == 'else':
                                self.advance()
                                if self.current_token.type == '{':
                                    self.advance()
                                    else_body_node = self.parseBody()
                                    self.advance()  # Advance past the closing '}'
                                    body.add_child(VowNode(condition, body_node, else_vows, ElseNode(else_body_node)))
                            else:
                                body.add_child(VowNode(condition, body_node, else_vows))
            else:
                self.advance()
        return body

    def parseInvokeArgument(self):
        if self.current_token.type == 'string_literal':
            return self.parseString()
        else:
            return self.parseExpr()

    def parseString(self):
        left = StringNode(self.current_token.value)
        self.advance()
        while self.current_token.type == '+':
            op = self.current_token
            self.advance()
            if self.current_token.type == 'string_literal':
                right = StringNode(self.current_token.value)
                self.advance()
            else:
                right = self.parseFactor()
            left = StringConcatNode(left, op, right)
        return left

def is_non_terminal(text): # (boolean) checks if the given string is a non-terminal
    return text.startswith('<') and text.endswith('>')

def parse_run(tokens):
    parser = Parser(tokens)
    error = parser.syntax_analyzer()
    ast = parser.build_ast()
    if ast:
        ast.print_tree()
    else:
        print("No AST built")
    
    if error:
        print(error)
        return error, None
    return "Successful from Syntax Analyzer", ast