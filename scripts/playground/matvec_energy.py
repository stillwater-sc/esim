from tabulate import tabulate

from energysim import StoredProgramMachineEnergyDatabase, StoredProgramMachineMetrics, flat_mv_spm
from energysim.execution.spm_events import StoredProgramMachineEvents


def report(events: StoredProgramMachineEvents, energy: StoredProgramMachineMetrics):
    instruction_events = events.instructions
    execute_events = events.execute
    register_read_events = events.register_read
    register_write_events = events.register_write
    compute_events = instruction_events + execute_events + register_read_events + register_write_events

    instruction_energy = energy.instruction
    execute_energy = energy.execute
    register_read_energy = energy.register_read
    register_write_energy = energy.register_write
    compute_energy = instruction_energy + execute_energy + register_read_energy + register_write_energy

    l1_events = events.l1_read + events.l1_write
    l2_events = events.l2_read + events.l2_write
    l3_events = events.l3_read + events.l3_write
    cache_events = l1_events + l2_events + l3_events
    dram_events = events.dram_read + events.dram_write
    data_movement_events = cache_events + dram_events
    # data movement energy costs
    l1_energy = energy.l1_read + energy.l1_write
    l2_energy = energy.l2_read + energy.l2_write
    l3_energy = energy.l3_read + energy.l3_write
    cache_energy = l1_energy + l2_energy + l3_energy
    dram_energy = energy.dram_read + energy.dram_write
    data_movement_energy = cache_energy + dram_energy
    total_energy = compute_energy + data_movement_energy

    if data_movement_energy > 0:
        l1_read_relative = energy.l1_read / data_movement_energy
        l2_read_relative = energy.l2_read / data_movement_energy
        l3_read_relative = energy.l3_read / data_movement_energy
        memory_read_relative = energy.dram_read / data_movement_energy
        l1_write_relative = energy.l1_write / data_movement_energy
        l2_write_relative = energy.l2_write / data_movement_energy
        l3_write_relative = energy.l3_write / data_movement_energy
        memory_write_relative = energy.dram_write / data_movement_energy
    else:
        l1_read_relative = 0
        l2_read_relative = 0
        l3_read_relative = 0
        memory_read_relative = 0
        l1_write_relative = 0
        l2_write_relative = 0
        l3_write_relative = 0
        memory_write_relative = 0

    print("Name: " + energy.name)
    data = [["event", "Occurrences", "pJ", "%"],
            ["Total", "-", total_energy, 100.0],
            ["Compute", compute_events, compute_energy, 100 * compute_energy / total_energy],
            ["DataMovement", data_movement_events, data_movement_energy, 100 * data_movement_energy / total_energy],
            ["Compute", compute_events, compute_energy, 100 * compute_energy / total_energy],
            ["- Execute", execute_events, execute_energy, 100 * execute_energy / total_energy],
            ["- Instruction", instruction_events, instruction_energy, 100 * instruction_energy / total_energy],
            ["- Register Read", register_read_events, register_read_energy, 100 * register_read_energy / total_energy],
            ["- Register Write", register_write_events, register_write_energy, 100 * register_write_energy / total_energy],
            ["Cache", cache_events, cache_energy, 100 * cache_energy / total_energy],
            ["- L1 Cache", l1_events, l1_energy, 100 * l1_energy / total_energy],
            ["-  read", events.l1_read, energy.l1_read, 100 * energy.l1_read / total_energy],
            ["-  write", events.l1_write, energy.l1_write, 100 * energy.l1_write / total_energy],
            ["- L2 Cache", l2_events, l2_energy, 100 * l2_energy / total_energy],
            ["-  read", events.l2_read, energy.l2_read, 100 * energy.l2_read / total_energy],
            ["-  write", events.l2_write, energy.l2_write, 100 * energy.l2_write / total_energy],
            ["- L3 Cache", l3_events, l3_energy, 100 * l3_energy / total_energy],
            ["-  read", events.l3_read, energy.l3_read, 100 * energy.l3_read / total_energy],
            ["-  write", events.l3_write, energy.l3_write, 100 * energy.l3_write / total_energy],
            ["Memory", dram_events, dram_energy, 100 * dram_energy / total_energy],
            ["- read", events.dram_read, energy.dram_read, 100 * energy.dram_read / total_energy],
            ["- write", events.dram_write, energy.dram_write, 100 * energy.dram_write / total_energy]

            ]

    print(tabulate(data, headers="firstrow", floatfmt=".1f"))

if __name__ == '__main__':
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_attributes = db.generate('n14l', 2.5, 3.2, 64)
    print(spm_attributes)
    events, energy = flat_mv_spm(16, 16, spm_attributes)
    report(events, energy)

