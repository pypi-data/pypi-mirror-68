from open_vsdcli.vsd_common import *


@vsdcli.command(name='vm-list')
@click.option('--egressacltemplate-id', metavar='<id>')
@click.option('--enterprise-id', metavar='<id>')
@click.option('--ingressacltemplate-id', metavar='<id>')
@click.option('--vrs-id', metavar='<id>')
@click.option('--vport-id', metavar='<id>')
@click.option('--zone-id', metavar='<id>')
@click.option('--l2domain-id', metavar='<id>')
@click.option('--app-id', metavar='<id>')
@click.option('--domain-id', metavar='<id>')
@click.option('--user-id', metavar='<id>')
@click.option('--subnet-id', metavar='<id>')
@click.option('--filter', metavar='<filter>',
              help='Filter for UUID, name, status, reasonType, hypervisorIP, '
                   'lastUpdatedDate, creationDate, externalID')
@click.pass_context
def vm_list(ctx, filter, **ids):
    """List all VMs"""
    id_type, id = check_id(**ids)
    request = "vms"
    if id:
        if id_type:
            request = "%ss/%s/vms" % (id_type, id)
    if not filter:
        result = ctx.obj['nc'].get(request)
    else:
        result = ctx.obj['nc'].get(request, filter=filter)
    table = PrettyTable(["ID",
                         "Vm UUID",
                         "Name",
                         "Status",
                         "Hypervisor IP",
                         "Reason Type"])
    for line in result:
        table.add_row([line['ID'],
                       line['UUID'],
                       line['name'],
                       line['status'],
                       line['hypervisorIP'],
                       line['reasonType']])
    print(table)


@vsdcli.command(name='vm-show')
@click.argument('vm-id', metavar='<vm ID>', required=True)
@click.pass_context
def vm_show(ctx, vm_id):
    """Show information for a given VM ID"""
    result = ctx.obj['nc'].get("vms/%s" % vm_id)[0]
    print_object(result, exclude=['interfaces', 'resyncInfo'],
                 only=ctx.obj['show_only'])


@vsdcli.command(name='vm-delete')
@click.argument('vm-id', metavar='<vm ID>', required=True)
@click.pass_context
def vm_delete(ctx, vm_id):
    """Delete VM for a given ID"""
    result = ctx.obj['nc'].delete("vms/%s" % vm_id)


@vsdcli.command(name='vm-create',
                help='Create a new VM. One interface is needed')
@click.argument('name', metavar='<name>', required=True)
@click.option('--uuid', metavar='<uuid>', required=True,
              help='UUID of the associated virtual machine')
@click.option('--vport-id', metavar='<ID>', required=True,
              help='ID of the vport that the interface is attached to')
@click.option('--mac', metavar='<mac address>', required=True,
              help='Mac address in format aa:bb:cc:dd:ee:ff')
@click.option('--ipaddress', metavar='<IP Address>',
              help='Mac address in format a.b.c.d. If no IP is given, '
              'VSD will assign one if needed')
@click.pass_context
def vm_create(ctx, name, uuid, vport_id, mac, ipaddress):
    """Create VM for a given ID"""
    params = {'name': name,
              'UUID': uuid,
              'interfaces': [{'VPortID': vport_id,
                              'MAC': mac,
                              'IPAddress': ipaddress}]}
    result = ctx.obj['nc'].post("vms", params)[0]
    print_object(result, exclude=['interfaces', 'resyncInfo'],
                 only=ctx.obj['show_only'])


@vsdcli.command(name='vm-update')
@click.argument('vm-id', metavar='<ID>', required=True)
@click.option('--key-value', metavar='<key:value>', multiple=True)
@click.pass_context
def vm_update(ctx, vm_id, key_value):
    """Update key/value for a given vm"""
    params = {}
    for kv in key_value:
        key, value = kv.split(':', 1)
        params[key] = value
    ctx.obj['nc'].put("vms/%s" % vm_id, params)
    result = ctx.obj['nc'].get("vms/%s" % vm_id)[0]
    print_object(result, exclude=['interfaces', 'resyncInfo'],
                 only=ctx.obj['show_only'])


@vsdcli.command(name='vminterface-list')
@click.option('--subnet-id', metavar='<id>')
@click.option('--zone-id', metavar='<id>')
@click.option('--vm-id', metavar='<id>')
@click.option('--vport-id', metavar='<id>')
@click.option('--domain-id', metavar='<id>')
@click.option('--filter', metavar='<filter>',
              help='Filter for name, IPAddress, MAC, name, IPAddress, name, '
                   'lastUpdatedDate, creationDate, externalID')
@click.pass_context
def vminterfaces_list(ctx, filter, **ids):
    """List VM interfaces"""
    id_type, id = check_id(**ids)
    if (id and not id_type) or (not id and id_type):
        raise Exception("Set id and id-type")
    if id_type:
        request = "%ss/%s/vminterfaces" % (id_type, id)
    else:
        request = "vminterfaces"
    if not filter:
        result = ctx.obj['nc'].get(request)
    else:
        result = ctx.obj['nc'].get(request, filter=filter)
    table = PrettyTable(["ID",
                         "VM UUID",
                         "IP Address",
                         "MAC",
                         "Vport id"])
    for line in result:
        if line['IPAddress']:
            cidr = line['IPAddress'] + '/' + netmask_to_length(line['netmask'])
        else:
            cidr = None
        table.add_row([line['ID'],
                       line['VMUUID'],
                       cidr,
                       line['MAC'],
                       line['VPortID']])
    print(table)


@vsdcli.command(name='vminterface-show')
@click.argument('vminterface-id', metavar='<vminterface ID>', required=True)
@click.pass_context
def vminterface_show(ctx, vminterface_id):
    """Show information for a given VM interface ID"""
    result = ctx.obj['nc'].get("vminterfaces/%s" % vminterface_id)[0]
    print_object(result, only=ctx.obj['show_only'])


@vsdcli.command(name='vminterface-create',
                help='Add an interface to a given VM')
@click.option('--name', metavar='<Interface name>')
@click.option('--vm-id', metavar='<vm id>', required=True,
              help='VM ID (it\'s not the UUID, it\'s the VSD ID)')
@click.option('--vport-id', metavar='<vport ID>',
              help='ID of the vport that the interface is attached to')
@click.option('--network-id', metavar='<network ID>',
              help='ID of the network that the interface is attached to. '
                   'Can be either l2domain or subnet within domain')
@click.option('--mac', metavar='<mac address>', required=True,
              help='Mac address in format aa:bb:cc:dd:ee:ff')
@click.option('--ipaddress', metavar='<IP Address>',
              help='Mac address in format a.b.c.d. If no IP is given, '
              'VSD will assign one if needed')
@click.pass_context
def vminterface_create(ctx, name, vm_id, vport_id, network_id, mac, ipaddress):
    """Add interface to a given VM"""
    params = {'name': name,
              'VPortID': vport_id,
              'attachedNetworkID': network_id,
              'MAC': mac,
              'IPAddress': ipaddress}
    result = ctx.obj['nc'].post("vms/%s/vminterfaces" % vm_id, params)[0]
    print_object(result, only=ctx.obj['show_only'])


@vsdcli.command(name='vminterface-update')
@click.argument('vminterface-id', metavar='<vminterface ID>', required=True)
@click.option('--key-value', metavar='<key:value>', multiple=True)
@click.pass_context
def vminterface_update(ctx, vminterface_id, key_value):
    """Update key/value for a given vminterface"""
    params = {}
    for kv in key_value:
        key, value = kv.split(':', 1)
        params[key] = value
    ctx.obj['nc'].put("vminterfaces/%s" % vminterface_id, params)
    result = ctx.obj['nc'].get("vminterfaces/%s" % vminterface_id)[0]
    print_object(result, only=ctx.obj['show_only'])
