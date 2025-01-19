##############
# IMPORTS
##############
from lexer import run as lexer_run

############## 
# CONSTANTS 
##############

CFG = {
    "<program>": [              
        ["expansion", ";", "<global_dec>"] ########### 1 
    ],
    "<global_dec>": [           
        ["<global_type_dec>", "<global_dec>"],
        ["<restrict_dec>", "<datatype>", "id", "<type_choice>", "<global_dec>"],
        []
    ],
    
    "<global_type_dec>": [
        ["<datatype>", "<nonvoid_curse_opt>", "id", "<type_choice>"], ########### 
        ["<void_curse_dec>"], ###########
    ],
    "<restrict_dec>": [
        ["restrict"], ###########
        []  
    ], 

    "<nonvoid_curse_opt>": [
        ["curse"],
        []
    ],

    "<type_choice>": [
        ["<var_dec>", ";"], ########### 
        ["<clan_dec>", ";"], ###########
        ["<nonvoid_curse_dec>"] ###########
    ],

    "<var_dec>": [
        ["<assign>", "<multi-assign>"], ########### 
    ],
    "<assign>": [
        ["=", "<value>"], ########### 
        []
    ],
    "<multi-assign>": [
        [",", "id", "<assign>", "<multi-assign>"],  ########### 29
        []                                   ########### 30
    ],

    "<void_curse_dec>": [
        ["curse", "<init_void_curse>"],   ########### 16
    ],

    "<init_void_curse>": [
        ["id", "(", "<param>", ")", "{", "<body>", "}"],
        ["domain", "(", ")", "{", "<body>", "}"]
    ],

    "<nonvoid_curse_dec>": [
        ["(", "<param>", ")", "{", "<body>", "<recall_statement>", "}"], ########### 31
    ],

    "<param>": [
        ["<datatype>", "id", "<more_param>"],
        []
    ],  

    "<more_param>": [
        [",", "<datatype>", "id", "<more_param>"],
        []
    ],

    "<recall_statement>": [
        ["recall", "<recall_val>", ";"],
        []
    ],

    "<recall_val>": [
        ["<literal>"],
        ["id"],
        ["<value>"]
    ],

    "<body>": [               
        ["<statement>", "<body>"],          ########### 4
        []                                      ########### 5
    ],

    "<statement>": [
        ["<local_dec>"],   ########### 
        ["<re-assign>", ";"],   ########### 
        ["<invoke_stm>", ";"],  ########### 
        ["<capture_stm>", ";"], ########### 
        ["<curse_call>", ";"],  ########### 
        ["<conditional_stm>"],  ########### 
        ["<looping_stm>"],      ########### 
        []                      ###########
    ],

    "<local_dec>": [
        ["<local_type_dec>", "<local_dec>"], ###########
        ["<restrict_dec>", "<datatype>", "id", "<type_choice>", "<local_dec>"], ###########
        []
    ],

    "<local_type_dec>": [
        ["<datatype>", "<nonvoid_curse_opt>", "id", "<type_choice>"], ###########
        ["curse", "id", "(", "<param>", ")", "{", "<body>", "}"], ###########
    ],


    "<re-assign>": [
        ["<assign_expression>"],                ########### 20
        []                                   ########### 21
    ],

    "<value>": [
        ["<literal>"],                          ########### 31         
        ["id"],                                 ########### 32
        ["<arith_expression>"],                 ########### 33
        ["<relational_expression>"],            ########### 34
        ["<logic_expression>"],                 ########### 35
        ["<string_concat>"],                    ########### 36
        ["<clan_access>"],                      ########### 37
        ["<string_access>"],                    ########### 38
        ["<curse_call>"],                       ########### 39
        ["<length>"],                           ########### 40
        ["<dismantle>"],                        ########### 41
        ["<cleave>"],                           ########### 42
        []                                   ########### 43
    ],
    "<clan_dec>": [
        ["<clan_size>", "<clan_assign>"]    ########### 44
    ],
    "<clan_size>": [
        ["[", "int_literal", "]", "<two_dimensional>"],  ########### 45
        ["[...]"]  ########### 46
    ],
    "<two_dimensional>": [
        ["[", "int_literal", "]", "<two_dimensional>"], ########### 46
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
        ["<literal>", "<clan_multi_item>", "<clan_item>"],  ########### 51
        ["{", "<literal>", "<clan_multi_item>", "}", "<more_item>"],  ########### 52
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
    "<invoke_stm>": [
        ["invoke", "(", "<arguments>", ")"]         ########### 71
    ],
    "<capture_stm>": [
        ["capture", "(", "id", ")"]             ########### 72
    ],
    "<conditional_stm>": [
        ["<vow_statement>"],                    ########### 73
        ["<boogie_woogie_statement>"],          ########### 74
        ["<boogie_true_statement>"]             ########### 75
    ],
    "<vow_statement>": [
        ["vow", "(", "<vow_conditions>", ")", "{", "<con_loop_body>", "}", "<vow_next>"]  ########### 76
    ],
    "<vow_next>": [
        ["<vow_else>"],                         ########### 77
        ["<vow_ladder>"],                       ########### 78
        []                                   ########### 79                     
    ],
    "<vow_else>": [
        ["else{", "<statement>", "<recall_statement>", "}"],    ########### 80
        []                                   ########### 81
    ],
    "<vow_ladder>": [
        ["else vow(", "vow_conditions", "){", "<statement>", "<recall_statement>", "}", "<more_vow_else>", "<vow_else>"],   ########### 82
        []                                   ########### 83
    ],
    "<more_vow_else>": [
        ["else vow(", "<vow_conditions>", "){", "<con_loop_body>", "}", "<more_vow_else>"], ########### 84
        []                                   ########### 85             
    ],
    "<vow_conditions>": [
        ["id"],                                 ########### 86
        ["<relational_expression>"],            ########### 87
        ["<logic_expression>"],                 ########### 88
        ["id == bool_literal"],                 ########### 89
        ["<not_logic_op>", "id"],               ########### 90
        ["<not_logic_op>", "(", "<relational_expression>", ")"],    ########### 91
        ["<not_logic_op>", "(", "<logic_expression>", ")"],         ########### 92
        ["<not_logic_op>", "(", "id == bool_literal", ")"],         ########### 93
        ["<not_logic_op>", "(", "<vow_conditions>", ")"]            ########### 94
    ],
    "<boogie_woogie_statement>": [              ########### 95
        ["boogie", "(", "<control_var>", ")", "{", "woogie", "<constant>", ":", "<con_loop_body>", "<control_flow>", "<more_woogie>", "default:", "<statement>", "}"]
    ],
    "<constant>": [
        ["<literal>"]                           ########### 96
    ],
    "<more_woogie>": [
        ["woogie", "<constant>", ":", "<statement>", "<control_flow>", "<more_woogie>"],    ########### 97
        []                                   ########### 98
    ],
    "<boogie_true_statement>": [                ########### 99
        ["boogie", "{", "woogie", "(", "<woogie_sustain_condition>", ")", ":", "<con_loop_body>", "<control_flow>", "<more_true_woogie>", "default:", "<statement>", "}"]
    ],
    "<more_true_woogie>": [                     
        ["woogie", "(", "<woogie_sustain_condition>", ")", ":", "<statement>", "<control_flow>", "<more_true_woogie>"], ########### 100
        []                                   ########### 101
    ],
    "<control_var>": [
        ["id"]                                  ########### 102
    ],
    "<woogie_sustain_condition>": [
        ["id"],                                 ########### 103
        ["<relational_expression>"],            ########### 104
        ["<logic_expression>"],                 ########### 105  
        ["id == <bool_literal>"],               ########### 106
        ["<not_logic_op>", "id"],               ########### 107
        ["<not_logic_op>", "(", "<relational_expression>", ")"],    ########### 108
        ["<not_logic_op>", "(", "<logic_expression>", ")"],         ########### 109
        ["<not_logic_op>", "(", "id == <bool_literal>", ")"],       ########### 110
        ["<not_logic_op>", "(", "<vow_conditions>", ")"]            ########### 111
    ],
    "<control_flow>": [
        ["dismiss",";"],                        ########### 112
        ["hop",";"],                            ########### 113
        []                                   ########### 114
    ],
    "<looping_stm>": [
        ["<sustain-loop>"],                     ########### 115
        ["<persustain-loop>"],                  ########### 116
        ["<cycle-loop>"]                        ########### 117
    ],
    "<cycle-loop>": [
        ["cycle","(", "<cycle_initialize>", ";", "<cycle_condition>", ";", "<iteration>", ")","{", "<con_loop_body>", "}"]    ########### 118
    ],
    "<cycle_initialize>": [
        ["id", "=", "<cycle_ini_val>"],           ########### 119
        ["<datatype>", "id", "=", "<cycle_ini_val>"]  ########### 120
    ],
    "<cycle_ini_val>": [
        ["id"],                                 ########### 121
        ["int_literal"],                        ########### 122
        ["<arith_expression>"]                  ########### 123
    ],
    "<cycle_condition>": [
        ["<relational_expression>"],            ########### 124
        ["<not_logic_op>", "(", "<relational_expression>", ")"],    ########### 125
        ["<not_logic_op>", "(", "<cycle_condition>", ")"]        ########### 126
    ],
    "<iteration>": [
        ["<unary_expression>"]                  ########### 127
    ],
    "<sustain-loop>": [
        ["sustain (", "<woogie_sustain_condition>", "){", "<con_loop_body>", "}"]   ########### 128
    ],
    "<persustain-loop>": [
        ["perform {", "<con_loop_body>", "} sustain(", "<woogie_sustain_condition>", ")"]   ########### 129
    ],
    "<con_loop_body>": [
        ["<var_dec>", ";", "<con_loop_body>"],      ########### 130
        ["<restrict_dec>", ";", "<con_loop_body>"], ########### 131
        ["<re-assign>", ";", "<con_loop_body>"],    ########### 132
        ["<expression>", ";", "<con_loop_body>"],   ########### 133
        ["<invoke_stm>", ";", "<con_loop_body>"],   ########### 134
        ["<capture_stm>", ";", "<con_loop_body>"],  ########### 135
        ["<curse_call>", ";", "<con_loop_body>"],   ########### 136
        ["<recall_statement>", ";", "<con_loop_body>"], ########### 137
        ["<conditional_stm>", "<con_loop_body>"],   ########### 138
        ["<con_loop_body>", "<con_loop_body>"],     ########### 139                         
        []                                       ########### 140
    ],
    "<expressions>": [
        ["<assign_expression>"],                    ########### 141
        ["<unary_expression>"],                     ########### 142
        ["<relational_expression>"],                ########### 143
        ["<arith_expression>"],                     ########### 144
        ["<logic_expression>"],                     ########### 145
        []                                       ########### 146
    ],
    "<assign_expression>": [
        ["<assign_left_operand>", "<assign_op>", "<assign_right_operand>"]  ########### 147
    ],
    "<assign_left_operand>": [
        ["id"],                                     ########### 148
        ["<clan_access>"],                          ########### 149
        ["<string_access>"]                         ########### 150
    ],
    "<assign_right_operand>": [
        ["id"],                                     ########### 151
        ["<literal>"],                              ########### 152       
        ["<length>"],                               ########### 153              
        ["<relational_expression>"],                ########### 154
        ["<logic_expression>"],                     ########### 155
        ["<arith_expression>"],                     ########### 156
        ["<curse_call>"]                            ########### 157
    ],  
    "<assign_op>": [
        ["="],                                      ########### 158
        ["+="],                                     ########### 159
        ["-="],                                     ########### 160
        ["*="],                                     ########### 161
        ["/="]                                      ########### 162                           
    ],
    "<unary_expression>": [
        ["<prefix_unary_expression>"],              ########### 163
        ["<postfix_unary_expression>"]              ########### 164
    ],
    "<prefix_unary_expression>": [
        ["<unary_op>", "<unary_operand>"]           ########### 165
    ],
    "<postfix_unary_expression>": [
        ["<unary_operand>", "<unary_op>"]           ########### 166
    ],
    "<unary_operand>": [
        ["id"]                                      ########### 167
    ],
    "<unary_op>": [
        ["++"],                                     ########### 168
        ["--"]                                      ########### 169
    ],
    "<arith_expression>": [
        ["<arith_operand>", "<arith_op>", "<arith_operand>", "<more_arith>"],   ########### 170
        ["(", "<paren_arith_expression>", ")"]      ########### 171
    ],
    "<paren_arith_expression>": [
        ["<arith_expression>"]                      ########### 172
    ],
    "<arith_operand>": [
        ["(", "<paren_arith_operand>", ")"],        ########### 173
        ["id"],                                     ########### 174 
        ["int_literal"],                            ########### 175
        ["float_literal"],                          ########### 176
        ["<curse_call>"]                            ########### 177
    ],
    "<arith_operand>": [
        ["<clan_access>"],                          ########### 178
        ["<arith_expression>"]                      ########### 179
    ],
    "<paren_arith_operand>": [
        ["<arith_operand>"]                         ########### 180
    ],
    "<more_arith>": [
        ["<arith_op>", "<arith_operand>", "<more_arith>"],  ########### 181
        []                                       ########### 182
    ],
    "<arith_op>": [
        ["+"],                                      ########### 183                       
        ["-"],                                      ########### 184                       
        ["*", "<pow>"],                             ########### 185
        ["/"],                                      ########### 186           
        ["%"]                                       ########### 187
    ],
    "<pow>": [
        ["*"],                                      ########### 188                       
        []                                       ########### 189                                
    ],
    "<relational_expression>": [
        ["<relational_operand>", "<relational_op>", "<relational_operand>"],    ########### 190
        ["(", "<paren_relational_expression>", ")"] ########### 191
    ],
    "<paren_relational_expression>": [
        ["<relational_expression>"]                 ########### 192
    ],
    "<relational_operand>": [
        ["(", "<paren_relational_operand>", ")"],   ########### 193    
        ["id"],                                     ########### 194    
        ["<literal>"],                              ########### 195               
        ["<clan_access>"],                          ########### 196               
        ["<length>"],                               ########### 197                
        ["<curse_call>"],                           ########### 198            
        ["<arith_expression>"]                      ########### 199       
    ],
    "<paren_relational_operand>": [
        ["<relational_operand>"]                    ########### 200
    ],
    "<relational_op>": [
        ["=="],                                     ########### 201
        ["!="],                                     ########### 202    
        [">"],                                      ########### 203
        ["<"],                                      ########### 204
        [">="],                                     ########### 205          
        ["<="]                                      ########### 206                   
    ],
    "<logic_expression>": [
        ["<not_logic_operand>", "<logic_op>", "<not_logic_operand>", "<more_logic>"],   ########### 207
        ["(", "<paren_logic_expression>", ")"],     ########### 208
        ["<not_logic_op>", "(", "<logic_expression>", ")"]  ########### 209
    ],
    "<paren_logic_expression>": [
        ["<logic_expression>"]                      ########## 210
    ],
    "<not_logic_operand>": [
        ["<not_logic_op>", "<logic_operand>"]       ########### 211
    ],
    "<logic_operand>": [
        ["(", "<not_logic_operand>", ")"],          ########### 212
        ["id"],                                     ########### 213
        ["bool_literal"],                           ########### 214
        ["<curse_call>"],                           ########### 215
        ["<relational_expression>"]                 ########### 216
    ],
    "<more_logic>": [
        ["<logic_op>", "<not_logic_operand>", "<more_logic>"],  ########### 217
        []                                       ########### 218
    ],
    "<logic_op>": [
        ["&&"],                                     ########### 219
        ["||"]                                      ########### 220
    ],
    "<not_logic_op>": [
        ["!", "<more_not>"],                        ########### 221
        []                                       ########### 222
    ],  
    "<more_not>": [
        ["<not_logic_op>"]                          ########### 223
    ],
    "<string_concat>": [
        ["string_literal", "+", "<string_concat>"], ########### 224
        ["string_literal"]                          ########### 225
    ],
    "<literal>": [
        ["int_literal"],                            ########### 
        ["string_literal"],                         ########### 226
        ["bool_literal"],                           ########### 227
        ["float_literal"],                          ########### 228
        ["null_literal"],                           ########### 229
        []                                       ########### 230
    ],
    "<curse_call>": [
        ["id", "(", "<arguments>", ")"]             ########### 231
    ],
    "<arguments>": [
        ["<value>", "<more_arguments>"],            ########### 232
        ["id", "<more_arguments>"],                 ########### 233
        []                                       ########### 234
    ],
    "<more_arguments>": [
        [",", "<arguments>"],                       ########### 235
        []                                       ########### 236
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
    "<datatype>": [
        ["int"],                                    ########### 254
        ["float"],                                  ########### 255
        ["string"],                                 ########### 256
        ["bool"]                                    ########### 257 
    ]
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
        "restrict": ["<global_dec>", 1],
        "Ø": ["<global_dec>", 2]
    }, 

    "<global_type_dec>": {
        "int": ["<global_type_dec>", 0],
        "float": ["<global_type_dec>", 0],
        "string": ["<global_type_dec>", 0],
        "bool": ["<global_type_dec>", 0],
        "curse": ["<global_type_dec>", 1]
    },

    "<restrict_dec>": {
        "restrict": ["<restrict_dec>", 0],
        "int": ["<restrict_dec>", 1],
        "string": ["<restrict_dec>", 1],
        "float": ["<restrict_dec>", 1],
        "bool": ["<restrict_dec>", 1],
        "Ø": ["<restrict_dec>", 1]
    },

    "<nonvoid_curse_opt>": {
        "curse": ["<nonvoid_curse_opt>", 0],
        "id": ["<nonvoid_curse_opt>", 1],
        "restrict": ["<nonvoid_curse_opt>", 1],
        "Ø": ["<nonvoid_curse_opt>", 1]
    },

     "<type_choice>": {
        "=": ["<type_choice>", 0],
        ",": ["<type_choice>", 0],
        ";": ["<type_choice>", 0],
        "[": ["<type_choice>", 1],
        "[...]": ["<type_choice>", 1],
        "(": ["<type_choice>", 2]
    },

    "<var_dec>": {
        "=": ["<var_dec>", 0],
        ",": ["<var_dec>", 0],
        ";": ["<var_dec>", 0],
    },

    "<assign>": {
        "=": ["<assign>", 0],
        ";": ["<assign>", 1],
        "Ø": ["<assign>", 1]
    },

    "<multi-assign>": {
        ",": ["<multi-assign>", 0],
        ";": ["<multi-assign>", 1],
        "Ø": ["<multi-assign>", 1]
    },

    "<void_curse_dec>": {
        "curse": ["<void_curse_dec>", 0],
    },

    "<nonvoid_curse_dec>": {
        "(": ["<nonvoid_curse_dec>", 0]
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
        "Ø": ["<param>", 1]
    },

    "<more_param>": {
        ",": ["<more_param>", 0],
        ")": ["<more_param>", 1],
        "Ø": ["<more_param>", 1]
    },

    "<recall_statement>": {
        "recall": ["<recall_statement>", 0],
        "Ø": ["<recall_statement>", 1]
    },

    "<recall_val>": {
        "string_literal": ["<recall_val>", 0],
        "int_literal": ["<recall_val>", 0],
        "bool_literal": ["<recall_val>", 0],
        "float_literal": ["<recall_val>", 0],
        "(" : ["<recall_val>", 0], #FIXME Ambiguity for '('
        "id": ["<recall_val>", 1],
        "Ø": ["<recall_val>", 2]
    },

    "<body>": {
        "int": ["<body>", 0],
        "string": ["<body>", 0],
        "float": ["<body>", 0],
        "bool": ["<body>", 0],
        "curse": ["<body>", 0],
        "restrict": ["<body>", 0],
        "id": ["<body>", 0],
        #"len": ["<body>", 0],
        "invoke": ["<body>", 0],
        "capture": ["<body>", 0],
        "vow": ["<body>", 0],
        "boogie": ["<body>", 0],
        "cycle": ["<body>", 0],
        "sustain": ["<body>", 0],
        "perform": ["<body>", 0],
        "recall": ["<body>", 1],
        "}": ["<body>", 1],
        ";": ["<body>", 1],
        "Ø": ["<body>", 1]
    },

    "<statement>": {
        "int": ["<statement>", 0], 
        "string": ["<statement>", 0], 
        "float": ["<statement>", 0],
        "bool": ["<statement>", 0],
        "curse": ["<statement>", 0],
        "restrict": ["<statement>", 0],
        "id": ["<statement>", 1],
        "invoke": ["<statement>", 2],
        "capture": ["<statement>",3],
        "vow": ["<statement>", 5],
        "boogie": ["<statement>", 6],
        "cycle": ["<statement>", 6],
        "sustain": ["<statement>", 6],
        "perform": ["<statement>", 6],
        "recall": ["<statement>", 7],
        "}": ["<statement>", 7],
        "Ø": ["<statement>", 7]
    },

    "<local_dec>": {
        "int": ["<local_dec>", 0],
        "string": ["<local_dec>", 0],
        "float": ["<local_dec>", 0],
        "bool": ["<local_dec>", 0],
        "curse": ["<local_dec>",0],
        "restrict": ["<local_dec>", 1],
        "}": ["<local_dec>", 2],
        ";": ["<local_dec>", 2],
        "Ø": ["<local_dec>", 2]
    },
    
    "<local_type_dec>": {
        "int": ["<local_type_dec>", 0],
        "string": ["<local_type_dec>", 0],
        "float": ["<local_type_dec>", 0],
        "bool": ["<local_type_dec>", 0],
        "curse": ["<local_type_dec>", 1]
    },

    "<re-assign>": {
        "id": ["<re-assign>", 0],
        "Ø": ["<re-assign>", 1]
    },

    "<multi-assign>": { ############# 9 in First Set
        ",": ["<multi-assign>", 0],
        ";": ["<multi-assign>", 1],
        "Ø": ["<multi-assign>", 1]
    },
    
    "<var_dec_syntax>": { ############# 19 in First Set
        "int": ["<var_dec_syntax>", 0],
        "float": ["<var_dec_syntax>", 0],
        "string": ["<var_dec_syntax>", 0],
        "bool": ["<var_dec_syntax>", 0],
        "id": ["<var_dec_syntax>", 1]
    },

    "<assign>": { ############# 
        "=": ["<assign>", 0],
        "Ø": ["<assign>", 1],
        ",": ["<assign>", 1],
        ";": ["<assign>", 1]
    },

    "<invoke_stm>": { ############# 25 in First Set
        "invoke": ["<invoke_stm>", 0]
    },

    "<capture_stm>": { ############# 26 in First Set
        "capture": ["<capture_stm>", 0]
    },

    "<conditional_stm>": { ############# 27 in First Set
        "vow": ["<conditional_stm>", 0],
        "boogie": ["<conditional_stm>", 1],
    },

    "<vow_statement>": { ############# 28 in First Set
        "vow": ["<vow_statement>", 0]
    },

    "<vow_next>": { ############# 29 in First Set
        "else": ["<vow_next>", 0], #FIXME Ambiguity for 'else'
        "Ø": ["<vow_next>", 2]
    },

    "<vow_else>": { ############# 30 in First Set
        "else": ["<vow_else>", 0], #FIXME Ambiguity for 'else'
        "Ø": ["<vow_else>", 1]
    },

    "<vow_ladder>": { ############# 31 in First Set
        "else": ["<vow_ladder>", 0], #FIXME Ambiguity for 'else'
        "Ø": ["<vow_ladder>", 1]
    },

    "<more_vow_else>": { ############# 32 in First Set
        "else": ["<more_vow_else>", 0], #FIXME Ambiguity for 'else'
        "Ø": ["<more_vow_else>", 1]
    },

    "<vow_conditions>": { ############# 33 in First Set
        "id": ["<vow_conditions>", 0],
        "(": ["<vow_conditions>", 1],
        "string_literal": ["<vow_conditions>", 6], # FIXME Ambiguity for vow_conditions T_T this whole thing
        "int_literal": ["<vow_conditions>", 6],
        "bool_literal": ["<vow_conditions>", 6],
        "float_literal": ["<vow_conditions>", 6],
        "len": ["<vow_conditions>", 6],
        "!": ["<vow_conditions>", 4],
    },

    "<value>": {    ############# 10 in First Set
        "string_literal": ["<value>", 0],
        "int_literal": ["<value>", 0],
        "bool_literal": ["<value>", 0],
        "float_literal": ["<value>", 0],
        "id": ["<value>", 1],
        "(": ["<value>", 4], ######## TEMPORARY, NEED FIX
        "!": ["<value>", 4], ######## TEMPORARY, NEED FIX
        "len": ["<value>", 9],
        "dismantle":  ["<value>", 10],
        "cleave":   ["<value>", 11],
        "Ø": ["<value>", 12]
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
         "Ø": ["<two_dimensional", 1]
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

    "<assign_expression>": { ############# 52 in First Set
        "id": ["<assign_expression>", 0]
    },
    "<assign_left_operand>": { ############# 53 in First Set
        "id": ["<assign_left_operand>", 0],
    },
    "<assign_right_operand>": { ############# 54 in First Set
        "id": ["<assign_right_operand>", 0],
        "string_literal": ["<assign_right_operand>", 1],
        "int_literal": ["<assign_right_operand>", 1],
        "bool_literal": ["<assign_right_operand>", 1],
        "float_literal": ["<assign_right_operand>", 1],
        "len": ["<assign_right_operand>", 2],
        "!": ["<assign_right_operand>", 4],
        "(": ["<assign_right_operand>", 5], #FIXME Ambiguity for '('
        "++": ["<assign_right_operand>", 6],
        "--": ["<assign_right_operand>", 6],
        "curse": ["<assign_right_operand>", 7]
    },
    "<assign_op>": { ############# 55 in First Set
        "=": ["<assign_op>", 0],
        "+=": ["<assign_op>", 1],
        "-=": ["<assign_op>", 2],
        "*=": ["<assign_op>", 3],
        "/=": ["<assign_op>", 4]
    },

    "<curse_dec>": { ############# 57 in First Set
        "curse": ["<curse_dec>", 0],
        "int": ["<curse_dec>", 1],
        "string": ["<curse_dec>", 1],
        "float": ["<curse_dec>", 1],
        "bool": ["<curse_dec>", 1],
        "Ø": ["<curse_dec>", 2]
    },

    "<relational_expression>": { ############# 68 in First Set
        "(": ["<relational_expression>", 1],
        "id": ["<relational_expression>", 0],
        "string_literal": ["<relational_expression>", 0],
        "int_literal": ["<relational_expression>", 0],
        #"bool_literal": ["<relational_expression>", 2],
        "float_literal": ["<relational_expression>", 0],
        "len": ["<relational_expression>", 0]
    },

    "<relational_operand>": { ############# 70 
        "(": ["<relational_operand>", 0],
        "id": ["<relational_operand>", 1],
        "string_literal": ["<relational_operand>", 2],
        "int_literal": ["<relational_operand>", 2],
        "bool_literal": ["<relational_operand>", 2],
        "float_literal": ["<relational_operand>", 2],
        "len": ["<relational_operand>", 4] #FIXME Missing in First Set: curse_call, clan_access, length
    },

    "<relational_op>": { ############# 71 in First Set
        "==": ["<relational_op>", 0],
        "!=": ["<relational_op>", 1],
        ">": ["<relational_op>", 2],
        "<": ["<relational_op>", 3],
        ">=": ["<relational_op>", 4],
        "<=": ["<relational_op>", 5]
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

    "<arguments>": { ############# 
        "string_literal": ["<arguments>", 0],
        "int_literal": ["<arguments>", 0],
        "bool_literal": ["<arguments>", 0],
        "float_literal": ["<arguments>", 0],
        "id": ["<arguments>", 1],
        "(": ["<arguments>", 0],
        "!": ["<arguments>", 0],
        ")": ["<arguments>", 2],
        "Ø": ["<arguments>", 2]
    },

    "<more_arguments>": { #############   
        ",": ["<more_arguments>", 0],
        ")": ["<more_arguments>", 1],
        "Ø": ["<more_arguments>", 1]
    },

    "<datatype>": { ############# 97 in first set
        "int": ["<datatype>", 0],
        "float": ["<datatype>", 1],
        "string": ["<datatype>", 2],
        "bool": ["<datatype>", 3]
    }
}


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
        errors = []

        while stack:
            top = stack[-1]
            print(f"1. Stack: {stack}")
            if self.current_token is None:
                self.current_token = type('Token', (object,), {'type': 'Ø'})()
                
            print(f"2. Current Token: {self.current_token.type}")

            if is_non_terminal(top):
                # Check what production to use by checking the top of the stack and the current token
                production_key = PREDICT_SET[top][self.current_token.type]
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
                        errors.append(f"Syntax Error: No production rule for '{production}'")
                        break
                else:
                    errors.append(f"Syntax Error: No prediction for '{production_key}'")
                    break
            else:
                # Check if the top of the stack is equal to the current token
                if top == self.current_token.type:
                    stack.pop()  # Remove the terminal from the stack
                    print(f"2. Matched Terminal: {top}")
                    self.advance()  # Move to the next token
                else:
                    errors.append(f"Syntax Error: Expected '{top}' but found '{self.current_token.type}'")
                    break

        if errors:
            return errors
        return []

def is_non_terminal(text):
    return text.startswith('<') and text.endswith('>')

def parse_run(tokens):
    parser = Parser(tokens)
    errors = parser.parse()
    if errors:
        for err in errors:
            print(err)
        return "Failure from Syntax Analyzer"
    return "Successful from Syntax Analyzer"