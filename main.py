import string
from collections import defaultdict
import datetime

class Vehichle:
    vehichles = {}
    def __init__(self, lisence: str, type: str):
        self.lno = lisence
        self.type = type
        self.status = "entry"
        self.sid = -1
        self.tid = -1
        # vehichles.
    
    # @classmethod
    # def vehichles_in_town():
    #     vehichles[lno]
        
    # items = {}

    # def __new__(cls, id, type):
    #     if id not in cls.items:
    #         cls.items[id] = super().__new__(cls)
    #         print(cls.items[id])
    #     return cls.items[id]




class Ticket(Vehichle):
    sid = checkin = checkout = 0
    def __init__(self, id : int, v : Vehichle, hour: int, sid: str):
        self.sid = sid
        self.vid = v.lno
        self.checkin = hour
        self.checkout = 0
        self.rate = 0
        self.tid = id 
    def display_ticket(self):
        print(f"Ticket ID: {self.tid}")
        print(f"VID: {self.vid}")
        print(f"Slot: {self.sid}")
        print(f"Check In: {self.checkin}")
        print(f"Check Out: {self.checkout}")
        print(f"Rate: {self.rate}")

# class Town:
#     def __init__(self):
#         self.vehichle_in_town = []
#     def add_vehichle(vehichle_in_town, lis, type):
#         v = Vehichle("456J", "Electric")
#         vehichle_in_town.append(v)

class Parking():
    levels = {}
    vehichle_in_town = {}
    def __init__(self, level: int ) : # slot_per_level: int):
        self.levels = defaultdict()
        self.noOfLevel = level
        self.pay = 50
        #self.slot_type = type
        #self.avbl = True
        #self.slotpl = slot_per_level
        #self.slots = {"Regular": 0, "Electric": 0, "Handicapped" : 0 }
    
    def create_slots_level(self, level: int, slots: dict) -> str:
        slotpl = {}
        if level >= self.noOfLevel:
            return "Exceeding existing Levels"
        for i in slots:
            s = [True] * slots[i]
            slotpl[i] = (slots[i], s)
        self.levels[level] = slotpl
        return "Created successfuly"
    
    def get_slot(self, lno: str) -> tuple:
        car = self.vehichle_in_town[lno]
        t = car.type
        for l in self.levels:
            lvl = self.levels[l]
            if any(lvl[t][1]):
                ind = lvl[t][1].index(True)
                return (l, ind)
        return (-1, -1)
    
    
    def book_slot(self, lno: str, hour: int) -> (str, Ticket):
        car =self.vehichle_in_town[lno]
        lvl, sid = self.get_slot(car.lno)
        if lvl == -1 and sid == -1 or car.status == "Parked":
            return "Rejected", None
        self.levels[lvl][car.type][1][sid] = False
        slotID = "L"+ str(lvl) + "S" + str(sid) + car.type[0]
        id = str(hour * (sid + 1)) + car.type[0]
        tkt = Ticket(id, car, hour, slotID)
        car.status = "Parked"
        car.sid = slotID
        return "Successfully parked", tkt
    
    def free_slot(self, lvl : int, lno: str, sid : int) -> None:
        car =self.vehichle_in_town[lno]
        self.levels[lvl][car.type][1][sid] = 0
    
    def exit_slot(self, lno: str, hour: int, tkt: Ticket) -> str:
        car =self.vehichle_in_town[lno]
        if car.status != "Parked":
            return "The car is not in Parking!"
        
        occupied_hours = (hour - tkt.checkin) % 24
        tkt.rate = occupied_hours * self.pay
        

        lvl, sid = int(tkt.sid[1]), int(tkt.sid[3:4])
        self.free_slot(lvl, lno, sid)

        car.status = "exit"
        tkt.checkout = hour
        return f"Rate: {tkt.rate}"
    def add_vehichle(self, lis, type):
        v = Vehichle(lis, type)
        self.vehichle_in_town[lis] = v
    

# class Slot:
#     def __init__(self, level: int, id: int, type: string):
#         self.level = level
#         self.sid = id
#         self.slot_type = type
#         self.avbl = True
        #self.slots = slots

# def add_vehichle(vehichle_in_town, lis, type):
#     v = Vehichle("456J", "Electric")
#     vehichle_in_town.append(v)

def main():
    park1 = Parking(3)
    park1.add_vehichle("456", "Electric")
    park1.add_vehichle("452","Electric" )
    print(park1.vehichle_in_town["456"])
    # v.append(park1)
    # v = Vehichle(456, "Regular")
    # v1 = Vehichle(452, "Electric")


    res = park1.create_slots_level(1, {"Regular": 3, "Electric": 0, "Handicapped" : 5 })
    res = park1.create_slots_level(2, {"Regular": 5, "Electric": 1, "Handicapped" : 1 })
    print(res)
    res = park1.create_slots_level(3, {"Regular": 4, "Electric": 0, "Handicapped" : 5 })
    print(res)
    print("working")
    print(park1.get_slot("456"))
    r, tkt = park1.book_slot("456", 2)
    print(r)
    print(park1.get_slot("452"))
    r1, tkt1 = park1.book_slot("452", 3)
    print(r1)
    e = park1.exit_slot("456",5, tkt)
    print(e)
    if tkt:
        tkt.display_ticket()
        print("------------------------")
    if tkt1:
        tkt1.display_ticket()
if __name__ == "__main__":
    main()