from collections import defaultdict

class Vehichle:
    vehichles = {}
    def __init__(self, lisence: str, type: str):
        self.lno = lisence
        self.type = type
        self.status = "entry"
        self.sid = -1
        self.tid = -1

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


class Parking():
    levels = {}
    vehichle_in_town = {}
    def __init__(self, level: int ) : 
        self.levels = defaultdict()
        self.noOfLevel = level
        self.pay = 50
        self.waitlist = defaultdict(list)

    
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
        if car.status == "Parked":
            return "Already parked", None
        if lvl == -1 and sid == -1 :
            self.waitlist[car.type].append(car)
            car.status = "waiting"
            # print(self.waitlist)
            return "waiting", None
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
    
    def rate(self, park_hour: int) -> int:
        if park_hour < 4:
            return 50
        elif park_hour < 10:
            rem_hour = park_hour - 4
            return 50 + rem_hour * 10
        elif park_hour < 18:
            rem_hour = park_hour - 14
            return 50 + (park_hour - 4) * 10 + rem_hour * 20
        else:
            rem_hour = park_hour - 18
            return 50 + (park_hour - 4) * 10 + (park_hour - 10) * 20 + rem_hour * 30
    
    def exit_slot(self, lno: str, hour: int, tkt: Ticket) -> str:
        car =self.vehichle_in_town[lno]
        if car.status != "Parked":
            return "The car is not in Parking!"
        
        occupied_hours = (hour - tkt.checkin) % 24
        tkt.rate = self.rate(occupied_hours)
        

        lvl, sid = int(tkt.sid[1]), int(tkt.sid[3:4])
        self.free_slot(lvl, lno, sid)

        car.status = "exit"
        tkt.checkout = hour
        if self.waitlist[car.type] != []:
            self.move_waitlist(car.type)
        return f"Rate: {tkt.rate}"
    def add_vehichle(self, lis, type):
        v = Vehichle(lis, type)
        self.vehichle_in_town[lis] = v
    
    def move_waitlist(self,car_type : str):
        waitCar = self.waitlist[car_type].pop(0)
        _, tkt = self.book_slot(waitCar.lno, 12)
        print (f"{waitCar.lno} is now parked from waiting list")


    
def main():
    park1 = Parking(3)
    park1.add_vehichle("456", "Electric")
    park1.add_vehichle("452","Electric" )
    # print(park1.vehichle_in_town["456"])

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
    e = park1.exit_slot("456",18, tkt)
    print(e)
    if tkt:
        tkt.display_ticket()
        print("------------------------")
    if tkt1:
        tkt1.display_ticket()
if __name__ == "__main__":
    main()