#kMC_pseudo.py
# * + A <-> A*

import copy
import random
import math

class ElementaryReaction():
	"""docstring for ElementaryReaction"""
	def __init__(self, reactants, products, k):
		self.reactants = reactants
		self.products = products
		self.k = k

class Process():
	"""docstring for Process"""
	def __init__(self, dt, step, location, elem_rxn):
		self.dt = dt
		self.step = step
		self.location = location
		self.elem_rxn = elem_rxn	

class kMC_Simulation():
	"""docstring for kMC_Simulation"""
	def __init__(self):
		self.time = 0
		self.step = 0
		self.SIZE = 10
		self.UNIT_CELL = ["*"]
		self.lattice = [[copy.copy(self.UNIT_CELL) for i in range(self.SIZE)] for j in range(self.SIZE)]
		self.ELEMENTARY_RXNS = [ElementaryReaction(["*"], ["A"], 1), ElementaryReaction(["A"], ["*"], 1)]
		self.enabled_processes = self._build_enabled_list()

		self.STOP_TIME = float("inf")
		
	def run(self):
		#while True:
		while self.time < self.STOP_TIME:
			print(self.lattice)
			self._get_coverage()
			self._next_process = self.enabled_processes[0]
			del self.enabled_processes[0]
			if self._is_enabled(self._next_process):
				self.step += 1
				self.time = self._next_process.dt
				self._update_lattice()
				self._add_enabled_processes()
			#print(self.time)
			#input()
		print(self.time)
		print(self.step)


	def _get_coverage(self):
		empty = 0
		A = 0
		for i in range(self.SIZE):
			for j in range(self.SIZE):
				if self.lattice[i][j] == ["*"]:
					empty += 1
				else:
					A += 1
		print("Empty (*) coverage = ",empty/self.SIZE/self.SIZE,'\tA coverage = ',A/self.SIZE/self.SIZE)


	def _is_enabled(self, candidate_process):
		i = self._next_process.location[0]
		j = self._next_process.location[1]
		current_site_occupant = self.lattice[i][j]
		return current_site_occupant == self._next_process.elem_rxn.reactants

	def _update_lattice(self):
		i = self._next_process.location[0]
		j = self._next_process.location[1]
		new_site_occupant = self._next_process.elem_rxn.products
		self.lattice[i][j] = new_site_occupant

	def _add_enabled_processes(self):
		i = self._next_process.location[0]
		j = self._next_process.location[1]
		if self.lattice[i][j] == ["*"]:
			elem_rxn = self.ELEMENTARY_RXNS[0]
			t = self._get_time(elem_rxn)
			p = Process(t, self.step, (i,j), elem_rxn)
		elif self.lattice[i][j] == ["A"]:
			elem_rxn = self.ELEMENTARY_RXNS[1]
			t = self._get_time(elem_rxn)
			p = Process(t, self.step, (i,j), elem_rxn)
		self.enabled_processes = self._ordered_list_add(self.enabled_processes, p)

	def _get_time(self, elem_rxn):
		return self.time - math.log(random.random()) / elem_rxn.k

	def _build_enabled_list(self):
		result = []
		for i in range(self.SIZE):
			for j in range(self.SIZE):
				if self.lattice[i][j] == ["*"]:
					elem_rxn = self.ELEMENTARY_RXNS[0]
					t = self._get_time(elem_rxn)
					p = Process(t, self.step, (i,j), elem_rxn)
					result = self._ordered_list_add(result, p)
				elif self.lattice[i][j] == ["A"]:
					elem_rxn = self.ELEMENTARY_RXNS[1]
					t = self._get_time(elem_rxn)
					p = Process(t, self.step, (i,j), elem_rxn)
					result = self._ordered_list_add(result, p)
		return result

	def _ordered_list_add(self, l, process):
		if len(l) == 0:
			return [process]
		for i in range(len(l)):
			if process.dt < l[i].dt:
				l.insert(i, process)
				return l
		l.append(process)
		return l


def main():
	kMC = kMC_Simulation()
	kMC.run()

if __name__ == '__main__':
	main()
