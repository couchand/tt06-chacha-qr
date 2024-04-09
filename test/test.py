# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_load(dut):
  dut._log.info("Start")

  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

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

  dut._log.info("Set 1 to 30")
  dut.ui_in.value = 30
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x11
  await ClockCycles(dut.clk, 2)
  dut.uio_in.value = 0x01
  await ClockCycles(dut.clk, 1)

  dut._log.info("Set 2 to 40")
  dut.ui_in.value = 40
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x12
  await ClockCycles(dut.clk, 2)
  dut.uio_in.value = 0x02
  await ClockCycles(dut.clk, 1)

  dut._log.info("Check that 0 is 20")
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 20

  dut._log.info("Check that 1 is 30")
  dut.uio_in.value = 0x01
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 30

  dut._log.info("Check that 2 is 40")
  dut.uio_in.value = 0x02
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 40

  dut._log.info("End")

@cocotb.test()
async def test_qr(dut):
  dut._log.info("Start")

  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1
  await ClockCycles(dut.clk, 10)

  dut._log.info("Set a to 'expa'")
  dut.ui_in.value = 0x65
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x10
  await ClockCycles(dut.clk, 2)
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)

  dut.ui_in.value = 0x78
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x11
  await ClockCycles(dut.clk, 2)
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)

  dut.ui_in.value = 0x70
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x12
  await ClockCycles(dut.clk, 2)
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)

  dut.ui_in.value = 0x61
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x13
  await ClockCycles(dut.clk, 2)
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)

  dut._log.info("All others are zeroed by reset")

  await ClockCycles(dut.clk, 10)

  dut._log.info("Run quarter round")
  dut.uio_in.value = 0x20
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x60
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 10)

  dut._log.info("Check that a is 0xB7877FEB")
  dut.uio_in.value = 0x00
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0xEB

  dut.uio_in.value = 0x01
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x7F

  dut.uio_in.value = 0x02
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x87

  dut.uio_in.value = 0x03
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0xB7

  dut._log.info("End")
