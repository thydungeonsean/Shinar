import code.entities.actions as actions
import code.entities.troop as tr
from code.constants import *

t = tr.Archer('a', 'ea', RED)
m = actions.Move('b', t, (1, 0), (2, 0))
for i in range(60):
    m.run()
