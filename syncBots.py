from py3cw.request import Py3CW

p3cwDestination = Py3CW(
    key='e4a561f20fb44012a28f6a74aa32844abf2328cef80d4a678a5c9c40a60b930e',
    secret='9a553d0b69094a1cbc59f779b4f50030ae90e27212e2e25667bf06c54412ee0a89fb025cbd600ebcef8c4b2ff0da08b71386aefadc8dd54dee098bd8994ef4f42de61bc2884d7a1f8c29720b3c54b619ac7188ff88172458355347e58547ecf70f45b8da')

p3cwTarget = Py3CW(
    key='e9e2e1465c964a5b995bc4b8d03dd03080ffa02c47094ca6a25cf013246ea222',
    secret='6f6b57ea96ec7a14aa03b2191ca580d7762ef228331c07c9572b44ddeb52f1999c15fa65d558b7a898a8b72cef2515e49dd86fb6985d35e163c7b4d0b788da39777d1607444e46d547a1733a8f57703097479d0d871e602ff597f853c6783f7e50f7c173')


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


def get_bot_pairs_by_name(name, bots):
    for bot in bots:
        if (bot["name"] == name):
            return bot["pairs"]
    return None

def disable_bot(bot_id):
    target_error, target_data = p3cwTarget.request(
            entity='bots',
            action='disable',
            action_id=str(bot_id)
        )
    return target_error,target_data

def enable_bot(bot_id):
    target_error, target_data = p3cwTarget.request(
            entity='bots',
            action='enable',
            action_id=str(bot_id)
        )
    return target_error,target_data

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