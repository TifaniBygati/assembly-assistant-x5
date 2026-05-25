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

def update_client(data, client_id,new_client_data):
    client = find_client_by_id(data,client_id)

    if client is None:
        return None

    if new_client_data.order_id is not None:
        client['order_id'] = new_client_data.order_id

    if new_client_data.street is not None:
        client['street'] = new_client_data.street

    if new_client_data.house is not None:
        client['house'] = new_client_data.house

    if new_client_data.apartment is not None:
        client['apartment'] = new_client_data.apartment

    if new_client_data.phone is not None:
        client['phone'] = new_client_data.phone

    if new_client_data.comment is not None:
        client['comment'] = new_client_data.comment

    return client

def delete_client(data, client_id):
    client = find_client_by_id(data,client_id)

    if client is None:
        return None

    data.remove(client)
    return client

def replace_client(data, client_id,client_data):

    client = find_client_by_id(data,client_id)

    if client is None:
        return None

    new_data = client_data.model_dump()

    client.update(new_data)

    return client

