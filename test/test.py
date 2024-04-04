# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
  dut._log.info("Start")

  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1
  await ClockCycles(dut.clk, 10)

  dut._log.info("Set 0 to 20")
  dut.ui_in.value = 20
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x10
  await ClockCycles(dut.clk, 2)
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)

  #dut.ui_in.value = 30
  #dut.uio_in.value = 0x11
  #await ClockCycles(dut.clk, 1)

  #dut.ui_in.value = 40
  #dut.uio_in.value = 0x12
  #await ClockCycles(dut.clk, 1)

  dut._log.info("Check that 0 is 20")
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 20

  #dut.uio_in.value = 0x01
  #await ClockCycles(dut.clk, 1)
  #assert dut.uo_out.value == 30

  #dut.uio_in.value = 0x02
  #await ClockCycles(dut.clk, 1)
  #assert dut.uo_out.value == 40
