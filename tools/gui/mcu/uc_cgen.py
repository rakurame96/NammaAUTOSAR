#
# Created on Sat Aug 13 2022 10:19:54 PM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import os

import arxml.mcu.arxml_mcu as arxml_mcu
import utils.search as search



def generate_platform_header(gui):
    cwd = os.getcwd()
    board_path = search.find_dir("board", cwd+"/submodules/MCAL/Mcu")
    platform_h = open(board_path+"/platform.h", "w")
    platform_h.write("#ifndef NAMMA_AUTOSAR_PLATFORM_H\n")
    platform_h.write("#define NAMMA_AUTOSAR_PLATFORM_H\n\n")
    platform_h.write("/* This file is autogenerated by NammaAUTOSAR builder */\n\n")
    platform_h.write("#include <"+gui.uc_info.micro+".h>\n")
    platform_h.write("#include <platform_"+gui.uc_info.micro+".h>\n")
    platform_h.write("\n\n#endif\n")
    platform_h.close()



def create_source(gui):
    cwd = os.getcwd()
    makefile = open(cwd+"/Makefile", "w")

    # PATH variables
    makefile.write("# Definitions\n")
    makefile.write("CWD := "+cwd+"\n")
    makefile.write("ROOT_PATH := "+cwd+"\n")

    mcu_board_path = search.find_dir("board", cwd+"/submodules/MCAL/Mcu")
    mcu_micro_path = mcu_board_path+"/"+gui.uc_info.micro
    makefile.write("MCU_BOARD_PATH := "+mcu_board_path+"\n")
    makefile.write("MCU_MICRO_PATH := "+mcu_micro_path+"\n")

    mcu_path = search.find_dir("Mcu", cwd+"/submodules")
    makefile.write("MCU_PATH := "+mcu_path+"\n")
    
    mcu_path = search.find_dir("EcuM", cwd+"/submodules")
    makefile.write("ECUM_PATH := "+mcu_path+"\n")

    port_path = search.find_dir("Port", cwd+"/submodules")
    makefile.write("PORT_PATH := "+port_path+"\n")

    dio_path = search.find_dir("Dio", cwd+"/submodules")
    makefile.write("DIO_PATH := "+dio_path+"\n")

    os_path = search.find_dir("Os", cwd+"/submodules")
    makefile.write("OS_PATH := "+os_path+"\n")

    os_builder_path = search.find_dir("os_builder", cwd)
    makefile.write("OS_BUILDER_PATH := "+os_builder_path+"\n")

    makefile.write("\n")

    # Include mk files
    makefile.write("# Inclusions\n")
    micro_mk = search.find_file(gui.uc_info.micro+".mk", cwd)
    makefile.write("include "+micro_mk+"\n")
    microarch_mk = search.find_file(gui.uc_info.micro_arch+".mk", cwd)
    makefile.write("include "+microarch_mk+"\n")
    makefile.write("\n")

    ################################################################
    # Temporary work around. This function needs a redesign
    app_path = search.find_dir("NammaTestApp", cwd+"/submodules")
    makefile.write("NAMMATESTAPP_PATH := "+app_path+"\n")
    mk_file = search.find_file_ext("mk", app_path)
    makefile.write("include "+mk_file+"\n")

    Mcu_mk = search.find_file("Mcu.mk", cwd+"/submodules")
    makefile.write("include "+Mcu_mk+"\n")
    EcuM_mk = search.find_file("EcuM.mk", cwd+"/submodules")
    makefile.write("include "+EcuM_mk+"\n")
    Port_mk = search.find_file("Port.mk", cwd+"/submodules")
    makefile.write("include "+Port_mk+"\n")
    Dio_mk = search.find_file("Dio.mk", cwd+"/submodules")
    makefile.write("include "+Dio_mk+"\n")

    os_objs_mk = search.find_file("os-objs.mk", cwd)
    makefile.write("include "+os_objs_mk+"\n")
    os_common_mk = search.find_file("os-common.mk", cwd)
    makefile.write("include "+os_common_mk+"\n")
    common_mk = search.find_file("common.mk", cwd)
    makefile.write("include "+common_mk+"\n")
    makefile.write("\n")
    # Temporary work around. This function needs a redesign
    ##################################################################

    # Generate micro & arch specifc header files
    generate_platform_header(gui)
    
    # Update ARXML file
    arxml_mcu.update_arxml(gui.arxml_file, gui.uc_info)
    
    makefile.close()