#Model design
import agentpy as ap

class ForestModel(ap.Model):

    def setup(self):
        # Create Agents (trees)
        n_trees = int(self.p['Tree density'] * (self.p.size**2))
        trees = self.agents = ap.AgentList(self, n_trees)

        # Create Grid (forest)
        self.forest = ap.Grid(self, [self.p.size]*2, track_empty=True)
        self.forest.add_agents(trees, random=True, empty=True)

        # Initiate a dynamic variable for all trees
        # Condition 0: Alive
        # Condition 1: Burning is L I T
        # Condition 2: Burned rip
        self.agents.condition = 0

        # Start a fire from left side of the grid
        unfortunate_trees = self.forest.agents[0:self.p.size, 0:2]
        unfortunate_trees.condition = 1

    def step(self):

        # Select burning trees
        burning_trees = self.agents.select(self.agents.condition == 1)

        # Spread fire
        for tree in burning_trees:
            for neighbor in self.forest.neighbors(tree):
                if neighbor.condition == 0:
                    neighbor.condition = 1 # Haha neighbor goes brrr
            tree.condition = 2 # Tree burned out

        # Stop simulation if no fire is left
        if len(burning_trees) == 0:
            self.stop()

    def end(self):
        # Document a measure at the end of the simulation
        burned_trees = len(self.agents.select(self.agents.condition == 2))
        self.report('Percentage of burned trees', burned_trees / len(self.agents))

parameters = {
    'Tree density': 0.6, # Percentage of grid covered by trees
    'size' : 50, # Height and Length of the grid
    'steps': 100,
}

print('')

model = ForestModel(parameters)
result = model.run()

# Console Out 
print('-- Burning Tree Simulation Results --')
print('Initial Parameters:')
print('Tree Density:', parameters.get('Tree density'))
print('Height and Length of the grid:', parameters.get('size'))
print('Steps:', parameters.get('steps'))
print(result.reporters)

print('')
