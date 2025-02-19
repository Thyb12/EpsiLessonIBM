import os
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp

# 🔹 Vérifier que la clé API est bien définie
TOKEN = os.getenv("IBM_QUANTUM_API_KEY")
if not TOKEN:
    raise ValueError("Erreur : la clé API IBM Quantum est absente. Vérifiez que IBM_QUANTUM_API_KEY est bien défini dans les Secrets GitHub.")

# 🔹 Authentifier le service avec la clé API
QiskitRuntimeService.save_account(token=TOKEN, channel="ibm_quantum")
service = QiskitRuntimeService()

# 🔹 Sélectionner le backend le moins occupé
backend = service.least_busy(simulator=False, operational=True)
print(f"Backend sélectionné : {backend.name}")

# 🔹 Créer un circuit quantique simple
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# 🔹 Convertir en circuit ISA
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)

# 🔹 Construire l'estimateur
estimator = Estimator()
estimator.options.resilience_level = 1
estimator.options.default_shots = 5000

# 🔹 Mapper les observables
observables_labels = ["ZZ", "XX", "YY"]
observables = [SparsePauliOp(label) for label in observables_labels]
mapped_observables = [obs.apply_layout(isa_circuit.layout) for obs in observables]

# 🔹 Exécuter le job
job = estimator.run([(isa_circuit, mapped_observables)])

# 🔹 Afficher l'ID du job
print(f">>> Job ID: {job.job_id()}")
