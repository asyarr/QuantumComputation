from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np

# Função para aplicar a QFT em um circuito quântico
def apply_qft(circuit, n_qubits):
    # Aplica a QFT em n_qubits
    for qubit in range(n_qubits):
        # Aplica a porta Hadamard no qubit atual
        circuit.h(qubit)
        
        # Aplica as portas de rotação controlada (R_k)
        for control_qubit in range(qubit + 1, n_qubits):
            angle = np.pi / (2 ** (control_qubit - qubit))
            circuit.cp(angle, control_qubit, qubit)
    
    # Reordena os qubits no final
    for qubit in range(n_qubits // 2):
        circuit.swap(qubit, n_qubits - qubit - 1)


# Função para aplicar a IQFT em um circuito quântico
def apply_iqft(inverse_circuit, n_qubits):
    # Reordena os qubits no início (inverso da QFT)
    for qubit in range(n_qubits // 2):
        inverse_circuit.swap(qubit, n_qubits - qubit - 1)
    
    # Aplica as portas de rotação controlada inversa e Hadamard
    for qubit in range(n_qubits):
        # Aplica as portas de rotação controlada inversa
        for control_qubit in range(qubit):
            angle = -np.pi / (2 ** (qubit - control_qubit))
            inverse_circuit.cp(angle, control_qubit, qubit)
        
        # Aplica a porta Hadamard no qubit atual
        inverse_circuit.h(qubit)

# Número de qubits
n_qubits = 4

# Registradores quânticos e clássicos
qubits = QuantumRegister(n_qubits, name="q")
creg = ClassicalRegister(n_qubits, name="c")
circuit = QuantumCircuit(qubits, creg)
inverse_circuit = QuantumCircuit(qubits, creg)

# Aplica a QFT/IQFT ao circuito
apply_iqft(inverse_circuit, n_qubits)

# Desenha o circuito
print(inverse_circuit.draw("latex_source"))

# Simula o estado final usando Statevector
state = Statevector.from_instruction(inverse_circuit)

# Plota o estado no Diagrama de Bloch
plot_bloch_multivector(state)

# Salva o plot como uma imagem
plt.savefig("bloch_plot_qft.png")  # Salva no diretório atual
plt.show()  # Exibe o plot