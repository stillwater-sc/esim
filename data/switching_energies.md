# Database of switching energies

## Storage Elements

## Register Read/Write Energy Estimates by Process Node
Note: Values are approximate and may vary by foundry and implementation

| Register  | 28/22nm (fJ) | 16/14/12nm (fJ) | 7/6/5nm (fJ) | 3nm (fJ)  | 2nm (fJ)  |
|-----------|--------------|-----------------|--------------|-----------|-----------|
| Read bit  | 2.5 - 3.5    | 1.8 - 2.3       | 0.9 - 1.2    | 0.6 - 0.8 | 0.4 - 0.6 |
| Write bit | 3.0 - 4.0    | 2.0 - 2.8       | 1.1 - 1.5    | 0.7 - 1.0 | 0.5 - 0.8 |

**Notes:**
- Values assume typical operating conditions (TT corner, nominal voltage, 25°C)
- Energy includes both dynamic and short-circuit power
- Leakage power not included
- Values are for basic register operations without additional clock tree or routing overhead
- Advanced nodes (3nm, 2nm) are based on early estimates and projections

## Register file energy estimates

 All values in femtojoules per bit (fJ/bit)

| Operation | Size      | 28/22nm     | 16/14/12nm    | 7/6/5nm     | 3nm         | 2nm         |
|-----------|-----------|-------------|---------------|-------------|-------------|-------------|
| Read      |           |             |               |             |             |             |
|           | 32-entry  | 8.5  - 10.5 | 6.00  -  7.50 | 3.20 - 4.00 | 2.25 - 2.80 | 1.57 - 1.95 |
|           | 64-entry  | 12.0 - 14.0 | 8.50  - 10.00 | 4.50 - 5.50 | 3.15 - 3.85 | 2.21 - 2.70 |
|           | 128-entry | 16.0 - 18.0 | 11.00 - 13.00 | 6.00 - 7.00 | 4.20 - 4.90 | 2.95 - 3.45 |
| Write     |           |             |               |             |             |             |
|           | 32-entry  | 10.0 - 12.0 | 7.00  -  8.50 | 3.80 - 4.60 | 2.65 - 3.25 | 1.85 - 2.28 |
|           | 64-entry  | 14.0 - 16.0 | 10.00 - 11.50 | 5.20 - 6.20 | 3.65 - 4.35 | 2.55 - 3.05 |
|           | 128-entry | 18.0 - 20.0 | 13.00 - 15.0  | 7.00 - 8.00 | 4.90 - 5.60 | 3.45 - 3.95 |

**Notes:**
- All values in femtojoules per bit (fJ/bit)
- Assumes typical operating conditions (TT corner, nominal voltage, 25°C)
- Includes decoder, wordline, and bitline energy
- Includes local clock distribution
- Includes both dynamic and short-circuit power
- Values represent single read port, single write port configuration
- Additional ports would increase energy roughly linearly
- 3nm and 2nm nodes omitted due to limited data availability
  - estimating it by scaling 30% from previous gen node

This table format makes it easier to observe several trends:

1. Technology Scaling:
   - ~30% reduction from 28/22nm to 16/14/12nm
   - ~45% reduction from 16/14/12nm to 7/6/5nm
2. Size Scaling:
   - ~40% increase from 32 to 64 entries
   - ~35% increase from 64 to 128 entries
3. Operation Type:
    - Write operations consistently consume ~15-20% more energy than reads

Key scaling factors to note for the register file:

1. Energy roughly increases with log(N) where N is the number of entries due to:
    - Longer bitlines
    - More complex decoders
    - Increased wire capacitance
2. Each doubling of register file size typically adds about:
    - 40-50% energy overhead in older nodes (28/22nm)
    - 35-45% in intermediate nodes (16/14/12nm)
    - 30-40% in newer nodes (7/6/5nm)


## Logic Data Path elements

| Logic Operator | 28/22nm (fJ)  | 16/14/12nm (fJ) | 7/6/5nm (fJ) | 3nm (fJ) | 2nm (fJ) |
|----------------|---------------|-----------------|--------------|----------|----------|
| NOT            | 2.1 - 3.5     | 1.4 - 2.3       | 0.9 - 1.6    | 0.6 - 1.1| 0.4 - 0.8|
| NAND (2-input) | 3.2 - 4.7     | 2.1 - 3.1       | 1.4 - 2.1    | 0.9 - 1.5| 0.6 - 1.0|
| NOR (2-input)  | 3.5 - 5.0     | 2.3 - 3.4       | 1.5 - 2.3    | 1.0 - 1.7| 0.7 - 1.2|
| XOR (2-input)  | 5.6 - 7.8     | 3.7 - 5.2       | 2.5 - 3.5    | 1.6 - 2.3| 1.1 - 1.6|
| Half-Adder     | 8.9 - 12.5    | 5.8 - 8.1       | 3.9 - 5.5    | 2.5 - 3.6| 1.7 - 2.4|
| Full-Adder     | 12.4 - 17.3   | 8.1 - 11.3      | 5.4 - 7.6    | 3.5 - 5.0| 2.3 - 3.3|

**Notes:**
- Values are approximate and represent typical switching energy in femtojoules (fJ)
- Energy values are dynamic switching energy per operation
- Actual values may vary based on specific circuit design, load capacitance, and operating conditions
- Lower technology nodes show significant reduction in switching energy due to smaller transistor sizes and improved manufacturing processes

## Addition and subtraction

| Adder Size (bits) | 28/22nm (pJ) | 16/14/12nm (pJ) | 7/6/5nm (pJ) | 3nm (pJ)      | 2nm (pJ)      |
|-------------------|--------------|-----------------|--------------|---------------|---------------|
| 2                 | 0.018 - 0.025| 0.012 - 0.017   | 0.008 - 0.011| 0.005 - 0.007 | 0.003 - 0.005 |
| 4                 | 0.036 - 0.050| 0.024 - 0.034   | 0.016 - 0.022| 0.010 - 0.014 | 0.007 - 0.010 |
| 8                 | 0.072 - 0.100| 0.048 - 0.068   | 0.032 - 0.044| 0.020 - 0.028 | 0.014 - 0.020 |
| 12                | 0.108 - 0.150| 0.072 - 0.102   | 0.048 - 0.066| 0.030 - 0.042 | 0.021 - 0.030 |
| 16                | 0.144 - 0.200| 0.096 - 0.136   | 0.064 - 0.088| 0.040 - 0.056 | 0.028 - 0.040 |
| 20                | 0.180 - 0.250| 0.120 - 0.170   | 0.080 - 0.110| 0.050 - 0.070 | 0.035 - 0.050 |
| 24                | 0.216 - 0.300| 0.144 - 0.204   | 0.096 - 0.132| 0.060 - 0.084 | 0.042 - 0.060 |
| 28                | 0.252 - 0.350| 0.168 - 0.238   | 0.112 - 0.154| 0.070 - 0.098 | 0.049 - 0.070 |
| 32                | 0.288 - 0.400| 0.192 - 0.272   | 0.128 - 0.176| 0.080 - 0.112 | 0.056 - 0.080 |
| 64                | 0.576 - 0.800| 0.384 - 0.544   | 0.256 - 0.352| 0.160 - 0.224 | 0.112 - 0.160 |

**Notes:**
- Values are approximate switching energy in picojoules (pJ)
- Assumes a Carry-Look-Ahead (CLA) or similar optimized adder architecture
- Energy values represent typical dynamic switching energy per addition operation
- Actual energy consumption may vary based on specific circuit design, implementation, and operating conditions
- Scaling shows a linear relationship between adder size and energy consumption
- Significant energy reduction observed across smaller technology nodes

**Estimation Methodology:**
- Base energy calculated from fundamental gate-level switching energy
- Accounts for additional routing, interconnect, and parasitic capacitance
- Extrapolated using empirical scaling factors for different technology nodes

## Multiplication

| Multiplier Size (bits) | 28/22nm (pJ) | 16/14/12nm (pJ)   | 7/6/5nm (pJ)    | 3nm (pJ)        | 2nm (pJ)       |
|------------------------|--------------|-------------------|-----------------|-----------------|----------------|
| 2 × 2                  | 0.035 - 0.050| 0.023 - 0.033     | 0.015 - 0.022   | 0.010 - 0.014   | 0.007 - 0.010  |
| 4 × 4                  | 0.140 - 0.200| 0.093 - 0.133     | 0.062 - 0.088   | 0.040 - 0.056   | 0.028 - 0.040  |
| 8 × 8                  | 0.560 - 0.800| 0.373 - 0.533     | 0.249 - 0.355   | 0.160 - 0.224   | 0.112 - 0.160  |
| 12 × 12                | 1.260 - 1.800| 0.840 - 1.200     | 0.560 - 0.800   | 0.360 - 0.504   | 0.252 - 0.360  |
| 16 × 16                | 2.240 - 3.200| 1.493 - 2.133     | 0.995 - 1.424   | 0.640 - 0.896   | 0.448 - 0.640  |
| 20 × 20                | 3.500 - 5.000| 2.333 - 3.333     | 1.556 - 2.222   | 1.000 - 1.400   | 0.700 - 1.000  |
| 24 × 24                | 5.040 - 7.200| 3.360 - 4.800     | 2.240 - 3.200   | 1.440 - 2.016   | 1.008 - 1.440  |
| 28 × 28                | 6.960 - 9.940| 4.640 - 6.627     | 3.094 - 4.418   | 1.988 - 2.782   | 1.392 - 1.947  |
| 32 × 32                | 9.216 - 13.180| 6.144 - 8.787    | 4.096 - 5.858   | 2.636 - 3.694   | 1.845 - 2.586  |
| 64 × 64                | 36.864 - 52.720| 24.576 - 35.147 | 16.384 - 23.431 | 10.546 - 14.776 | 7.382 - 10.343 |

**Notes:**
- Values are approximate switching energy in picojoules (pJ)
- Assumes an optimized Booth multiplier architecture with Wallace tree reduction
- Energy values represent typical dynamic switching energy per multiplication operation
- Actual energy consumption may vary based on:
  - Specific multiplication algorithm (Array, Booth, Wallace Tree)
  - Circuit design and implementation details
  - Operating conditions and load capacitance

**Estimation Methodology:**
- Base energy calculated from fundamental gate-level switching energy
- Includes partial product generation, reduction, and final addition stages
- Accounts for additional routing, interconnect, and parasitic capacitance
- Extrapolated using empirical scaling factors for different technology nodes