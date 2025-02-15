from entity.fan_id_cardEntity import FanIDCardEntity
from entity.matchesEntity import MatchEntity
from entity.personEntity import PersonEntity
from entity.ticketEntity import TicketEntity
from domain.person import Person
from domain.seat import Seat
from domain.ticket import SingleTicket
import random

class NobodyBuyTickets(Exception):
    pass
class Organizer(Person):

    def __init__(self, username, first_name, last_name, age, password):
        super().__init__(username, first_name, last_name, age, password, "organizer")

    @staticmethod
    def add_match(match):
        new_match_id = MatchEntity.add_match(match)
        match.id = new_match_id
        seats = Seat.get_seats()
        id = random.sample(range(10000000, 99999999), len(seats))
        cnt = 0
        for seat in seats:
            price = 20 * seat.block + 5 * seat.row + 3 * seat.place + 0.99
            ticket = SingleTicket(id[cnt], None, price, match, seat)
            cnt += 1
            TicketEntity.add_ticket(ticket)

    @staticmethod
    def update_match(match):
        MatchEntity.update_match(match)

    @staticmethod
    def delete_match(match_id):
        TicketEntity.delete_tickets_by_match_id(match_id)
        MatchEntity.delete_match(match_id)

    @staticmethod
    def cancel_match(match_id):
        paid_money = TicketEntity.get_paid_money(match_id)
        cnt = 0
        for card_id, price in paid_money:
            if not card_id == "NULL":
                FanIDCardEntity.increase_balance(card_id, price)
                cnt += 1
        TicketEntity.delete_tickets_by_match_id(match_id)
        MatchEntity.delete_match(match_id)
    @staticmethod
    def construct(username):
        row = PersonEntity.get_by_id(username)
        return Organizer(row[0], row[1], row[2], row[3], row[5])