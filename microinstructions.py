
# JAM encoding
#   JMPC JAMN JAMZ
#    4    2    1

# C-BUS encoding
#    H | OPC TOS CPP LV  | SP  PC  MDR MAR
#    1 |  8   4   2   1  |  8   4   2   1

# MEM encoding
#   write read fetch
#     4    2     1

# B-BUS encoding
# 0    -> MDR
# 1    -> PC
# 2    -> MBR
# 3    -> MBRU
# 4    -> SP
# 5    -> LV
# 6    -> CPP
# 7    -> TOS
# 8    -> OPC
# 9-15 -> none

control_store = {
#   this     next
#   addr.    addr.  JAM  ALU   C-BUS  MEM  B-BUS     name                 MAL                                        explanation
    0x100 : [0x000, 0x4, 0x35, 0x004, 0x1, 0x1,     "Main1"          ,   "PC = PC + 1; fetch; goto (MBR)"         , "MBR holds opcode; get next byte; dispatch"      ],
    0x000 : [0x100, 0x0, 0x00, 0x000, 0x0, 0x9,     "nop1"           ,   "goto Main1"                             , "Do nothing"                                     ],
    0x060 : [0x061, 0x0, 0x36, 0x009, 0x2, 0x4,     "iadd1"          ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word on stack"              ],
    0x061 : [0x062, 0x0, 0x14, 0x100, 0x0, 0x7,     "iadd2"          ,   "H = TOS"                                , "H = top of stack"                               ],
    0x062 : [0x100, 0x0, 0x3C, 0x042, 0x4, 0x0,     "iadd3"          ,   "MDR = TOS = MDR + H; wr; goto Main1"    , "Add top two words; write to top of stack"       ],
    0x064 : [0x065, 0x0, 0x36, 0x009, 0x2, 0x4,     "isub1"          ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word on stack"              ],
    0x065 : [0x066, 0x0, 0x14, 0x100, 0x0, 0x7,     "isub2"          ,   "H = TOS"                                , "H = top of stack"                               ],
    0x066 : [0x100, 0x0, 0x3F, 0x042, 0x4, 0x0,     "isub3"          ,   "MDR = TOS = MDR - H; wr; goto Main1"    , "Do subtraction; write to top of stack"          ],
    0x07E : [0x07D, 0x0, 0x36, 0x009, 0x2, 0x4,     "iand1"          ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word on stack"              ],
    0x07D : [0x07C, 0x0, 0x14, 0x100, 0x0, 0x7,     "iand2"          ,   "H = TOS"                                , "H = top of stack"                               ],
    0x07C : [0x100, 0x0, 0x0C, 0x042, 0x4, 0x0,     "iand3"          ,   "MDR = TOS = MDR AND H; wr; goto Main1"  , "Do AND; write to new top of stack"              ],
    0x080 : [0x081, 0x0, 0x36, 0x009, 0x2, 0x4,     "ior1"           ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word on stack"              ],
    0x081 : [0x082, 0x0, 0x14, 0x100, 0x0, 0x7,     "ior2"           ,   "H = TOS"                                , "H = top of stack"                               ],
    0x082 : [0x100, 0x0, 0x1C, 0x042, 0x4, 0x0,     "ior3"           ,   "MDR = TOS = MDR OR H; wr; goto Main1"   , "Do OR; write to new top of stack"               ],
    0x059 : [0x058, 0x0, 0x35, 0x009, 0x0, 0x4,     "dup1"           ,   "MAR = SP = SP + 1"                      , "Increment SP and copy to MAR"                   ],
    0x058 : [0x100, 0x0, 0x14, 0x002, 0x4, 0x7,     "dup2"           ,   "MDR = TOS; wr; goto Main1"              , "Write new stack word"                           ],
    0x057 : [0x056, 0x0, 0x36, 0x009, 0x2, 0x4,     "pop1"           ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word on stack"              ],
    0x056 : [0x055, 0x0, 0x00, 0x000, 0x0, 0x9,     "pop2"           ,   "NOP"                                    , "Wait for new TOS to be read from memory"        ],
    0x055 : [0x100, 0x0, 0x14, 0x040, 0x0, 0x0,     "pop3"           ,   "TOS = MDR; goto Main1"                  , "Copy new word to TOS"                           ],
    0x05F : [0x05E, 0x0, 0x36, 0x001, 0x2, 0x4,     "swap1"          ,   "MAR = SP - 1; rd"                       , "Set MAR to SP − 1; read 2nd word from stack"    ],
    0x05E : [0x05D, 0x0, 0x14, 0x001, 0x0, 0x4,     "swap2"          ,   "MAR = SP"                               , "Set MAR to top word"                            ],
    0x05D : [0x05C, 0x0, 0x14, 0x100, 0x4, 0x0,     "swap3"          ,   "H = MDR; wr"                            , "Save TOS in H; write 2nd word to top of stack"  ],
    0x05C : [0x05B, 0x0, 0x14, 0x002, 0x0, 0x7,     "swap4"          ,   "MDR = TOS"                              , "Copy old TOS to MDR"                            ],
    0x05B : [0x05A, 0x0, 0x36, 0x001, 0x4, 0x4,     "swap5"          ,   "MAR = SP - 1; wr"                       , "Set MAR to SP − 1; write as 2nd word on stack"  ],
    0x05A : [0x100, 0x0, 0x18, 0x040, 0x0, 0x0,     "swap6"          ,   "TOS = H; goto Main1"                    , "Update TOS"                                     ],
    0x010 : [0x00F, 0x0, 0x35, 0x009, 0x0, 0x4,     "bipush1"        ,   "SP = MAR = SP + 1"                      , "MBR = the byte to push onto stack"              ],
    0x00F : [0x00E, 0x0, 0x35, 0x004, 0x1, 0x1,     "bipush2"        ,   "PC = PC + 1; fetch"                     , "Increment PC, fetch next opcode"                ],
    0x00E : [0x100, 0x0, 0x14, 0x042, 0x4, 0x2,     "bipush3"        ,   "MDR = TOS = MBR; wr; goto Main1"        , "Sign-extend constant and push on stack"         ],
    0x015 : [0x016, 0x0, 0x14, 0x100, 0x0, 0x5,     "iload1"         ,   "H = LV"                                 , "MBR contains index; copy LV to H"               ],
    0x016 : [0x017, 0x0, 0x3C, 0x001, 0x2, 0x3,     "iload2"         ,   "MAR = MBRU + H; rd"                     , "MAR = address of local variable to push"        ],
    0x017 : [0x018, 0x0, 0x35, 0x009, 0x0, 0x4,     "iload3"         ,   "MAR = SP = SP + 1"                      , "SP points to new top of stack; prepare write"   ],
    0x018 : [0x019, 0x0, 0x35, 0x004, 0x5, 0x1,     "iload4"         ,   "PC = PC + 1; fetch; wr"                 , "Inc PC; get next opcode; write top of stack"    ],
    0x019 : [0x100, 0x0, 0x14, 0x040, 0x0, 0x0,     "iload5"         ,   "TOS = MDR; goto Main1"                  , "Update TOS"                                     ],
    0x036 : [0x037, 0x0, 0x14, 0x100, 0x0, 0x5,     "istore1"        ,   "H = LV"                                 , "MBR contains index; copy LV to H"               ],
    0x037 : [0x038, 0x0, 0x3C, 0x001, 0x0, 0x3,     "istore2"        ,   "MAR = MBRU + H"                         , "MAR = address of local variable to store into"  ],
    0x038 : [0x039, 0x0, 0x14, 0x002, 0x4, 0x7,     "istore3"        ,   "MDR = TOS; wr"                          , "Copy TOS to MDR; write word"                    ],
    0x039 : [0x03A, 0x0, 0x36, 0x009, 0x2, 0x4,     "istore4"        ,   "SP = MAR = SP - 1; rd"                  , "Read in next-to-top word on stack"              ],
    0x03A : [0x03B, 0x0, 0x35, 0x004, 0x1, 0x1,     "istore5"        ,   "PC = PC + 1; fetch"                     , "Increment PC; fetch next opcode"                ],
    0x03B : [0x100, 0x0, 0x14, 0x040, 0x0, 0x0,     "istore6"        ,   "TOS = MDR; goto Main1"                  , "Update TOS"                                     ],
    # start not implemented
    0x0C4 : [0x0C5, 0x0, 0x35, 0x004, 0x1, 0x1,     "wide1"          ,   "PC = PC + 1; fetch;"                    , "Fetch operand byte or next opcode"              ],
    0x0C5 : [0x100, 0x4, 0x00, 0x000, 0x0, 0x9,     "wide2"          ,   "goto (MBR OR 0x100)"                    , "Multiway branch with high bit set"              ],
    0x115 : [0x116, 0x0, 0x35, 0x004, 0x1, 0x1,     "wide_iload1"    ,   "PC = PC + 1; fetch"                     , "MBR contains 1st index byte; fetch 2nd"         ],
    0x116 : [0x117, 0x0, 0x80, 0x100, 0x0, 0x3,     "wide_iload2"    ,   "H = MBRU << 8"                          , "H = 1st index byte shifted left 8 bits"         ],
    0x117 : [0x118, 0x0, 0x1C, 0x100, 0x0, 0x3,     "wide_iload3"    ,   "H = MBRU OR H"                          , "H = 16-bit index of local variable"             ],
    0x118 : [0x017, 0x0, 0x3C, 0x001, 0x2, 0x5,     "wide_iload4"    ,   "MAR = LV + H; rd; goto iload3"          , "MAR = address of local variable to push"        ],
    0x136 : [0x137, 0x0, 0x35, 0x004, 0x1, 0x1,     "wide_istore1"   ,   "PC = PC + 1; fetch"                     , "MBR contains 1st index byte; fetch 2nd"         ],
    0x137 : [0x138, 0x0, 0x80, 0x100, 0x0, 0x3,     "wide_istore2"   ,   "H = MBRU << 8"                          , "H = 1st index byte shifted left 8 bits"         ],
    0x138 : [0x139, 0x0, 0x1C, 0x100, 0x0, 0x3,     "wide_istore3"   ,   "H = MBRU OR H"                          , "H = 16-bit index of local variable"             ],
    0x139 : [0x038, 0x0, 0x3C, 0x001, 0x0, 0x5,     "wide_istore4"   ,   "MAR = LV + H; goto istore3"             , "MAR = address of local variable to store into"  ],
    0x013 : [0x014, 0x0, 0x35, 0x004, 0x1, 0x1,     "ldc_w1"         ,   "PC = PC + 1; fetch"                     , "MBR contains 1st index byte; fetch 2nd"         ],
    0x014 : [0x012, 0x0, 0x80, 0x100, 0x0, 0x3,     "ldc_w2"         ,   "H = MBRU << 8"                          , "H = 1st index byte << 8"                        ],
    0x012 : [0x011, 0x0, 0x1C, 0x100, 0x0, 0x3,     "ldc_w3"         ,   "H = MBRU OR H"                          , "H = 16-bit index into constant pool"            ],
    0x011 : [0x017, 0x0, 0x3C, 0x001, 0x2, 0x6,     "ldc_w4"         ,   "MAR = H + CPP; rd; goto iload3"         , "MAR = address of constant in pool"              ],
    0x084 : [0x085, 0x0, 0x14, 0x100, 0x0, 0x5,     "iinc1"          ,   "H = LV"                                 , "MBR contains index; copy LV to H"               ],
    0x085 : [0x086, 0x0, 0x3C, 0x001, 0x2, 0x3,     "iinc2"          ,   "MAR = MBRU + H; rd"                     , "Copy LV + index to MAR; read variable"          ],
    0x086 : [0x087, 0x0, 0x35, 0x004, 0x1, 0x1,     "iinc3"          ,   "PC = PC + 1; fetch"                     , "Fetch constant"                                 ],
    0x087 : [0x088, 0x0, 0x14, 0x100, 0x0, 0x0,     "iinc4"          ,   "H = MDR"                                , "Copy variable to H"                             ],
    0x088 : [0x089, 0x0, 0x35, 0x004, 0x1, 0x1,     "iinc5"          ,   "PC = PC + 1; fetch"                     , "Fetch next opcode"                              ],
    0x089 : [0x100, 0x0, 0x3C, 0x002, 0x4, 0x2,     "iinc6"          ,   "MDR = MBR + H; wr; goto Main1"          , "Put sum in MDR; update variable"                ],
    # end not implemented
    0x0A7 : [0x0A6, 0x0, 0x36, 0x080, 0x0, 0x1,     "goto1"          ,   "OPC = PC - 1"                           , "Save address of opcode."                        ],
    0x0A6 : [0x0A5, 0x0, 0x35, 0x004, 0x1, 0x1,     "goto2"          ,   "PC = PC + 1; fetch"                     , "MBR = 1st byte of offset; fetch 2nd byte"       ],
    0x0A5 : [0x0A4, 0x0, 0x80, 0x100, 0x0, 0x2,     "goto3"          ,   "H = MBR << 8"                           , "Shift and save signed first byte in H"          ],
    0x0A4 : [0x0A3, 0x0, 0x1C, 0x100, 0x0, 0x3,     "goto4"          ,   "H = MBRU OR H"                          , "H = 16-bit branch offset"                       ],
    0x0A3 : [0x0A2, 0x0, 0x3C, 0x004, 0x1, 0x8,     "goto5"          ,   "PC = OPC + H; fetch"                    , "Add offset to OPC"                              ],
    0x0A2 : [0x100, 0x0, 0x00, 0x000, 0x0, 0x9,     "goto6"          ,   "goto Main1"                             , "Wait for fetch of next opcode"                  ],
    0x09B : [0x09C, 0x0, 0x36, 0x009, 0x2, 0x4,     "iflt1"          ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word on stack"              ],
    0x09C : [0x09D, 0x0, 0x14, 0x080, 0x0, 0x7,     "iflt2"          ,   "OPC = TOS"                              , "Save TOS in OPC temporarily"                    ],
    0x09D : [0x09E, 0x0, 0x14, 0x040, 0x0, 0x0,     "iflt3"          ,   "TOS = MDR"                              , "Put new top of stack in TOS"                    ],
    0x09E : [0x050, 0x2, 0x14, 0x000, 0x0, 0x8,     "iflt4"          ,   "N = OPC; if (N) goto T; else goto F"    , "Branch on N bit"                                ],
    0x099 : [0x098, 0x0, 0x36, 0x009, 0x2, 0x4,     "ifeq1"          ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word of stack"              ],
    0x098 : [0x097, 0x0, 0x14, 0x080, 0x0, 0x7,     "ifeq2"          ,   "OPC = TOS"                              , "Save TOS in OPC temporarily"                    ],
    0x097 : [0x096, 0x0, 0x14, 0x040, 0x0, 0x0,     "ifeq3"          ,   "TOS = MDR"                              , "Put new top of stack in TOS"                    ],
    0x096 : [0x050, 0x1, 0x14, 0x000, 0x0, 0x8,     "ifeq4"          ,   "Z = OPC; if (Z) goto T; else goto F"    , "Branch on Z bit"                                ],
    0x09F : [0x09A, 0x0, 0x36, 0x009, 0x2, 0x4,     "if_icmpeq1"     ,   "MAR = SP = SP - 1; rd"                  , "Read in next-to-top word of stack"              ],
    0x09A : [0x095, 0x0, 0x36, 0x009, 0x0, 0x4,     "if_icmpeq2"     ,   "MAR = SP = SP - 1"                      , "Set MAR to read in new top-of-stack"            ],
    0x095 : [0x094, 0x0, 0x14, 0x100, 0x2, 0x0,     "if_icmpeq3"     ,   "H = MDR; rd"                            , "Copy second stack word to H"                    ],
    0x094 : [0x093, 0x0, 0x14, 0x080, 0x0, 0x7,     "if_icmpeq4"     ,   "OPC = TOS"                              , "Save TOS in OPC temporarily"                    ],
    0x093 : [0x092, 0x0, 0x14, 0x040, 0x0, 0x0,     "if_icmpeq5"     ,   "TOS = MDR"                              , "Put new top of stack in TOS"                    ],
    0x092 : [0x050, 0x1, 0x3F, 0x000, 0x0, 0x8,     "if_icmpeq6"     ,   "Z = OPC - H; if (Z) goto T; else goto F", "If top 2 words are equal, goto T, else goto F"  ],
    0x150 : [0x0A6, 0x0, 0x36, 0x080, 0x0, 0x1,     "T"              ,   "OPC = PC - 1; goto goto2"               , "Same as goto1; needed for target address"       ],
    0x050 : [0x051, 0x0, 0x35, 0x004, 0x0, 0x1,     "F"              ,   "PC = PC + 1"                            , "Skip first offset byte"                         ],
    0x051 : [0x052, 0x0, 0x35, 0x004, 0x1, 0x1,     "F2"             ,   "PC = PC + 1; fetch"                     , "PC now points to next opcode"                   ],
    0x052 : [0x100, 0x0, 0x00, 0x000, 0x0, 0x9,     "F3"             ,   "goto Main1"                             , "Wait for fetch of opcode"                       ],
    # start not implemented
    0x0B6 : [0x0B5, 0x0, 0x35, 0x004, 0x1, 0x1,     "invokevirtual1" ,   "PC = PC + 1; fetch"                     , "MBR = index byte 1; inc. PC, get 2nd byte"      ],
    0x0B5 : [0x0B4, 0x0, 0x80, 0x100, 0x0, 0x3,     "invokevirtual2" ,   "H = MBRU << 8"                          , "Shift and save first byte in H"                 ],
    0x0B4 : [0x0B3, 0x0, 0x1C, 0x100, 0x0, 0x3,     "invokevirtual3" ,   "H = MBRU OR H"                          , "H = offset of method pointer from CPP"          ],
    0x0B3 : [0x0B2, 0x0, 0x3C, 0x001, 0x2, 0x6,     "invokevirtual4" ,   "MAR = CPP + H; rd"                      , "Get pointer to method from CPP area"            ],
    0x0B2 : [0x0B1, 0x0, 0x35, 0x080, 0x0, 0x1,     "invokevirtual5" ,   "OPC = PC + 1"                           , "Save return PC in OPC temporarily"              ],
    0x0B1 : [0x0B0, 0x0, 0x14, 0x004, 0x1, 0x0,     "invokevirtual6" ,   "PC = MDR; fetch"                        , "PC points to new method; get param count"       ],
    0x0B0 : [0x0B7, 0x0, 0x35, 0x004, 0x1, 0x1,     "invokevirtual7" ,   "PC = PC + 1; fetch"                     , "Fetch 2nd byte of parameter count"              ],
    0x0B7 : [0x0B8, 0x0, 0x80, 0x100, 0x0, 0x3,     "invokevirtual8" ,   "H = MBRU << 8"                          , "Shift and save first byte in H"                 ],
    0x0B8 : [0x0B9, 0x0, 0x1C, 0x100, 0x0, 0x3,     "invokevirtual9" ,   "H = MBRU OR H"                          , "H = number of parameters"                       ],
    0x0B9 : [0x0BA, 0x0, 0x35, 0x004, 0x1, 0x1,     "invokevirtual10",   "PC = PC + 1; fetch"                     , "Fetch first byte of # locals"                   ],
    0x0BA : [0x0BB, 0x0, 0x3F, 0x040, 0x0, 0x4,     "invokevirtual11",   "TOS = SP - H"                           , "TOS = address of OBJREF − 1"                    ],
    0x0BB : [0x0BC, 0x0, 0x35, 0x041, 0x0, 0x7,     "invokevirtual12",   "TOS = MAR = TOS + 1"                    , "TOS = address of OBJREF (new LV)"               ],
    0x0BC : [0x0BD, 0x0, 0x35, 0x004, 0x1, 0x1,     "invokevirtual13",   "PC = PC + 1; fetch"                     , "Fetch second byte of # locals"                  ],
    0x0BD : [0x0BE, 0x0, 0x80, 0x100, 0x0, 0x3,     "invokevirtual14",   "H = MBRU << 8"                          , "Shift and save first byte in H"                 ],
    0x0BE : [0x0BF, 0x0, 0x1C, 0x100, 0x0, 0x3,     "invokevirtual15",   "H = MBRU OR H"                          , "H = # locals"                                   ],
    0x0BF : [0x0CF, 0x0, 0x3C, 0x002, 0x4, 0x4,     "invokevirtual16",   "MDR = SP + H + 1; wr"                   , "Overwrite OBJREF with link pointer"             ],
    0x0CF : [0x0CE, 0x0, 0x14, 0x009, 0x0, 0x0,     "invokevirtual17",   "MAR = SP = MDR;"                        , "Set SP, MAR to location to hold old PC"         ],
    0x0CE : [0x0CD, 0x0, 0x14, 0x002, 0x4, 0x8,     "invokevirtual18",   "MDR = OPC; wr"                          , "Save old PC above the local variables"          ],
    0x0CD : [0x0CC, 0x0, 0x35, 0x009, 0x0, 0x4,     "invokevirtual19",   "MAR = SP = SP + 1"                      , "SP points to location to hold old LV"           ],
    0x0CC : [0x0CB, 0x0, 0x14, 0x002, 0x4, 0x5,     "invokevirtual20",   "MDR = LV; wr"                           , "Save old LV above saved PC"                     ],
    0x0CB : [0x0CA, 0x0, 0x35, 0x004, 0x1, 0x1,     "invokevirtual21",   "PC = PC + 1; fetch"                     , "Fetch first opcode of new method."              ],
    0x0CA : [0x100, 0x0, 0x14, 0x010, 0x0, 0x7,     "invokevirtual22",   "LV = TOS; goto Main1"                   , "Set LV to point to LV Frame"                    ],
    0x0AC : [0x0AB, 0x0, 0x14, 0x009, 0x2, 0x5,     "ireturn1"       ,   "MAR = SP = LV; rd"                      , "Reset SP, MAR to get link pointer"              ],
    0x0AB : [0x0AA, 0x0, 0x00, 0x000, 0x0, 0x9,     "ireturn2"       ,   "NOP"                                    , "Wait for read"                                  ],
    0x0AA : [0x0A9, 0x0, 0x14, 0x010, 0x2, 0x0,     "ireturn3"       ,   "LV = MAR = MDR; rd"                     , "Set LV to link ptr; get old PC"                 ],
    0x0A9 : [0x0A8, 0x0, 0x35, 0x001, 0x0, 0x5,     "ireturn4"       ,   "MAR = LV + 1"                           , "Set MAR to read old LV"                         ],
    0x0A8 : [0x0AD, 0x0, 0x14, 0x004, 0x3, 0x0,     "ireturn5"       ,   "PC = MDR; rd; fetch"                    , "Restore PC; fetch next opcode"                  ],
    0x0AD : [0x0AE, 0x0, 0x14, 0x001, 0x0, 0x4,     "ireturn6"       ,   "MAR = SP"                               , "Set MAR to write TOS"                           ],
    0x0AE : [0x0AF, 0x0, 0x14, 0x010, 0x0, 0x0,     "ireturn7"       ,   "LV = MDR"                               , "Restore LV"                                     ],
    0x0AF : [0x100, 0x0, 0x14, 0x002, 0x4, 0x7,     "ireturn8"       ,   "MDR = TOS; wr; goto Main1 "             , "Save return value on original top of stack"     ]}
    # end not implemented

if __name__ == "__main__":
    for inst in [0x10, 0x59, 0xA7, 0x60, 0x7E, 0x99, 0x9B, 0x9F, 0x84, 0x15, 0xB6, 0x80, 0xAC, 0x36, 0x64, 0x13, 0x00, 0x57, 0x5F, 0xC4]:
        while inst != 0 and inst != 0x100:
            print(control_store[inst][6])
            inst = control_store[inst][0]
        print()
