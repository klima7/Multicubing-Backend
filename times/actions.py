from .models import Turn
from room.models import Room


def start_new_turn_if_needed(room: Room):
    if _check_new_turn_needed(room):
        print('Starting turn')
        _start_new_turn(room)


def _check_new_turn_needed(room: Room):
    times = room.last_turn.time_set.all()
    if not times:
        return False
    solved_users = [time.user.username for time in times]
    active_participants = room.participant_set.filter(spectator=False, active=True).all()
    for participant in active_participants:
        if participant.user.username not in solved_users:
            return False
    return True


def _start_new_turn(room: Room):
    last_turn = room.last_turn
    last_number = last_turn.number if last_turn else 0
    new_turn = Turn(room=room, number=last_number+1, scramble='Some scramble')
    new_turn.save()
