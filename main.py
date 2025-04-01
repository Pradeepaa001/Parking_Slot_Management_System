import string
from collections import defaultdict
import datetime

class Vehichle:
    def __init__(self, lisence: string, type: string):
        self.lno = lisence
        self.type = type
        self.status = "entry"
        self.sid = -1

# class Slot:
#     def __init__(self, level: int, id: int, type: string):
#         self.level = level
#         self.sid = id
#         self.slot_type = type
#         self.avbl = True
        #self.slots = slots
class Ticket:
    sid = checkin = checkout = 0
    def __init__(self, v : Vehichle, hour: int, sid: string):
        self.sid = sid
        self.checkin = hour
        self.checkout = 0
        self. rate = 0 
    
class Parking:
    levels = {}
    def __init__(self, level: int, slot_per_level: int):
        #self.slot_type = type
        #self.avbl = True
        self.slotpl = slot_per_level
        self.levels = defaultdict()
        self.pay = 50
        #self.slots = {"Regular": 0, "Electric": 0, "Handicapped" : 0 }
    
    def create_slots_level(level: int, id: int, slots: dict) -> None:
        slotpl = {}
        for i in slots:
            s = [True] * slots[i]
            slotpl[i] = (i[s], s)
        self.levels[level] = slotpl
    
    def get_slot(car: Vehichle) -> tuple:
        t = car.type
        for l in self.levels:
            lvl = self.levels[l]
            if any(lvl[t][1]):
                ind = lvl[t][1].index(True)
                return l, ind
        return (-1, -1)
    
    def book_slot(car: Vehichle, hour: int) -> string:
        lvl, sid = self.get_slot(car)
        if lvl == -1 and sid == -1:
            return "Rejected"
        self.levels[lvl][sid] = False
        slotID = "L"+ string(lvl) + "S" + string(sid)
        tkt = Ticket(car, hour, slotID)
        car.status = "Parked"
        car.sid = slotID
        return "Successfully parked"
    
    def free_slot(lvl : int, sid : int) -> None:
        self.levels[lvl][sid] = True
    
    def exit_slot(car: Vehichle, hour: int, tkt: Ticket) -> string:
        if car.status != "Parked":
            return "The car is not in Parking!"
        
        occupied_hours = (hour - tkt.checkin) % 24
        tkt.rate = occupied_hours * self.pay
        

        lvl, sid = int(tkt.sid[1]), int(tkt.sid[3:])
        self.free_slot(lvl, sid)

        car.status = "exit"
        return f"Rate: {tkt.rate}"
    







def __main__():
    park1 = Parking(3, 4)
    v = Vehichle("456J", "Regular")