from django.db import models

# Create your models here.

SERV_OIL = 0
SERV_TIRES = 1
SERV_DIAG = 2


serv_times = {
    SERV_OIL: 2,
    SERV_TIRES: 5,
    SERV_DIAG: 30
}

last_ticket_id = 0


def new_ticket(serv_type):
    global last_ticket_id
    last_ticket_id += 1
    return Ticket(last_ticket_id, serv_type)


class Ticket:
    def __init__(self, id, serv_type):
        self.id = id
        self.serv_type = serv_type


class ServQueue:
    def __init__(self):
        self.q = {}
        for s in serv_times.keys():
            self.q[s] = []

    def add(self, ticket):
        wait_time = self.wait_time_for(ticket.serv_type)
        self.q[ticket.serv_type].append(ticket)
        return wait_time

    def wait_time_for(self, serv_type):
        res = 0
        for s, t in serv_times.items():
            res += len(self.q[s]) * t
            if s == serv_type:
                break
        return res


queue = ServQueue()
