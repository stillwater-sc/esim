# esim
Computational energy simulator

## Introduction

  An energy simulator of algorithms on micro-architecture to study the energy efficiency 
of different computational engines.

Of particular interest are the following micro-architectures

- multi-core CPU
- many-core GPU
- data flow Cerebras style
- data flow SambaNova style
- digital in-memory compute dMatrix or Axelera
- domain flow architecture style

algorithms will need to be expressed in the form of steps that the micro-architecture supports and
for which we have an energy estimate. Then running the algorithm will simply accumulate the energy
expended to yield a total energy requirements for that algorithms running on that micro-architecture.

For example, let's start with a single core CPU running a matrix-vector algorithm.

The matrix-vector algorithm can be summarized as:

for (int i = 0; i < N; ++i) {
   y[i] = 0;
   for (int j = 0; j < M; ++j) {
       y[i] += A[i][j] * x[j];
   }
}
