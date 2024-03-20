from __future__ import annotations

import numpy as np
import inspect
import parameters.cell_rules as cr
import parameters.env_rules as er
from classes.environment import Environment

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from parameters.env_rules import EnvRule
    from parameters.cell_rules import CellRule

class Simulation:
    def __init__(self, envrule: str | EnvRule, cellrule: str | CellRule, local=False):
        self.update_took = 0.0
        
        if local:
            self.envrule = getattr(er, envrule)()
            self.cellrule = getattr(cr, cellrule)()
            self.env = Environment(self.envrule, self.cellrule) # Initialize the environment
            self.update_rules(new_envrule=self.envrule, new_cellrule=self.cellrule)
        
        else:
            if not inspect.isclass(cellrule) and inspect.isclass(envrule):
                raise AttributeError(f'"local" parameter specified as {local}, therefore parameters "cellrule" and "envrule" must be classes')
            
            self.envrule = envrule
            self.cellrule = cellrule
            self.env = Environment(self.envrule, self.envrule)
        
        self.env.x = []
        
    def update_rules(self, new_params=None, new_envrule=None, new_cellrule=None):
        if new_params: 
            self.params.update_params(new_params)
            
        if new_envrule:
            envrules = inspect.getmembers(er, inspect.isclass) # Get all rules as functions
            self.envrule = next((r for r in envrules if r[0] == type(new_envrule).__name__), None)[1]() # Get the first object that matches the wanted envrule
            if not self.envrule: raise AttributeError(f"{new_envrule} is not a valid simulation ruleset. [{', '.join(r[0] for r in envrules)}]")
            self.env.envrule = self.envrule # Bind the desired rule method to the environment
        
        if new_cellrule: 
            cellrules = inspect.getmembers(cr, inspect.isclass) 
            cellrule = next((r for r in cellrules if r[0] == type(new_cellrule).__name__), None)[1]()
            if not cellrule: raise AttributeError(f"{new_cellrule} is not a valid cell ruleset. [{', '.join(r[0] for r in cellrules)}]")
            self.env.cellrule = cellrule
            [c.set_attributes(new_cell_rule=cellrule) for c in self.env.cells]

    def next(self):
        return self.env.next()

    def restart(self):
        self.env = Environment(self.envrule, self.cellrule)
        self.update_rules(new_envrule=self.envrule, new_cellrule=self.cellrule)