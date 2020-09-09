from config import *


def disable_bot(bot_id):
    target_error, target_data = p3cwTarget.request(
            entity='bots',
            action='disable',
            action_id=str(bot_id)
        )
    return target_error, target_data


def enable_bot(bot_id):
    target_error, target_data = p3cwTarget.request(
            entity='bots',
            action='enable',
            action_id=str(bot_id)
        )
    return target_error, target_data