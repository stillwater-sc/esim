import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend,
  ResponsiveContainer 
} from 'recharts';

const ALUFPUEnergyBoxplot = () => {
  const data = [
    {
      technology: '28/22nm',
      CPU_ALU_min: 3.60,
      CPU_ALU_max: 5.20,
      GPU_ALU_min: 4.80,
      GPU_ALU_max: 6.80,
      DSP_ALU_min: 4.40,
      DSP_ALU_max: 6.00,
      CPU_FPU_min: 7.20,
      CPU_FPU_max: 10.40,
      GPU_FPU_min: 9.60,
      GPU_FPU_max: 13.60,
      DSP_FPU_min: 8.80,
      DSP_FPU_max: 12.00
    },
    {
      technology: '16/14/12nm',
      CPU_ALU_min: 2.40,
      CPU_ALU_max: 3.47,
      GPU_ALU_min: 3.20,
      GPU_ALU_max: 4.56,
      DSP_ALU_min: 2.93,
      DSP_ALU_max: 4.00,
      CPU_FPU_min: 4.80,
      CPU_FPU_max: 6.93,
      GPU_FPU_min: 6.40,
      GPU_FPU_max: 9.13,
      DSP_FPU_min: 5.87,
      DSP_FPU_max: 8.00
    },
    {
      technology: '7/6/5nm',
      CPU_ALU_min: 1.60,
      CPU_ALU_max: 2.32,
      GPU_ALU_min: 2.13,
      GPU_ALU_max: 3.04,
      DSP_ALU_min: 1.96,
      DSP_ALU_max: 2.80,
      CPU_FPU_min: 3.20,
      CPU_FPU_max: 4.64,
      GPU_FPU_min: 4.27,
      GPU_FPU_max: 6.08,
      DSP_FPU_min: 3.91,
      DSP_FPU_max: 5.60
    },
    {
      technology: '3nm',
      CPU_ALU_min: 1.04,
      CPU_ALU_max: 1.52,
      GPU_ALU_min: 1.38,
      GPU_ALU_max: 2.00,
      DSP_ALU_min: 1.27,
      DSP_ALU_max: 1.84,
      CPU_FPU_min: 2.08,
      CPU_FPU_max: 3.04,
      GPU_FPU_min: 2.76,
      GPU_FPU_max: 4.00,
      DSP_FPU_min: 2.54,
      DSP_FPU_max: 3.68
    },
    {
      technology: '2nm',
      CPU_ALU_min: 0.72,
      CPU_ALU_max: 1.05,
      GPU_ALU_min: 0.96,
      GPU_ALU_max: 1.38,
      DSP_ALU_min: 0.88,
      DSP_ALU_max: 1.28,
      CPU_FPU_min: 1.44,
      CPU_FPU_max: 2.10,
      GPU_FPU_min: 1.92,
      GPU_FPU_max: 2.76,
      DSP_FPU_min: 1.76,
      DSP_FPU_max: 2.56
    }
  ];

  return (
    <div className="w-full h-[600px]">
      <ResponsiveContainer width="100%" height="100%" children={''}>
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="technology" 
            label={{ 
              value: 'CMOS Technology Node', 
              position: 'bottom', 
              offset: 40 
            }} 
          />
          <YAxis 
            label={{ 
              value: 'Switching Energy (pJ)', 
              angle: -90, 
              position: 'left', 
              offset: 20 
            }} 
          />
          <Tooltip />
          <Legend />
          
          <Bar dataKey="CPU_ALU_min" name="CPU ALU Min" fill="#8884d8" stackId="CPU_ALU" />
          <Bar dataKey="CPU_ALU_max" name="CPU ALU Max" fill="#8884d8" stackId="CPU_ALU" />
          
          <Bar dataKey="GPU_ALU_min" name="GPU ALU Min" fill="#82ca9d" stackId="GPU_ALU" />
          <Bar dataKey="GPU_ALU_max" name="GPU ALU Max" fill="#82ca9d" stackId="GPU_ALU" />
          
          <Bar dataKey="DSP_ALU_min" name="DSP ALU Min" fill="#ffc658" stackId="DSP_ALU" />
          <Bar dataKey="DSP_ALU_max" name="DSP ALU Max" fill="#ffc658" stackId="DSP_ALU" />
          
          <Bar dataKey="CPU_FPU_min" name="CPU FPU Min" fill="#ff7300" stackId="CPU_FPU" />
          <Bar dataKey="CPU_FPU_max" name="CPU FPU Max" fill="#ff7300" stackId="CPU_FPU" />
          
          <Bar dataKey="GPU_FPU_min" name="GPU FPU Min" fill="#387908" stackId="GPU_FPU" />
          <Bar dataKey="GPU_FPU_max" name="GPU FPU Max" fill="#387908" stackId="GPU_FPU" />
          
          <Bar dataKey="DSP_FPU_min" name="DSP FPU Min" fill="#ff0000" stackId="DSP_FPU" />
          <Bar dataKey="DSP_FPU_max" name="DSP FPU Max" fill="#ff0000" stackId="DSP_FPU" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ALUFPUEnergyBoxplot;
