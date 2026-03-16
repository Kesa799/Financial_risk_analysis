from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def quantum_risk_analysis(volatility):

    # Convert volatility into probability scale
    p = min(volatility * 10, 1)

    qc = QuantumCircuit(1,1)

    qc.ry(2*np.arcsin(np.sqrt(p)),0)

    qc.measure(0,0)

    simulator = AerSimulator()
    result = simulator.run(qc, shots=2000).result()

    counts = result.get_counts()

    risk_probability = counts.get('1',0)/2000

    return round(risk_probability,3)

