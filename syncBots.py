from config import *
from botUtil import *

def get_bot_id_from_name(name, bots):
    for bot in bots:
        if (bot["name"] == name):
            return bot["id"]
    return None


def get_bot(name, bots):
    for bot in bots:
        if (bot["name"] == name):
            return bot
    return None

def update_bot_pairs(bot, pairs=None, strategy_list=None, take_profit=None,
                     trailing_enabled=None, trailing_deviation=None):
    bot_id = bot["id"]
    print("Target Bot id for " + bot["name"] + " is: " + str(bot_id))

    if pairs is None:
        pairs = bot["pairs"]

    if strategy_list is None:
        strategy_list = bot["strategy_list"]

    if take_profit is None:
        take_profit = bot["take_profit"]

    if trailing_deviation is None:
        trailing_deviation = bot["trailing_deviation"]

    if trailing_enabled is None:
        trailing_enabled = bot["trailing_enabled"]

    bot_payload = {
        "name": bot["name"],
        "base_order_volume": bot["base_order_volume"],
        "take_profit": take_profit,
        "safety_order_volume": bot["safety_order_volume"],
        "martingale_volume_coefficient": bot["martingale_volume_coefficient"],
        "martingale_step_coefficient": bot["martingale_step_coefficient"],
        "max_safety_orders": bot["max_safety_orders"],
        "active_safety_orders_count": bot["active_safety_orders_count"],
        "safety_order_step_percentage": bot["safety_order_step_percentage"],
        "take_profit_type": bot["take_profit_type"],
        "strategy_list": strategy_list,
        "stop_loss_percentage": bot["stop_loss_percentage"],
        "cooldown": bot["cooldown"],
        "max_active_deals": bot["max_active_deals"],
        "trailing_enabled": trailing_enabled,
        "trailing_deviation": trailing_deviation,
        "pairs": pairs
    }

    target_error, target_data = p3cwTarget.request(
        entity='bots',
        action='update',
        action_id=str(bot_id),
        payload=bot_payload
    )
    return target_error, target_data


def run():

    dest_error, destination_bots = p3cwDestination.request(
        entity='bots',
        action=''
        )

    target_error, target_bots = p3cwTarget.request(
        entity='bots',
        action=''
        )

    bot_names = ['15 Minutes BTC',
                   '15 Minutes ETH',
                   '15 Minutes USDT']

    for name in bot_names:
        dest_bot = get_bot(name, destination_bots)
        dest_id = dest_bot["id"]
        target_bot = get_bot(name, target_bots)
        if target_bot is not None:
            print("Bot id for " + name + " is: " + str(dest_id))
            print("Pairs for " + name)
            print(dest_bot["pairs"])
            error, data = update_bot_pairs(
                bot=target_bot,
                pairs=dest_bot["pairs"],
                strategy_list=dest_bot["strategy_list"],
                trailing_deviation=dest_bot["trailing_deviation"],
                trailing_enabled=dest_bot["trailing_enabled"])

            print(error, data)

            if (dest_bot["is_enabled"] is True):
                if (target_bot["is_enabled"] is False):
                    print("Enabling bot")
                    enable_bot(target_bot["id"])
            elif (target_bot["is_enabled"] is True):
                print("Disabling bot")
                disable_bot(target_bot["id"])
    return "Bots synced"


if __name__ == "__main__":
    run()