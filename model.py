from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from random import randrange
import math


class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, pos, model):
        """
         Create a new Schelling agent.
         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos

    def step(self):

        oxy_level = self.model.get_oxygen(self.pos[0],self.pos[1])
        c,d,oxy_grad = self.model.get_oxy_grad(self.pos[0],self.pos[1])
        a=int(c)
        b=int(d)
        try:
            if not self.model.grid.out_of_bounds((self.pos[0]+a,self.pos[1]+b)):
                if oxy_level <5:
                    self.model.grid.move_agent(self,(self.pos[0]+a,self.pos[1]+b))
            if not self.model.grid.out_of_bounds((self.pos[0]-a,self.pos[1]-b)):
                if oxy_level >12:
                    self.model.grid.move_agent(self,(self.pos[0]-a,self.pos[1]-b))
        except:
            try:
                n=1
                if oxy_level <5:
                    while(1):
                        if self.model.grid.is_cell_empty((self.pos[0]+(a*n),self.pos[1]+(b*n))):
                            self.model.grid.move_agent(self.model.grid[self.pos[0]+(n-1)][self.pos[1]+(n-1)],(self.pos[0]+n,self.pos[1]+n))
                            break
                        else:
                            n+=1
                n=1
                if oxy_level >12:
                    while(1):
                        if self.model.grid.is_cell_empty((self.pos[0]-(a*n),self.pos[1]-(b*n))):
                            for m in range(n):            
                                self.model.grid.move_agent(self.model.grid[self.pos[0]-(n-m-1)][self.pos[1]-(n-m-1)],(self.pos[0]-n-m,self.pos[1]-n-m))
                            break
                        else:
                            n+=1
            except:
                self.model.grid.move_agent(self,self.pos)

            #if not self.model.grid.out_of_bounds((self.pos[0]+a,self.pos[1]+b)):
            #    m = self.model.grid[self.pos[0]+a][self.pos[1]+b]
            #    self.model.grid.remove_agent(self.model.grid[self.pos[0]+a][self.pos[1]+b])
            #    self.model.grid.move_agent(self,(self.pos[0]+a,self.pos[1]+b))
            #    self.model.grid.place_agent(m,(self.pos[0]-a,self.pos[1]-b))
            #    #self.model.grid.place_agent(m,(m.pos[0],m.pos[1]))
            #    #self.model.grid.move_agent(self.model.grid[w2][w1],(self.pos[0]-a,self.pos[1]-b))

class Model(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=30, width=30, density=0.1, oxy_den_count = 1):
        """
        """

        self.height = height
        self.width = width
        self.density = density

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)
        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                agent = SchellingAgent((x, y), self)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    def get_height():
        return self.height
    def get_width():
        return self.width

    def get_oxygen(self,x,y):
        return -1*pow((x/5)-5,2) -pow((y/5)-5,2) +25
    def get_oxy_grad(self, x, y):
        a = -(((2*x)/25) -2)
        b = -(((2*y)/25) -2)
        if  abs(b) != 0:
            b = b / abs(b)
        if abs(a) != 0:
            a = a / abs(a)

        total = -1*a - b
        return a,b,total

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
