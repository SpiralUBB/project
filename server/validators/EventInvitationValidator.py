from models.EventInvitation import event_invitation_status_map, event_invitation_attend_status_map
from utils.errors import EventInvitationStatusInvalid, EventInvitationAttendStatusInvalid


class EventInvitationValidator:
    def parse_status(self, value):
        if value is None:
            raise EventInvitationStatusInvalid(message='Event invitation status cannot be empty')

        try:
            value = int(value)
        except ValueError:
            pass

        value = event_invitation_status_map.to_key_either(value)
        if value < 0:
            raise EventInvitationStatusInvalid(message='Event invitation status cannot be found inside the predefined '
                                                       'list')

        return value

    def parse_attend_status(self, value):
        if value is None:
            raise EventInvitationAttendStatusInvalid(message='Event invitation attend status cannot be empty')

        try:
            value = int(value)
        except ValueError:
            pass

        value = event_invitation_attend_status_map.to_key_either(value)
        if value < 0:
            raise EventInvitationAttendStatusInvalid(message='Event invitation attend status cannot be found inside '
                                                             'the predefined list')

        return value
