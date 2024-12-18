| Multiplier Size (bits) | 28/22nm (pJ) | 16/14/12nm (pJ) | 7/6/5nm (pJ) | 3nm (pJ) | 2nm (pJ) |
|------------------------|--------------|-----------------|--------------|----------|----------|
| 2 × 2                 | 0.035 - 0.050| 0.023 - 0.033   | 0.015 - 0.022| 0.010 - 0.014 | 0.007 - 0.010 |
| 4 × 4                 | 0.140 - 0.200| 0.093 - 0.133   | 0.062 - 0.088| 0.040 - 0.056 | 0.028 - 0.040 |
| 8 × 8                 | 0.560 - 0.800| 0.373 - 0.533   | 0.249 - 0.355| 0.160 - 0.224 | 0.112 - 0.160 |
| 12 × 12               | 1.260 - 1.800| 0.840 - 1.200   | 0.560 - 0.800| 0.360 - 0.504 | 0.252 - 0.360 |
| 16 × 16               | 2.240 - 3.200| 1.493 - 2.133   | 0.995 - 1.424| 0.640 - 0.896 | 0.448 - 0.640 |
| 20 × 20               | 3.500 - 5.000| 2.333 - 3.333   | 1.556 - 2.222| 1.000 - 1.400 | 0.700 - 1.000 |
| 24 × 24               | 5.040 - 7.200| 3.360 - 4.800   | 2.240 - 3.200| 1.440 - 2.016 | 1.008 - 1.440 |
| 28 × 28               | 6.960 - 9.940| 4.640 - 6.627   | 3.094 - 4.418| 1.988 - 2.782 | 1.392 - 1.947 |
| 32 × 32               | 9.216 - 13.180| 6.144 - 8.787   | 4.096 - 5.858| 2.636 - 3.694 | 1.845 - 2.586 |
| 64 × 64               | 36.864 - 52.720| 24.576 - 35.147 | 16.384 - 23.431| 10.546 - 14.776 | 7.382 - 10.343 |

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
