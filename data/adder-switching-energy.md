| Adder Size (bits) | 28/22nm (pJ) | 16/14/12nm (pJ) | 7/6/5nm (pJ) | 3nm (pJ) | 2nm (pJ) |
|-------------------|--------------|-----------------|--------------|----------|----------|
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
