# Copyright 2015 Maxime Terras <maxime.terras@numergy.com>
# Copyright 2015 Pierre Padrixe <pierre.padrixe@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import sys
from flask import Flask, request, make_response
import json
from time import time as epoch

app = Flask(__name__)

database = {}

base_url="/nuage/api/v3_2/"

def get_object_id(obj_name, key, value):
    if obj_name not in database:
        return {}
    for object in database[obj_name]:
        if key in object:
            if object[key] == value:
                return object
    return {}


def filter_objets(obj_name, filter):
    ret = []
    if obj_name not in database:
        return ret
    if filter is None:
        return database[obj_name]
    for object in database[obj_name]:
        for k in object.keys():
            if filter in object[k]:
                ret.append(object)
                continue
    return ret


@app.route(base_url + "reset", methods=['GET'])
def reset():
    database.clear()
    database.update(
        {
            'enterprises':  [
                {
                    'ID': '92a76e6f-2ac4-43f2-8c1f-a052c5f4d90e',
                    'name': 'nulab-1',
                    'description': 'None',
                    'parentType': 'null',
                    'enterpriseProfileID': 'd63701e0-9246-4c7a-9f43-0c66d0fe45e3'
                },
                {
                    'ID': '5b2cc2f3-2b86-42ec-892d-edde741b2fd4',
                    'name': 'nulab-2',
                    'description': 'None',
                    'parentType': 'null',
                    'enterpriseProfileID': '3e05994c-0f9b-41d0-84d5-ec083ee89567'
                }
            ]
        }
    )
    database.update(
        {
            'messages':  [
                {
                    'name': 'already exists',
                    'message':  {
                        'errors':  [
                            {
                                'property': 'name',
                                'descriptions':  [
                                    {
                                        'title': 'Duplicate object',
                                        'description': 'Object already exists.'
                                    }
                                ]
                            }
                        ],
                        'internalErrorCode': 2002
                    }
                },
                {
                    'name': 'not found',
                    'message':  {
                        'errors':  [
                            {
                                'property': '',
                                'descriptions':  [
                                    {
                                        'title': 'Object not found',
                                        'description': 'Cannot find object with ID'
                                    }
                                ]
                            }
                        ],
                        'description': 'Cannot find object with ID'
                    }
                },
                {
                    'name': 'already in use',
                    'message':  {
                        'errors':  [
                            {
                                'property': '',
                                'descriptions':  [
                                    {
                                        'title': 'Object already in use',
                                        'description': 'Gateway x.x.x.x is already part of another Redundancy group'
                                    }
                                ]
                            }
                        ],
                        'description': 'Gateway x.x.x.x is already part of another Redundancy group'
                    }
                },
            ]
        }
    )
    return make_response('{}', '200')


@app.route(base_url + "me", methods=['GET'])
def me_show():
    xrest = [
        "XREST dGVzdDp0ZXN0",         # test/test
        "XREST ZGF0ZTp0ZXN0",         # date/test
        "XREST bnVsbGRhdGU6dGVzdA=="  # nulldate/test
    ]
    auth = request.headers.get('Authorization')
    if not auth in xrest:
        return make_response("<html><head><title>JBoss - Error report</head></html>", '401')
    reply = [{
        'firstName': 'csproot',
        'enterpriseName': 'CSP',
        'APIKey': '02a99c64-a09a-46d7',
        'APIKeyExpiry': (int(epoch()) + 100) * 1000,
        'enterpriseID': 'fc3a351e-87dc-46a4-bcf5-8c4bb204bd46',
    }]
    if auth == "XREST ZGF0ZTp0ZXN0":
        reply[0]['DateDecodeDate'] = '1469448000000'
        reply[0]['DateNotDecode'] = '1469448000000'
        reply[0]['ExpiryDecodeExpiry'] = '1469448000000'
        reply[0]['DateNoneDate'] = None

    if auth == "XREST bnVsbGRhdGU6dGVzdA==":
        reply[0]['DateDecodeDate'] = 'null'

    return json.dumps(reply)


@app.route(base_url + "enterprises/bad-object", methods=['GET'])
def bag_object():
    msg = ("<html><head><title>JBoss Web/7.0.17.Final - Error report</title>"
           " </head><body><h1>HTTP Status 400 - </h1><HR size=\"1\" noshade=\"noshade\">"
           "<p><b>type</b> Status report</p><p><b>message</b> <u></u></p><p><b>"
           "description</b> <u>The request sent by the client was syntactically incorrect ()."
           "</u></p><HR size=\"1\" noshade=\"noshade\"><h3>JBoss Web/7.0.17.Final</h3>"
           "</body></html>")
    make_response(msg, '405')


@app.route(base_url + "<obj_name>", methods=['GET'])
def object_list(obj_name):
    filter = request.headers.get('X-Nuage-Filter')
    return json.dumps(filter_objets(obj_name, filter))


@app.route(base_url + "<obj_name>/<obj_id>", methods=['GET'])
def object_show(obj_name, obj_id):
    data_src = get_object_id(obj_name, 'ID', obj_id)
    if data_src == {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'not found')['message']), '404')
    return json.dumps([get_object_id(obj_name, 'ID', obj_id)])


@app.route(base_url + "<parent_name>/<parent_id>/<obj_name>", methods=['GET'])
def get_object_list_with_parent(parent_name, parent_id, obj_name):
    # Check parent exist but don't check parent own objects
    data_src = get_object_id(parent_name, 'ID', parent_id)
    if data_src == {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'not found')['message']), '404')
    filter = request.headers.get('X-Nuage-Filter')
    return json.dumps(filter_objets(obj_name, filter))


@app.route(base_url + "groups/<obj_id>/users", methods=['PUT'])
def update_group_user_list(obj_id):
    # ToDo: Currently the server_mock doesn't do anything while we update
    #       the list of users in the group. If you wan to implement this
    #       mock method, you should at first fix the user-list mock: it
    #       currently doesn't list user by group-id (mock of "vsd user-list
    #       --group-id xD42x" currently doesn't work)
    #
    #       What we planned to do for a short term solution:
    #       don't use mock server to test it and just add more checks on
    #       the type of the parameters in the tests.
    return '{}'


def increment_id(id):
    """Increment each byte by one"""
    """111111 becomes 22222 and so on"""
    c = ord(id[0]) + 1
    new = chr(c) * 8 + '-' + chr(c) * 4 + '-' + chr(c) * 4 + '-' + chr(c) * 12
    return new


@app.route(base_url + "gateways", methods=['POST'])
def gateway_create():
    data_update = json.loads(request.data)
    if 'gateways' not in database:
        database.update({'gateways': []})
    data_src = get_object_id('gateways', 'systemID', data_update['systemID'])
    if data_src != {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'already exists')['message']), '409')

    id = '0'
    for object in database['gateways']:
        if (object['ID'][0] > id):
            id = object['ID'][0]

    id = increment_id(id)
    new = {'ID': id,
           'systemID': '9.9.9.9',
           'name': 'gateway-unknown',
           'description': 'None',
           'pending': 'False',
           'redundancyGroupID': 'None',
           'personality': 'VRSG'}
    new.update(data_update)
    database['gateways'].append(new)

    return json.dumps([get_object_id('gateways', 'ID', id)])


@app.route(base_url + "redundancygroups", methods=['POST'])
def gatewayredundantgroup_create():
    data_update = json.loads(request.data)
    if 'redundancygroups' not in database:
        database.update({'redundancygroups': []})

    id = get_object_id('redundancygroups', 'gatewayPeer1ID',
                       data_update['gatewayPeer1ID'])
    if id != {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'already in use')['message']), '409')

    id = get_object_id('redundancygroups', 'gatewayPeer2ID',
                       data_update['gatewayPeer2ID'])
    if id != {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'already in use')['message']), '409')

    id = '0'
    for object in database['gateways']:
        if (object['ID'][0] > id):
            id = object['ID'][0]

    id = increment_id(id)
    new = {'ID': id,
           'name': 'gw-group-unknown',
           'description': 'None',
           'entityScope': 'ENTERPRISE',
           'enterpriseID': '76046673-d0ea-4a67-b6af-2829952f0812',
           'gatewayPeer1ID': '11111111-1111-1111-111111111111',
           'gatewayPeer2ID': '22222222-2222-2222-222222222222',
           'gatewayPeer1Name': 'gateway-1',
           'gatewayPeer2Name': 'gateway-2',
           'redundantGatewayStatus': 'SUCCESS',
           'personality': 'VRSG'}

    new.update(data_update)
    database['redundancygroups'].append(new)
    return json.dumps([get_object_id('redundancygroups', 'ID', id)])


@app.route(base_url + "enterprises/<enterprise_id>/redundancygroups", methods=['POST'])
def gatewayredundantgroup_create_with_enterprise_id(enterprise_id):
    data_update = json.loads(request.data)
    if 'redundancygroups' not in database:
        database.update({'redundancygroups': []})

    id = get_object_id('redundancygroups', 'gatewayPeer1ID',
                       data_update['gatewayPeer1ID'])
    if id != {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'already in use')['message']), '409')

    id = get_object_id('redundancygroups', 'gatewayPeer2ID',
                       data_update['gatewayPeer2ID'])
    if id != {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'already in use')['message']), '409')

    id = '0'
    for object in database['gateways']:
        if (object['ID'][0] > id):
            id = object['ID'][0]

    id = increment_id(id)
    new = {'ID': id,
           'name': 'gw-group-unknown',
           'description': 'None',
           'entityScope': 'ENTERPRISE',
           'enterpriseID': enterprise_id,
           'gatewayPeer1ID': '11111111-1111-1111-111111111111',
           'gatewayPeer2ID': '22222222-2222-2222-222222222222',
           'gatewayPeer1Name': 'gateway-1',
           'gatewayPeer2Name': 'gateway-2',
           'redundantGatewayStatus': 'SUCCESS',
           'personality': 'VRSG'}

    new.update(data_update)
    database['redundancygroups'].append(new)
    return json.dumps([get_object_id('redundancygroups', 'ID', id)])


@app.route(base_url + "licenses", methods=['POST'])
def license_create():
    data_update = json.loads(request.data)
    if 'licenses' not in database:
        database.update({'licenses': []})
    data_src = get_object_id('licenses', 'license', data_update['license'])
    if data_src != {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'already exists')['message']), '409')
    new = {'license': data_update['license'],
           'ID': '255d9673-7281-43c4-be57-fdec677f6e07',
           'isClusterLicense': 'True',
           'description': 'None',
           'company': 'Compagny-1',
           'allowedNICsCount': '100',
           'allowedVMsCount': '100',
           'productVersion': '2',
           'majorRelease': '6',
           'expirationDate': 1500000000000}
    database['licenses'].append(new)
    return json.dumps([get_object_id('licenses', 'ID', '255d9673-7281-43c4-be57-fdec677f6e07')])


@app.route(base_url + "<obj_name>", methods=['POST'])
def object_create(obj_name):
    if obj_name == 'vms':
        if 'vms' not in database:
            database.update({'vms': []})
    data_update = json.loads(request.data)
    data_update.update({
        'ID': '255d9673-7281-43c4-be57-fdec677f6e07',
        'description': 'None'
    })
    data_src = get_object_id(obj_name, 'name', data_update['name'])
    if data_src != {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'already exists')['message']), '409')
    database[obj_name].append(data_update)
    return json.dumps([get_object_id(obj_name, 'ID', '255d9673-7281-43c4-be57-fdec677f6e07')])


@app.route(base_url + "<parent_name>/<parent_id>/<obj_name>", methods=['POST'])
def object_create_with_parent(parent_name, parent_id, obj_name):
    data_update = json.loads(request.data)
    # Check parent exist but don't check parent own objects
    data_src = get_object_id(parent_name, 'ID', parent_id)
    if data_src == {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'not found')['message']), '404')
    if 'name' in data_update.keys():
        data_src = get_object_id(obj_name, 'name', data_update['name'])
        if data_src != {}:
            return make_response(json.dumps(
                get_object_id('messages', 'name', 'already exists')['message']), '409')
    uuid = '255d9673-7281-43c4-be57-fdec677f6e07'
    with_random_uuid = ['dhcpoptions']
    if obj_name in with_random_uuid:
        import uuid
        uuid = str(uuid.uuid4())
    if obj_name == 'vminterfaces':
        data_update.update({'MAC':None})
    data_update.update({
        'ID': uuid,
        'description': 'None'
    })
    if obj_name not in database:
        database.update({obj_name: []})
    database[obj_name].append(data_update)
    return json.dumps([get_object_id(obj_name, 'ID', uuid)])


@app.route(base_url + "<obj_name>/<obj_id>", methods=['PUT'])
def object_update(obj_name, obj_id):
    data_update = json.loads(request.data)
    data_src = get_object_id(obj_name, 'ID', obj_id)
    data_src.update(data_update)
    return '{}'


@app.route(base_url + "<obj_name>/<obj_id>", methods=['DELETE'])
def object_delete(obj_name, obj_id):
    data_src = get_object_id(obj_name, 'ID', obj_id)
    if data_src == {}:
        return make_response(json.dumps(
            get_object_id('messages', 'name', 'not found')['message']), '404')
    database[obj_name].remove(data_src)
    return '{}'


if __name__ == "__main__":
    if '--debug' in sys.argv:
        app.debug = True
    app.run(host='127.0.0.1')
