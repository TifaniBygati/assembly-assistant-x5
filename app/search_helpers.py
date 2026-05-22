def find_clients_by_address(clients, street=None, house=None, apartment=None):
    result_to_find = []

    for client in clients:

        if street is not None and client['street'] != street:
            continue

        if house is not None and client['house'] != house:
            continue

        if apartment is not None and client['apartment'] != apartment:
            continue

        result_to_find.append(client)

    return result_to_find
