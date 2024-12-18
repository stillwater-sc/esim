# Integer Arithmetic and Logic Unit latency estimates


| Unit Type | Bit Size | 28/22nm (ns) | 16/14/12nm (ns) | 7/6/5nm (ns) | 3nm (ns) | 2nm (ns) |
|-----------|----------|--------------|-----------------|--------------|----------|----------|
| **CPU ALU** | | | | | | |
| | 8-bit     | 0.65 - 0.85 | 0.45 - 0.60  | 0.30 - 0.42 | 0.20 - 0.30 | 0.15 - 0.22 |
| | 16-bit    | 0.80 - 1.10 | 0.55 - 0.75  | 0.37 - 0.52 | 0.25 - 0.35 | 0.18 - 0.27 |
| | 32-bit    | 1.10 - 1.50 | 0.75 - 1.00  | 0.50 - 0.70 | 0.35 - 0.48 | 0.25 - 0.35 |
| | 64-bit    | 1.50 - 2.10 | 1.00 - 1.40  | 0.67 - 0.95 | 0.45 - 0.65 | 0.32 - 0.47 |
| **GPU ALU** | | | | | | |
| | 8-bit     | 0.55 - 0.75 | 0.38 - 0.52  | 0.25 - 0.35 | 0.17 - 0.25 | 0.12 - 0.18 |
| | 16-bit    | 0.70 - 0.95 | 0.48 - 0.65  | 0.32 - 0.44 | 0.22 - 0.30 | 0.15 - 0.22 |
| | 32-bit    | 0.95 - 1.30 | 0.65 - 0.88  | 0.43 - 0.60 | 0.30 - 0.40 | 0.21 - 0.30 |
| | 64-bit    | 1.30 - 1.80 | 0.88 - 1.20  | 0.59 - 0.80 | 0.40 - 0.55 | 0.28 - 0.40 |
| **DSP ALU** | | | | | | |
| | 8-bit     | 0.60 - 0.80 | 0.41 - 0.55  | 0.27 - 0.37 | 0.18 - 0.26 | 0.13 - 0.19 |
| | 16-bit    | 0.75 - 1.00 | 0.51 - 0.70  | 0.34 - 0.47 | 0.23 - 0.32 | 0.16 - 0.23 |
| | 32-bit    | 1.00 - 1.35 | 0.68 - 0.92  | 0.45 - 0.62 | 0.31 - 0.42 | 0.22 - 0.30 |
| | 64-bit    | 1.35 - 1.85 | 0.92 - 1.25  | 0.61 - 0.83 | 0.42 - 0.57 | 0.29 - 0.40 |

# Floating-Point Unit latency estimates

| Unit Type | Bit Size | 28/22nm (ns) | 16/14/12nm (ns) | 7/6/5nm (ns) | 3nm (ns) | 2nm (ns) |
|-----------|----------|--------------|-----------------|--------------|----------|----------|
| **CPU FPU** | | | | | | |
| | 8-bit     | 1.20 - 1.60 | 0.80 - 1.10  | 0.53 - 0.73 | 0.36 - 0.50 | 0.25 - 0.35 |
| | 16-bit    | 1.50 - 2.00 | 1.00 - 1.35  | 0.67 - 0.90 | 0.45 - 0.62 | 0.32 - 0.44 |
| | 32-bit    | 2.10 - 2.80 | 1.40 - 1.90  | 0.93 - 1.27 | 0.63 - 0.86 | 0.44 - 0.60 |
| | 64-bit    | 3.20 - 4.30 | 2.15 - 2.90  | 1.43 - 1.93 | 0.96 - 1.30 | 0.67 - 0.91 |
| **GPU FPU** | | | | | | |
| | 8-bit     | 1.00 - 1.40 | 0.67 - 0.95  | 0.45 - 0.63 | 0.30 - 0.42 | 0.21 - 0.30 |
| | 16-bit    | 1.30 - 1.75 | 0.87 - 1.18  | 0.58 - 0.79 | 0.39 - 0.53 | 0.27 - 0.37 |
| | 32-bit    | 1.80 - 2.40 | 1.20 - 1.62  | 0.80 - 1.08 | 0.54 - 0.74 | 0.38 - 0.52 |
| | 64-bit    | 2.75 - 3.70 | 1.83 - 2.47  | 1.22 - 1.65 | 0.82 - 1.11 | 0.57 - 0.77 |
| **DSP FPU** | | | | | | |
| | 8-bit     | 1.10 - 1.50 | 0.73 - 1.00  | 0.49 - 0.68 | 0.33 - 0.45 | 0.23 - 0.32 |
| | 16-bit    | 1.40 - 1.90 | 0.93 - 1.27  | 0.62 - 0.85 | 0.42 - 0.57 | 0.29 - 0.40 |
| | 32-bit    | 1.95 - 2.60 | 1.30 - 1.75  | 0.87 - 1.17 | 0.58 - 0.80 | 0.41 - 0.56 |
| | 64-bit    | 3.00 - 4.00 | 2.00 - 2.67  | 1.33 - 1.78 | 0.89 - 1.20 | 0.62 - 0.84 |

**Methodology and Key Observations:**

1. Latency Estimation Approach:
   - Based on critical path delays
   - Accounts for transistor switching times
   - Includes signal propagation and logic resolution times
   - Considers pipeline stages and circuit complexity

2. Technological Trends:
   - Consistent latency reduction across technology nodes
   - Approximately 3-4x latency improvement from 28/22nm to 2nm
   - Non-linear reduction due to:
     * Improved transistor switching speeds
     * Reduced interconnect capacitance
     * Advanced circuit design techniques

3. Design Point Characteristics:
   - CPU units: Most optimized for general-purpose computing
   - GPU units: Designed for parallel processing
   - DSP units: Specialized for signal processing algorithms

4. Bit Width Impact:
   - Latency increases with bit width
   - More pronounced in FPU units due to complex floating-point operations
   - Exponential complexity for larger bit sizes

**Factors Influencing Latency:**
- Transistor technology
- Circuit design complexity
- Instruction type (integer vs. floating-point)
- Architectural optimizations
- Specific implementation details

Would you like me to elaborate on any specific aspects of these latency estimates?