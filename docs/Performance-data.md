# Performance Information

| Attribute       | Value         |
|-----------------|---------------|
| GPU Name        | GP104         |
| GPU Variant     | GP104-200-A1  |
| Architecture    | Pascal        |
| Foundry         | TSMC          |
| Process Size    | 16 nm         |
| Transistors     | 7,200 million |
| Density         | 22.9M / mm²   |
| Die Size        | 314 mm²       |
| Chip Package    | BGA-2150      |

# Performance
| Attributes    | Value                     |
|---------------|---------------------------|
| Pixel Rate    | 107.7 GPixel/s            |
| Texture Rate  | 202.0 GTexel/s            |
| FP16 (half)   | 101.0 GFLOPS (1:64)       |
| FP32 (float)  | 6.463 TFLOPS              |
| FP64 (double) | 202.0 GFLOPS (1:32)       |
| Base Clock    | 1506 MHz                  |
| Boost Clock   | 1683 MHz                  |
| Memory Clock  | 2002 MHz 8 Gbps effective |
| TDP           | 150 W                     |
 Suggested PSU  | 450 W                     |

# Memory

| Attributes  | Value      |
|-------------|------------|
| Memory Size | 8 GB       |
| Memory Type | GDDR5      |
| Memory Bus  | 256 bit    |
| Bandwidth   | 256.3 GB/s |

Like its predecessor, GDDR4, GDDR5 is based on DDR3 SDRAM memory, which has double the data lines 
compared to DDR2 SDRAM. GDDR5 also uses 8-bit wide prefetch buffers similar to GDDR4 and DDR3 SDRAM.

GDDR5 SGRAM conforms to the standards which were set out in the GDDR5 specification by the JEDEC. 
SGRAM is single-ported. However, it can open two memory pages at once, which simulates the dual-port 
nature of other VRAM technologies. It uses an 8N-prefetch architecture and DDR interface to achieve 
high performance operation and can be configured to operate in ×32 mode or ×16 (clamshell) mode 
which is detected during device initialization. The GDDR5 interface transfers two 32-bit wide 
data words per write clock (WCK) cycle to/from the I/O pins. Corresponding to the 8N-prefetch, 
a single write or read access consists of a 256-bit wide two CK clock cycle data transfer at 
the internal memory core and eight corresponding 32-bit wide one-half WCK clock cycle data transfers 
at the I/O pins.

GDDR5 operates with two different clock types. A differential command clock (CK) as a reference 
for address and command inputs, and a forwarded differential write clock (WCK) as a reference for 
data reads and writes, that runs at twice the CK frequency. Being more precise, the GDDR5 SGRAM 
uses a total of three clocks: two write clocks associated with two bytes (WCK01 and WCK23) and 
a single command clock (CK). Taking a GDDR5 with 5 Gbit/s data rate per pin as an example, the 
CK runs with 1.25 GHz and both WCK clocks at 2.5 GHz. The CK and WCKs are phase aligned during 
the initialization and training sequence. This alignment allows read and write access with minimum latency.

A single 32-bit GDDR5 chip has about 67 signal pins and the rest are power and grounds 
in the 170 BGA package.

As of January 15, 2015, Samsung announced in a press release that it had begun mass production 
of "8 Gb" (8 × 1024^3 bits) GDDR5 memory chips based on a 20 nm fabrication process. 
To meet the demand of higher resolution displays (such as 4K) becoming more mainstream, higher 
density chips are required in order to facilitate larger frame buffers for graphically intensive 
computation, namely PC gaming and other 3D rendering. Increased bandwidth of the new high-density 
modules equates to 8 Gbit/s per pin × 170 pins on the BGA package x 32-bits per I/O cycle, 
or 256 Gbit/s effective bandwidth per chip.

# Actual program performance

Threads per Block : 128
Blocks per Grid   : 8192

Matrix-Vector Multiplication on GPU

| attribute      | value              |
|----------------|--------------------|
| Dimensions     | 1048576 x 1024     |
| Execution Time | 74.027008 ms       |
| Throughput     | 14.504731 SP-GLOPS |

Matrix-Vector Multiplication on GPU with load/unload over PCIe

| attribute       | value              |
|-----------------|--------------------|
| Dimensions      | 1048576 x 1024     |
| Execution Time  | 717.777893 ms      |
| Throughput      | 1.495925 SP-GLOPS  | 

Memory bw = 256GB/s
2 operands read for 1 FMA
4 bytes per operand
256 / 8 = 32G operands / sec -> 16GFlops/sec max

 