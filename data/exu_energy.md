All switching energies are in p-Joules (pJ)

The switching energy for the execute units, agu8, alu8, fpu8, sfu8,
are for 8-bit building blocks.

The register read and write are estimates for an 64 entry
register file, and then for an 8-bit building block.

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

28/22nm read: 12fJ * 8 = 0.096pJ  14fJ * 8 = 0.112pJ
28/22nm write: 14fJ * 8 = 0.112   16fJ * 8 = 0.128pJ

16/14/12nm read: 8.5fJ * 8 = 0.068pJ 10fJ * 8 = 0.080pJ
16/14/12nm write: 10fJ * 8 = 0.080pJ 11.5fJ * 8 = 0.092pJ

7/6/5nm read:  4.5fJ * 8 = 0.036pJ   5.5fJ * 8 = 0.044pJ
7/6/5nm write: 5.2fJ * 8 = 0.0416pJ  6.2fJ * 8 = 0.0496pJ

3nm read: 3.15fJ * 8 = 0.0252pJ  3.85fJ * 8 = 0.0308pJ
3nm write: 3.65fJ * 8 = 0.0292pJ 4.35fJ * 8 = 0.0348pJ

2nm read:  2.21fJ * 8 = 0.01768pJ  2.7fJ * 8 = 0.0216pJ
2nm write: 2.55fJ * 8 = 0.0204pJ 3.05fJ * 8 = 0.0244pJ