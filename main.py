import string
from collections import defaultdict

class Vehichle:
    def __init__(self, lisence: string, type: string):
        self.lno = lisence
        self.type = type
        self.status = "entry"
    def park_enter(park):
        #park.
        pass
# class Slot:
#     def __init__(self, level: int, id: int, type: string):
#         self.level = level
#         self.sid = id
#         self.slot_type = type
#         self.avbl = True
        #self.slots = slots

class Parking:
    levels = {}
    def __init__(self, level: int, slot_per_level: int):
        #self.slot_type = type
        #self.avbl = True
        self.slotpl = slot_per_level
        self.levels = defaultdict()
        #self.slots = {"Regular": 0, "Electric": 0, "Handicapped" : 0 }
    
    def create_slots_level(level: int, id: int, slots: dict):
        slotpl = {}
        for i in slots:
            s = [True] * slots[i]
            slotpl[i] = (i[s], s, i[s])
        self.levels[level] = slotpl
    
    def get_slot(car: Vehichle):
        t = car.type
        for l in self.levels:
            lvl = self.levels[l]
            if any(lvl[t][1]):
                ind = lvl[t][1].index(True)
                return l, ind
        return (-1, -1)
    def book_slot(car: Vehichle):
        lvl, sid = get_slot(car)
        if lvl != -1 

def __main__():
    park1 = Parking(3, 4)
    v = Vehichle("456J", "Regular")