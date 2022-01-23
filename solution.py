import copy
import math

class Node():
	def __init__(self, index, distance, edges=[]):
		"""The node in the map"""
		self.index = index # the index of the node in the nodes list
		self.distance = distance # the distance from the current node to the goal node
		self.edges = edges # the edges with the node

	def __repr__(self):
		return str(self.index)

	def __iter__(self):
		yield 'index', self.index
		yield 'distance', self.distance,
		edges = []
		for edge in self.edges:
			edges.append( str(edge) )
		yield 'edges', str( ', '.join(edges) )

class Edge():
	def __init__(self, start_node_index, end_node_index, cost):
		self.start_node_index = start_node_index
		self.end_node_index = end_node_index
		self.cost = cost # the cost of moving from start node to end node and vice versa

	def __repr__(self):
		return f"to node {self.end_node_index}, cost: {self.cost}"

class Path():
	def __init__(self, map_nodes, init_node=None):
		self.path_nodes = [] # the nodes in the path
		self.mapped_nodes = map_nodes # the nodes in the nodes list 
		self.frontier_node = init_node # the node in the path frontier
		self.cost = 0 # the total cost of the path so far
		self.distance = 0 # the distance from the frontier node to the goal node


	def __repr__(self):
		nodes_indexes = list( test_map(lambda node: str(node.index), self.path_nodes) )
		nodes_indexes += [str(self.frontier_node.index)]
		return ' -> '.join(nodes_indexes)


	def move_to_next_node(self):
		"""Move the path to the next frontier and return the current path and any path
		created from it
		"""
		returned_paths = []
		self.path_nodes.append(self.frontier_node)
		for index, edge in enumerate(self.frontier_node.edges):
			next_node = self.mapped_nodes[ edge.end_node_index ]
			cost = self.cost + edge.cost
			distance = next_node.distance
			if index == 0:
				self.frontier_node = next_node
				self.cost = cost
				self.distance = distance
				returned_paths.append(self)
			else:
				new_path = copy.deepcopy(self)
				new_path.frontier_node = next_node
				new_path.cost = cost
				new_path.distance = distance
				returned_paths.append(new_path)

		return returned_paths



class GraphMap():
	def __init__(self, roads, intersections, start_index, goal_index):

		def _calucate_distance_or_cost(node_1, node_2):
			""" Used to calculated the distance or cost between 2 nodes"""
			if node_1[0] == node_2[0] and node_1[1] == node_2[1]:
				return 0
			elif node_1[0] == node_2[0]:
				return abs( node_1[1] - node_2[1] )
			elif node_1[1] == node_2[1]:
				return abs( node_1[0] - node_2[0] )
			else:
				width = abs( node_2[0] - node_1[0])
				height = abs( node_2[1] - node_1[1])
				return math.sqrt( width ** 2 + height ** 2 )

		def _format_nodes(roads, intersections):
			""" create the needed nodes format for the GraphMap class """
			nodes = []
			goal_axis = intersections[goal_index]
			for node_index, edges_indexes in enumerate(roads):
				node_axis = intersections[node_index]
				node_distance = _calucate_distance_or_cost(node_axis,  goal_axis)
				edges = []
				for edge_node_index in edges_indexes:
					next_node_axis = intersections[edge_node_index]
					edge_cost = _calucate_distance_or_cost(node_axis, next_node_axis)
					new_edge = Edge(
						node_index,
						edge_node_index,
						edge_cost
					)

					edges.append(new_edge)

				node = Node(
					node_index,
					node_distance,
					edges
				)

				nodes.append(node)

			return nodes

		self.nodes = _format_nodes(roads, intersections)
		self.start_node = self.nodes[start_index]
		self.goal_node = self.nodes[goal_index]
		self.shortes_path = None
		self.frontier = set()
		self.explored = set()
		self.paths = self._create_init_path()
		self._on_paths_update(self.start_node)


	def __repr__(self):
		nodes = []
		for node in self.nodes:
			nodes.append( str( dict(node) ) )
		return "\n".join(nodes)


	def _update_frontier(self):
		""" called whenever an update to explored nodes is made """
		frontier = map(lambda path: path.frontier_node.index, self.paths)
		frontier = filter(lambda node: node not in self.explored, frontier)
		self.frontier = set(frontier)


	def _on_paths_update(self, new_node):
		""" called whenecer an update on the paths is made """
		if new_node in self.frontier:
			self.frontier.remove(new_node)
		self.explored.add(new_node.index)
		self._update_frontier()


	def _create_init_path(self):
		""" create the initial path from the start node """
		init_paths = Path(self.nodes, self.start_node)
		init_paths = init_paths.move_to_next_node()
		init_paths = set(init_paths)
		return init_paths


	def move_to_next_node(self):
		""" find the next node with least distance & cost, and move towards it """
		paths = sorted(self.paths, key=lambda path: path.distance + path.cost)
		min_total_path = paths[0]
		moved_node = min_total_path.frontier_node
		new_paths = min_total_path.move_to_next_node()
		# we check if new paths are created after progressing in the frontier node
		if len(new_paths) > 1:
			# only add the newly created paths
			for path in new_paths[1:]:
				self.paths.add(path)
		self._on_paths_update(moved_node)
		if moved_node.index == self.goal_node.index:
			self.shortes_path = min_total_path

	def find_shortest_path(self):
		while not self.shortes_path:
			self.move_to_next_node()
		shortest_path_index = list( map(lambda node: node.index, self.shortes_path.path_nodes) )
		return shortest_path_index


def shortest_path(map, start, goal):
	print("shortest path called")
	graph_map = GraphMap(map.roads, map.intersections, start, goal)
	return graph_map.find_shortest_path()


if __name__ == "__main__":

	class TestMap():
		def __init__(self, roads, intersections):
			self.roads = roads
			self.intersections = intersections

	# Shows the full connectivity of the map
	roads = [
		[36, 34, 31, 28, 17],
		[35, 31, 27, 26, 25, 20, 18, 17, 15, 6],
 		[39, 36, 21, 19, 9, 7, 4],
		[35, 20, 15, 11, 6],
		[39, 36, 21, 19, 9, 7, 2],
		[32, 16, 14],
		[35, 20, 15, 11, 1, 3],
		[39, 36, 22, 21, 19, 9, 2, 4],
		[33, 30, 14],
		[36, 21, 19, 2, 4, 7],
		[31, 27, 26, 25, 24, 18, 17, 13],
		[35, 20, 15, 3, 6],
		[37, 34, 31, 28, 22, 17],
		[27, 24, 18, 10],
		[33, 30, 16, 5, 8],
		[35, 31, 26, 25, 20, 17, 1, 3, 6, 11],
		[37, 30, 5, 14],
		[34, 31, 28, 26, 25, 18, 0, 1, 10, 12, 15],
		[31, 27, 26, 25, 24, 1, 10, 13, 17],
		[21, 2, 4, 7, 9],
		[35, 26, 1, 3, 6, 11, 15],
		[2, 4, 7, 9, 19],
		[39, 37, 29, 7, 12],
		[38, 32, 29],
		[27, 10, 13, 18],
		[34, 31, 27, 26, 1, 10, 15, 17, 18],
		[34, 31, 27, 1, 10, 15, 17, 18, 20, 25],
		[31, 1, 10, 13, 18, 24, 25, 26],
		[39, 36, 34, 31, 0, 12, 17],
		[38, 37, 32, 22, 23],
		[33, 8, 14, 16],
		[34, 0, 1, 10, 12, 15, 17, 18, 25, 26, 27, 28],
		[38, 5, 23, 29],
		[8, 14, 30],
		[0, 12, 17, 25, 26, 28, 31],
		[1, 3, 6, 11, 15, 20],
		[39, 0, 2, 4, 7, 9, 28],
		[12, 16, 22, 29],
		[23, 29, 32],
		[2, 4, 7, 22, 28, 36]
	]

	# x,y cordinates for each node
	intersections = {
		0: [0.7801603911549438, 0.49474860768712914],
		1: [0.5249831588690298, 0.14953665513987202],
		2: [0.8085335344099086, 0.7696330846542071],
		3: [0.2599134798656856, 0.14485659826020547],
		4: [0.7353838928272886, 0.8089961609345658],
		5: [0.09088671576431506, 0.7222846879290787],
		6: [0.313999018186756, 0.01876171413125327],
		7: [0.6824813442515916, 0.8016111783687677],
		8: [0.20128789391122526, 0.43196344222361227],
		9: [0.8551947714242674, 0.9011339078096633],
		10: [0.7581736589784409, 0.24026772497187532],
		11: [0.25311953895059136, 0.10321622277398101],
		12: [0.4813859169876731, 0.5006237737207431],
		13: [0.9112422509614865, 0.1839028760606296],
		14: [0.04580558670435442, 0.5886703168399895],
		15: [0.4582523173083307, 0.1735506267461867],
		16: [0.12939557977525573, 0.690016328140396],
		17: [0.607698913404794, 0.362322730884702],
		18: [0.719569201584275, 0.13985272363426526],
		19: [0.8860336256842246, 0.891868301175821],
		20: [0.4238357358399233, 0.026771817842421997],
		21: [0.8252497121120052, 0.9532681441921305],
		22: [0.47415009287034726, 0.7353428557575755],
		23: [0.26253385360950576, 0.9768234503830939],
		24: [0.9363713903322148, 0.13022993020357043],
		25: [0.6243437191127235, 0.21665962402659544],
		26: [0.5572917679006295, 0.2083567880838434],
		27: [0.7482655725962591, 0.12631654071213483],
		28: [0.6435799740880603, 0.5488515965193208],
		29: [0.34509802713919313, 0.8800306496459869],
		30: [0.021423673670808885, 0.4666482714834408],
		31: [0.640952694324525, 0.3232711412508066],
		32: [0.17440205342790494, 0.9528527425842739],
		33: [0.1332965908314021, 0.3996510641743197],
		34: [0.583993110207876, 0.42704536740474663],
		35: [0.3073865727705063, 0.09186645974288632],
		36: [0.740625863119245, 0.68128520136847],
		37: [0.3345284735051981, 0.6569436279895382],
		38: [0.17972981733780147, 0.999395685828547],
		39: [0.6315322816286787, 0.7311657634689946]
	}

	test_map = TestMap(roads, intersections)
	print( shortest_path(test_map, start=5, goal=34) )