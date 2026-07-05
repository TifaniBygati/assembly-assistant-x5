def group_clients_with_addresses(rows):
    client_by_id = {}
    for row in rows:
        client_id = row['client_id']
        if client_id not in client_by_id:
            client_by_id[client_id] = {
                'client_id': client_id,
                'name': row.get('name', None),
                'phone': row['phone'],
                'addresses':[]
            }
        if row['address_id'] is not None:
            client_by_id[client_id]['addresses'].append(
                {
                    'address_id': row['address_id'],
                    'street': row['street'],
                    'house': row['house'],
                    'floor': row.get('floor', None),
                    'entrance': row.get('entrance', None),
                    'apartment': row.get('apartment', None),
                    'comment': row.get('comment', None),
                }
            )

    return list(client_by_id.values())
