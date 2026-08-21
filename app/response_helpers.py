def group_clients_with_addresses(rows):
    client_by_id = {}
    for row in rows:
        client_id = row['client_id']
        if client_id not in client_by_id:
            client_by_id[client_id] = {
                'client_id': client_id,
                'name': row.get('name', None),
                'phone': row['phone'],
                'addresses': []
            }
        if row['address_id'] is not None:
            client_by_id[client_id]['addresses'].append({
                'address_id': row['address_id'],
                'street': row['street'],
                'house': row['house'],
                'floor': row.get('floor', None),
                'entrance': row.get('entrance', None),
                'apartment': row.get('apartment', None),
                'comment': row.get('comment', None),
            })

    return list(client_by_id.values())

def group_clients_with_obj_orm(obj):
    result = []

    for client in obj:

        addresses = []
        for address in client.addresses:
            addresses.append({
                'address_id': address.id,
                'client_id': address.client_id,
                'street': address.street,
                'house': address.house,
                'floor': address.floor,
                'entrance': address.entrance,
                'apartment': address.apartment,
                'comment': address.comment
            })

        client_data = {
            'client_id': client.id,
            'name': client.name,
            'phone': client.phone,
            'addresses': addresses,
        }

        result.append(client_data)

    return result

def group_one_with_obj_orm(obj):

    addresses = []

    for address in obj.addresses:
        addresses.append({
            'address_id': address.id,
            'client_id': address.client_id,
            'street': address.street,
            'house': address.house,
            'floor': address.floor,
            'entrance': address.entrance,
            'apartment': address.apartment,
            'comment': address.comment
        })

    result = {
        'client_id': obj.id,
        'name': obj.name,
        'phone': obj.phone,
        'addresses': addresses,
    }

    return result
