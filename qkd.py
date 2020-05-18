import numpy as np
from utils import *
from qiskit import(QuantumCircuit,execute, Aer)
from qiskit.visualization import plot_histogram
from random import randrange
from math import floor

NUM_TABS = 8

# Use Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')

def x_measurement(qc,qubit,cbit):
    """Measure 'qubit' in the X-basis, and store the result in 'cbit'"""
    qc.h(qubit)
    qc.measure(qubit, cbit)
    qc.h(qubit)
    return qc


def RBG():
   qc = QuantumCircuit(1, 1)
   qc.h(0)
   qc.measure(0,0)
   job = execute(qc, simulator, shots=1)
   result = job.result()
   counts = result.get_counts(qc)
   try:
      counts['0']
      return 0
   except:
      return 1

def test_RBG(num):
   ones = 0
   zeroes = 0
   for i in range(num):
      if RBG() == 0: zeroes += 1
      else: ones +=1
   return zeroes, ones

# print(test_RBG(1000))

def AliceCreateQubit(EVE):
   bit = RBG()
   applyH = RBG()
   qc = QuantumCircuit(1,2)
   if bit:
      qc.x(0)
   if applyH:
      qc.h(0)
      basis = "x"
      a = '1/rt(2)'
      if bit: 
         b = '-1/rt(2)'
      else:
         b = '1/rt(2)'
   else:
      basis = "+"
      if bit: 
         a, b = 0,1
      else:
         a, b = 1, 0
   if EVE: 
      MY_PrintSendQubit(a, b, lefttoright=True, bit = False, num_tabs=floor(NUM_TABS/2))
   else: MY_PrintSendQubit(a,b)
   return qc, basis, bit

def BobMeasureInBasis(qc):
   hadamard_basis = RBG()
   if hadamard_basis:
      basis = "x"
      qc = x_measurement(qc,0,0)
   else:
      basis = "+"
      qc.measure(0,0)
   job = execute(qc, simulator, shots=1)
   result = job.result()
   counts = result.get_counts(qc)
   try:
      try: counts['00']
      except: counts['10']
      bit =  0
   except:
      bit = 1
   MY_PrintMeasureQubit(basis, bit, NUM_TABS)
   return basis, bit


def EveMeasureInBasis(qc):
   hadamard_basis = RBG()
   if hadamard_basis:
      basis = "x"
      qc = x_measurement(qc,0,1)
   else:
      basis = "+"
      qc.measure(0,1)
   job = execute(qc, simulator, shots=1)
   result = job.result()
   counts = result.get_counts(qc)
   try:
      counts['00']
      bit =  0
   except:
      bit = 1
   MY_PrintMeasureQubit(basis, bit, floor(NUM_TABS/2))
   sys.stdout.write("\033[F") #back to previous line
   return basis, bit, qc





def CompareBasesClassicially(sender_bases, recipient_bases, recipient_bits, lefttoright = True):
   same_bits = []
   for i in range(len(sender_bases)):
      if sender_bases[i] == recipient_bases[i]:
         same_bits += [recipient_bits[i]]
      MY_PrintSendQubit(0, 0, lefttoright, True, num_tabs=NUM_TABS, icon = str(sender_bases[i]), pause = .01)
   return same_bits

def ObserveBasesClassicially(sender_bases, recipient_bases, observer_bases,  observer_bits):
   same_bits = []
   for i in range(len(sender_bases)):
      if sender_bases[i] == recipient_bases[i]:
         same_bits += [observer_bits[i]]
   return same_bits


def QKD(num_bits_sent, EVE, VIEW):
   print("\n\nQUANTUM KEY DISTRIBUTION (QKD)\n\n" + "=" * 90 + "\n")
   if EVE: MY_print("ALICE"+ '\t' * floor(NUM_TABS/2) + "EVE"+ '\t' * floor(NUM_TABS/2) + 'BOB')
   else: MY_print("ALICE"+ '\t' * NUM_TABS + 'BOB')
   # Initialize basis/bit arrays for Alice and Bob
   alice_bases = [0 for x in range(num_bits_sent)]
   alice_bits = [0 for x in range(num_bits_sent)]
   bob_bases = [0 for x in range(num_bits_sent)]
   bob_bits = [0 for x in range(num_bits_sent)]
   eve_bases = [0 for x in range(num_bits_sent)]
   eve_bits = [0 for x in range(num_bits_sent)]
   if EVE:  MY_print("ALICE: CHOOSE BASES & BITS\tEVE: INTERUPTS & MEASURES\tBOB: CHOOSE BASES & MEASURE")
   else: MY_print("ALICE: CHOOSE BASES & BITS\t\t\t\t\tBOB: CHOOSE BASES & MEASURE")

   # For each qubit...
   for i in range(num_bits_sent):
      # Alice creates the qubits 
      qc, alice_bases[i], alice_bits[i] = AliceCreateQubit(EVE)
      # Alice sends qubit to Bob
      qc.barrier()
      # Eve interupts
      if EVE: 
         eve_bases[i], eve_bits[i], qc = EveMeasureInBasis(qc)
         qc.barrier()
      # Bob measures in randomly chosen basis
      bob_bases[i], bob_bits[i] = BobMeasureInBasis(qc)
      # MY_print(qc.draw())
      # Alice and Bob classically compare bases
      # Alice creates key from her bits that match Bob's bases
   MY_print("\nALICE & BOB'S RESULTING BITS")
   print("Alice : " + str(alice_bits))
   if EVE: print("Eve   : " + str(eve_bits))
   print("Bob   : " + str(bob_bits) + "\n")
   MY_print("ALICE & BOB COMPARE BASES CLASSICALLY")
   alice_key = CompareBasesClassicially(bob_bases, alice_bases, alice_bits)
   # Bob creates key from his bits that match Alice's bases
   bob_key = CompareBasesClassicially(alice_bases, bob_bases, bob_bits, False)
   # Length of key ie qubits measured in same basis
   MY_print("ALICE & BOB DISCARD BITS CREATED/MEASURED WITH DIFFERENT BASES")
   eve_key  = ObserveBasesClassicially(alice_bases, bob_bases, eve_bases, eve_bits)
   print("\nAlice : " + str(alice_key))
   print("Bob   : " + str(bob_key))
   if EVE: print("Eve   : " + str(eve_key))
   # If true, protocol worked
   if (alice_key == bob_key): 
      print("ALICE KEY == BOB KEY\n")
      if EVE: print("FAILURE: EVE WAS NOT DETECTED")
      else: print("SUCCESS")
   else: 
      print("ALICE KEY != BOB KEY\n")
      if EVE: print("SUCCESS: EVE WAS DETECTED")
      else: print("FAILURE: ERROR IN PROTOCOL")
   print("\n")

def MY_PrintSendQubit(a, b, lefttoright=True, bit = False, num_tabs=NUM_TABS, icon = "", pause  = .1):
   if VIEW: PrintSendQubit(a, b, lefttoright, bit , num_tabs, icon, pause)

def MY_PrintMeasureQubit(basis, result, num_tabs=0): 
   if VIEW: PrintMeasureQubit(basis, result, num_tabs)

def MY_print(s): 
   if VIEW: print(s)



if __name__ == '__main__':
   num_bits_sent = int(input("Number of qubits to send = "))
   EVE = bool(input("Eve? (press any key for yes, enter for no) = "))
   VIEW = True

   QKD(num_bits_sent, EVE, VIEW)



