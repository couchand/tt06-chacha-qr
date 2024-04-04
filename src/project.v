/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`define default_netname none

module tt_um_couchand_chacha_qr (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  assign uio_out = 0;
  assign uio_oe  = 0;

  reg [31:0] a;
  reg [31:0] b;
  reg [31:0] c;
  reg [31:0] d;

  wire [3:0] addr = uio_in[3:0];
  wire wr_en = uio_in[4];
  wire qr_en = uio_in[5];

  wire [31:0] reg_out = addr[3]
    ? (addr[2] ? d : c)
    : (addr[2] ? b : a);

  assign uo_out = addr[1]
    ? (addr[0] ? reg_out[31:24] : reg_out[23:16])
    : (addr[0] ? reg_out[15:8] : reg_out[7:0]);

  wire [31:0] a_plus_b = a + b;
  wire [31:0] d_xor_apb = d ^ a_plus_b;
  wire [31:0] dxa_rotl_16;
  assign dxa_rotl_16[15:0] = d_xor_apb[31:16];
  assign dxa_rotl_16[31:16] = d_xor_apb[15:0];

  wire [31:0] c_plus_d = c + dxa_rotl_16;
  wire [31:0] b_xor_cpd = b ^ c_plus_d;
  wire [31:0] bxc_rotl_12;
  assign bxc_rotl_12[11:0] = b_xor_cpd[31:20];
  assign bxc_rotl_12[31:12] = b_xor_cpd[19:0];

  wire [31:0] apb_plus_br12 = a_plus_b + bxc_rotl_12;
  wire [31:0] dr16_xor_apb = dxa_rotl_16 ^ apb_plus_br12;
  wire [31:0] dxa_rotl_8;
  assign dxa_rotl_8[7:0] = dr16_xor_apb[31:24];
  assign dxa_rotl_8[31:8] = dr16_xor_apb[23:0];

  wire [31:0] cpd_plus_dr8 = c_plus_d + dxa_rotl_8;
  wire [31:0] br12_xor_cpd = bxc_rotl_12 ^ cpd_plus_dr8;
  wire [31:0] bxc_rotl_7;
  assign bxc_rotl_7[6:0] = br12_xor_cpd[31:25];
  assign bxc_rotl_7[31:7] = br12_xor_cpd[24:0];

  always @(posedge clk) begin
    if (!rst_n) begin
      a <= 31'b0;
      b <= 31'b0;
      c <= 31'b0;
      d <= 31'b0;
    end else begin
      if (wr_en) begin
        if (addr[3]) begin
          if (addr[2]) begin
            if (addr[1]) begin
              if (addr[0]) begin
                d[31:24] <= ui_in;
              end else begin
                d[23:16] <= ui_in;
              end
            end else begin
              if (addr[0]) begin
                d[15:8] <= ui_in;
              end else begin
                d[7:0] <= ui_in;
              end
            end
          end else begin
            if (addr[1]) begin
              if (addr[0]) begin
                c[31:24] <= ui_in;
              end else begin
                c[23:16] <= ui_in;
              end
            end else begin
              if (addr[0]) begin
                c[15:8] <= ui_in;
              end else begin
                c[7:0] <= ui_in;
              end
            end
          end
        end else begin
          if (addr[2]) begin
            if (addr[1]) begin
              if (addr[0]) begin
                b[31:24] <= ui_in;
              end else begin
                b[23:16] <= ui_in;
              end
            end else begin
              if (addr[0]) begin
                b[15:8] <= ui_in;
              end else begin
                b[7:0] <= ui_in;
              end
            end
          end else begin
            if (addr[1]) begin
              if (addr[0]) begin
                a[31:24] <= ui_in;
              end else begin
                a[23:16] <= ui_in;
              end
            end else begin
              if (addr[0]) begin
                a[15:8] <= ui_in;
              end else begin
                a[7:0] <= ui_in;
              end
            end
          end
        end
      end else begin
        if qr_en begin
          a <= apb_plus_br12;
          b <= bxc_rotl_7;
          c <= cpd_plus_dr8;
          d <= dxa_rotl_8;
        end
      end
    end
  end

endmodule
