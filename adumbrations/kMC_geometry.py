"""
File: kMC_geometry.py
---------------------
Two simple functions to translate an elementary reaction definition
to an origin and then generate three equivalent elementary reactions 
rotated 90, 180, and 270 degrees.
"""


def adjust_elem_rxn_spec(spec):
	min_x = float("inf")
	min_y = float("inf")
	for key in spec:
		x = key[0]
		if x<min_x:
			min_x = x
		y = key[1]
		if y<min_y:
			min_y = y
	adjusted_spec = {}
	for key in spec:
		x = key[0]
		y = key[1]
		s = key[2]
		adjusted_spec[(x-min_x, y-min_y, s)] = spec[key]
	return adjusted_spec

def generate_rotated_specs(spec):
	rot_90 = {}
	rot_180 = {}
	rot_270 = {}
	for key in spec:
		x = key[0]
		y = key[1]
		s = key[2]
		rot_90[(y, -x, s)] = spec[key]
		rot_180[(-y, -x, s)] = spec[key]
		rot_270[(-y, x, s)] = spec[key]
	return [rot_90, rot_180, rot_270]

def main():
	spec = {(5,5,0): ("*", "A"), (6,6,0): ("*", "A"),(5,6,0): ("*", "A")}
	adjust = adjust_elem_rxn_spec(spec)
	rots = generate_rotated_specs(adjust)
	print("The spec left and upper adjusted: ",adjust)
	print("\nThe spec rotated 90, 180, and 270 degrees: ")
	for key in rots:
		print(key)

if __name__ == '__main__':
	main()



