import inspect
import src.rules.cell_rules as cr
import src.rules.env_rules as er
from src.environment import Environment

class Simulation:
    def __init__(self, params, wenvrule="env_rule2", wcellrule="cell_rule1"):
        self.update_params(params)
        self.env = Environment(params) # Initialize the environment
        self.update_rules(wenvrule, wcellrule)
 
    def update_params(self, new_params):
        self.params = new_params
        
    def update_rules(self, new_envrule=None, new_cellrule=None):
        if new_envrule:
            envrules = inspect.getmembers(er, inspect.isfunction) # Get all rules as functions
            self.envrule = next((r for r in envrules if r[0] == new_envrule), None) # Get the first object that matches the wanted envrule
            if not self.envrule: raise AttributeError(f"{new_envrule} is not a valid simulation ruleset. [{', '.join(r[0] for r in envrules)}]")
            setattr(self.env, self.envrule[0], self.envrule[1]) # Bind the desired rule method to the environment
        
        if new_cellrule: 
            cellrules = inspect.getmembers(cr, inspect.isfunction) 
            cellrule = next((r for r in cellrules if r[0] == new_cellrule), None)
            if not cellrule: raise AttributeError(f"{new_cellrule} is not a valid cell ruleset. [{', '.join(r[0] for r in cellrules)}]")
            self.env.cellrule = cellrule
        
            for c in self.env.cells:
                setattr(c, cellrule[0], cellrule[1])
                c.cellrule = cellrule

    def next(self):
        getattr(self.env, self.envrule[0])(self.env)