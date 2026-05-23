def get_next_client_id(data):
    max_id_client = max((x['id'] for x in data),default=0)

    return max_id_client + 1

def create_new_client(data, client_data):
    result = {
        "id": get_next_client_id(data),
        "order_id": client_data.order_id,
        "street": client_data.street,
        "house": client_data.house,
        "apartment": client_data.apartment,
        "phone": client_data.phone,
        "comment": client_data.comment,
    }

    data.append(result)
    return result

def find_client_by_id(data,client_id):
    for client in data:
        if client['id'] == client_id:
            return client

    return None