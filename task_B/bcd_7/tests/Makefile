CWD = $(shell pwd)
COCOTB = $(CWD)/../../../cocotb
VERILOG_SOURCES = $(CWD)/../verilog/bcd_7.v
TOPLEVEL = bcd_7
MODULE=$(TOPLEVEL)_cocotb
SIM = verilator
TOPLEVEL_LANG = verilog
include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim