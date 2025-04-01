from collections import defaultdict

class Vehichle:
    vehichles = {}
    def __init__(self, lisence: str, type: str):
        self.liscence_no = lisence
        self.type = type
        self.status = "entry"
        self.slot_id = -1

class Ticket(Vehichle):
    slot_id = checkin = checkout = 0
    def __init__(self, id : int, v : Vehichle, hour: int, slot_id: str):
        self.slot_id = slot_id
        self.vid = v.liscence_no
        self.checkin = hour
        self.checkout = 0
        self.rate = 0
    def display_ticket(self):
        print(f"Ticket ID: {self.tid}")
        print(f"VID: {self.vid}")
        print(f"Slot: {self.slot_id}")
        print(f"Check In: {self.checkin}")
        print(f"Check Out: {self.checkout}")
        print(f"Rate: {self.rate}")


class Parking():
    levels = {}
    vehichle_in_town = {}
    cars_reserve = {}
    def __init__(self, level: int ) : 
        self.levels = defaultdict()
        self.noOfLevel = level
        self.pay = 50
        self.waitlist = defaultdict(list)
        self.cars_reserve = defaultdict(tuple)
    
    def create_slots_level(self, level: int, slots: dict) -> str:
        slotpl = {}
        if level >= self.noOfLevel:
            return "Exceeding existing Levels"
        for i in slots:
            s = [True] * slots[i]
            slotpl[i] = (slots[i], s)
        self.levels[level] = slotpl
        return "Created successfuly"
    
    def get_slot(self, liscence_no: str) -> tuple:
        car = self.vehichle_in_town[liscence_no]
        t = car.type
        for l in self.levels:
            lvl = self.levels[l]
            if any(lvl[t][1]):
                ind = lvl[t][1].index(True)
                return (l, ind)
        return (-1, -1)
    def chk_reservation(self, slotId, hour):
        for liscence_no in self.cars_reserve:
            if slotId == self.cars_reserve[liscence_no][2] and hour >= self.cars_reserve[liscence_no][0] and hour <= self.cars_reserve[liscence_no][1]:
                return True
        return False
    
    def book_slot(self, liscence_no: str, hour: int) -> (str, Ticket):
        car =self.vehichle_in_town[liscence_no]
        lvl, slot_id = self.get_slot(car.liscence_no)
        if car.status == "Parked":
            return "Already parked", None
        
        if lvl == -1 and slot_id == -1 :
            self.waitlist[car.type].append(car)
            car.status = "waiting"
            # print(self.waitlist)
            return "waiting", None
        
        slotID = "L"+ str(lvl) + "S" + str(slot_id) + car.type[0]
        id = str(hour * (slot_id + 1)) + car.type[0]
        
        if self.chk_reservation(slotID, hour):
            self.waitlist[car.type].append(car)
            car.status = "waiting"
            return "Already Booked", None
        
        self.levels[lvl][car.type][1][slot_id] = False
        tkt = Ticket(id, car, hour, slotID)
        # self.cars_in_park[car.liscence_no] = tkt
        car.status = "Parked"
        car.slot_id = slotID
        return "Successfully parked", tkt
    
    def free_slot(self, lvl : int, liscence_no: str, slot_id : int) -> None:
        car =self.vehichle_in_town[liscence_no]
        self.levels[lvl][car.type][1][slot_id] = 0
    
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
    
    def exit_slot(self, liscence_no: str, hour: int, tkt: Ticket) -> str:
        car =self.vehichle_in_town[liscence_no]
        if car.status != "Parked":
            return "The car is not in Parking!"
        
        occupied_hours = (hour - tkt.checkin) % 24
        tkt.rate = self.rate(occupied_hours)
        

        lvl, slot_id = int(tkt.slot_id[1]), int(tkt.slot_id[3:4])
        self.free_slot(lvl, liscence_no, slot_id)

        car.status = "exit"
        tkt.checkout = hour
        if self.waitlist[car.type] != []:
            self.move_waitlist(car.type)
        return f"Rate: {tkt.rate}"
    
    def add_vehichle(self, lis, type) -> None:
        v = Vehichle(lis, type)
        self.vehichle_in_town[lis] = v
    
    def move_waitlist(self,car_type : str)-> None:
        waitCar = self.waitlist[car_type].pop(0)
        _, tkt = self.book_slot(waitCar.liscence_no, 12)
        print (f"{waitCar.liscence_no} is now parked from waiting list")

    def book_reservation(self, liscence_no: str, car_type: str, hour: int, out : int) -> None:
        car =self.vehichle_in_town[liscence_no]
        lvl, slot_id = self.get_slot(liscence_no)
        if lvl == -1 and slot_id == -1:
            print("car not booked")
            return        

        print(lvl, slot_id)
        slotID = "L"+ str(lvl) + "S" + str(slot_id) + car.type[0]
        id = str(hour * (slot_id + 1)) + car.type[0]
        tkt = Ticket(id, car, hour, slotID)
        tkt.checkout = out
        occupied_hours = (hour - out) % 24
        tkt.rate = self.rate(occupied_hours)
        self.cars_reserve[car.liscence_no] = (tkt.checkin, tkt.checkout, tkt.slot_id)
        car.status = "booked"
        print("car booked")






    
def main():
    park1 = Parking(3)
    park1.add_vehichle("456", "Electric")
    park1.add_vehichle("452","Electric" )
    park1.add_vehichle("416","Electric" )

    # print(park1.vehichle_in_town["456"])
    
    res = park1.create_slots_level(1, {"Regular": 3, "Electric": 0, "Handicapped" : 5 })
    res = park1.create_slots_level(2, {"Regular": 5, "Electric": 1, "Handicapped" : 1 })
    print(res)
    res = park1.create_slots_level(3, {"Regular": 4, "Electric": 0, "Handicapped" : 5 })
    print(res)
    print("working")
    park1.book_reservation("416", "Electric", 2, 7)
    print(park1.get_slot("456"))
    r, tkt = park1.book_slot("456", 2)
    print(r)
    print(park1.get_slot("452"))
    r1, tkt1 = park1.book_slot("452", 3)
    print(r1)
    print("going to exit")
    e = park1.exit_slot("456",18, tkt)
    print(e)
    if tkt:
        tkt.display_ticket()
        print("------------------------")
    if tkt1:
        tkt1.display_ticket()
if __name__ == "__main__":
    main()