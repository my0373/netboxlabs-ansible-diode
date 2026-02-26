# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Convert Ansible task dicts into Diode SDK Entity objects."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from netboxlabs.diode.sdk.ingester import (
        ASN,
        ASNRange,
        Aggregate,
        Cable,
        CablePath,
        CableTermination,
        Circuit,
        CircuitGroup,
        CircuitGroupAssignment,
        CircuitTermination,
        CircuitType,
        Cluster,
        ClusterGroup,
        ClusterType,
        ConsolePort,
        ConsoleServerPort,
        Contact,
        ContactAssignment,
        ContactGroup,
        ContactRole,
        CustomField,
        CustomFieldChoiceSet,
        CustomLink,
        Device,
        DeviceBay,
        DeviceConfig,
        DeviceRole,
        DeviceType,
        Entity,
        FHRPGroup,
        FHRPGroupAssignment,
        FrontPort,
        IKEPolicy,
        IKEProposal,
        IPAddress,
        IPRange,
        IPSecPolicy,
        IPSecProfile,
        IPSecProposal,
        Interface,
        InventoryItem,
        InventoryItemRole,
        JournalEntry,
        L2VPN,
        L2VPNTermination,
        Location,
        MACAddress,
        Manufacturer,
        Module,
        ModuleBay,
        ModuleType,
        ModuleTypeProfile,
        Owner,
        OwnerGroup,
        Platform,
        PowerFeed,
        PowerOutlet,
        PowerPanel,
        PowerPort,
        Prefix,
        Provider,
        ProviderAccount,
        ProviderNetwork,
        RIR,
        Rack,
        RackReservation,
        RackRole,
        RackType,
        RearPort,
        Region,
        Role,
        RouteTarget,
        Service,
        Site,
        SiteGroup,
        Tag,
        Tenant,
        TenantGroup,
        Tunnel,
        TunnelGroup,
        TunnelTermination,
        VLAN,
        VLANGroup,
        VLANTranslationPolicy,
        VLANTranslationRule,
        VMInterface,
        VRF,
        VirtualChassis,
        VirtualCircuit,
        VirtualCircuitTermination,
        VirtualCircuitType,
        VirtualDeviceContext,
        VirtualDisk,
        VirtualMachine,
        WirelessLAN,
        WirelessLANGroup,
        WirelessLink,
    )

    HAS_DIODE_SDK = True
except ImportError:
    HAS_DIODE_SDK = False

# Maps user-facing type names to (Entity kwarg name, SDK class).
# The kwarg name is the parameter name on Entity.__new__().
ENTITY_TYPE_MAP = {
    "asn": ("asn", ASN if HAS_DIODE_SDK else None),
    "asn_range": ("asn_range", ASNRange if HAS_DIODE_SDK else None),
    "aggregate": ("aggregate", Aggregate if HAS_DIODE_SDK else None),
    "cable": ("cable", Cable if HAS_DIODE_SDK else None),
    "cable_path": ("cable_path", CablePath if HAS_DIODE_SDK else None),
    "cable_termination": ("cable_termination", CableTermination if HAS_DIODE_SDK else None),
    "circuit": ("circuit", Circuit if HAS_DIODE_SDK else None),
    "circuit_group": ("circuit_group", CircuitGroup if HAS_DIODE_SDK else None),
    "circuit_group_assignment": ("circuit_group_assignment", CircuitGroupAssignment if HAS_DIODE_SDK else None),
    "circuit_termination": ("circuit_termination", CircuitTermination if HAS_DIODE_SDK else None),
    "circuit_type": ("circuit_type", CircuitType if HAS_DIODE_SDK else None),
    "cluster": ("cluster", Cluster if HAS_DIODE_SDK else None),
    "cluster_group": ("cluster_group", ClusterGroup if HAS_DIODE_SDK else None),
    "cluster_type": ("cluster_type", ClusterType if HAS_DIODE_SDK else None),
    "console_port": ("console_port", ConsolePort if HAS_DIODE_SDK else None),
    "console_server_port": ("console_server_port", ConsoleServerPort if HAS_DIODE_SDK else None),
    "contact": ("contact", Contact if HAS_DIODE_SDK else None),
    "contact_assignment": ("contact_assignment", ContactAssignment if HAS_DIODE_SDK else None),
    "contact_group": ("contact_group", ContactGroup if HAS_DIODE_SDK else None),
    "contact_role": ("contact_role", ContactRole if HAS_DIODE_SDK else None),
    "custom_field": ("custom_field", CustomField if HAS_DIODE_SDK else None),
    "custom_field_choice_set": ("custom_field_choice_set", CustomFieldChoiceSet if HAS_DIODE_SDK else None),
    "custom_link": ("custom_link", CustomLink if HAS_DIODE_SDK else None),
    "device": ("device", Device if HAS_DIODE_SDK else None),
    "device_bay": ("device_bay", DeviceBay if HAS_DIODE_SDK else None),
    "device_config": ("device_config", DeviceConfig if HAS_DIODE_SDK else None),
    "device_role": ("device_role", DeviceRole if HAS_DIODE_SDK else None),
    "device_type": ("device_type", DeviceType if HAS_DIODE_SDK else None),
    "fhrp_group": ("fhrp_group", FHRPGroup if HAS_DIODE_SDK else None),
    "fhrp_group_assignment": ("fhrp_group_assignment", FHRPGroupAssignment if HAS_DIODE_SDK else None),
    "front_port": ("front_port", FrontPort if HAS_DIODE_SDK else None),
    "ike_policy": ("ike_policy", IKEPolicy if HAS_DIODE_SDK else None),
    "ike_proposal": ("ike_proposal", IKEProposal if HAS_DIODE_SDK else None),
    "interface": ("interface", Interface if HAS_DIODE_SDK else None),
    "inventory_item": ("inventory_item", InventoryItem if HAS_DIODE_SDK else None),
    "inventory_item_role": ("inventory_item_role", InventoryItemRole if HAS_DIODE_SDK else None),
    "ip_address": ("ip_address", IPAddress if HAS_DIODE_SDK else None),
    "ip_range": ("ip_range", IPRange if HAS_DIODE_SDK else None),
    "ip_sec_policy": ("ip_sec_policy", IPSecPolicy if HAS_DIODE_SDK else None),
    "ip_sec_profile": ("ip_sec_profile", IPSecProfile if HAS_DIODE_SDK else None),
    "ip_sec_proposal": ("ip_sec_proposal", IPSecProposal if HAS_DIODE_SDK else None),
    "journal_entry": ("journal_entry", JournalEntry if HAS_DIODE_SDK else None),
    "l2vpn": ("l2vpn", L2VPN if HAS_DIODE_SDK else None),
    "l2vpn_termination": ("l2vpn_termination", L2VPNTermination if HAS_DIODE_SDK else None),
    "location": ("location", Location if HAS_DIODE_SDK else None),
    "mac_address": ("mac_address", MACAddress if HAS_DIODE_SDK else None),
    "manufacturer": ("manufacturer", Manufacturer if HAS_DIODE_SDK else None),
    "module": ("module", Module if HAS_DIODE_SDK else None),
    "module_bay": ("module_bay", ModuleBay if HAS_DIODE_SDK else None),
    "module_type": ("module_type", ModuleType if HAS_DIODE_SDK else None),
    "module_type_profile": ("module_type_profile", ModuleTypeProfile if HAS_DIODE_SDK else None),
    "owner": ("owner", Owner if HAS_DIODE_SDK else None),
    "owner_group": ("owner_group", OwnerGroup if HAS_DIODE_SDK else None),
    "platform": ("platform", Platform if HAS_DIODE_SDK else None),
    "power_feed": ("power_feed", PowerFeed if HAS_DIODE_SDK else None),
    "power_outlet": ("power_outlet", PowerOutlet if HAS_DIODE_SDK else None),
    "power_panel": ("power_panel", PowerPanel if HAS_DIODE_SDK else None),
    "power_port": ("power_port", PowerPort if HAS_DIODE_SDK else None),
    "prefix": ("prefix", Prefix if HAS_DIODE_SDK else None),
    "provider": ("provider", Provider if HAS_DIODE_SDK else None),
    "provider_account": ("provider_account", ProviderAccount if HAS_DIODE_SDK else None),
    "provider_network": ("provider_network", ProviderNetwork if HAS_DIODE_SDK else None),
    "rack": ("rack", Rack if HAS_DIODE_SDK else None),
    "rack_reservation": ("rack_reservation", RackReservation if HAS_DIODE_SDK else None),
    "rack_role": ("rack_role", RackRole if HAS_DIODE_SDK else None),
    "rack_type": ("rack_type", RackType if HAS_DIODE_SDK else None),
    "rear_port": ("rear_port", RearPort if HAS_DIODE_SDK else None),
    "region": ("region", Region if HAS_DIODE_SDK else None),
    "rir": ("rir", RIR if HAS_DIODE_SDK else None),
    "role": ("role", Role if HAS_DIODE_SDK else None),
    "route_target": ("route_target", RouteTarget if HAS_DIODE_SDK else None),
    "service": ("service", Service if HAS_DIODE_SDK else None),
    "site": ("site", Site if HAS_DIODE_SDK else None),
    "site_group": ("site_group", SiteGroup if HAS_DIODE_SDK else None),
    "tag": ("tag", Tag if HAS_DIODE_SDK else None),
    "tenant": ("tenant", Tenant if HAS_DIODE_SDK else None),
    "tenant_group": ("tenant_group", TenantGroup if HAS_DIODE_SDK else None),
    "tunnel": ("tunnel", Tunnel if HAS_DIODE_SDK else None),
    "tunnel_group": ("tunnel_group", TunnelGroup if HAS_DIODE_SDK else None),
    "tunnel_termination": ("tunnel_termination", TunnelTermination if HAS_DIODE_SDK else None),
    "vlan": ("vlan", VLAN if HAS_DIODE_SDK else None),
    "vlan_group": ("vlan_group", VLANGroup if HAS_DIODE_SDK else None),
    "vlan_translation_policy": ("vlan_translation_policy", VLANTranslationPolicy if HAS_DIODE_SDK else None),
    "vlan_translation_rule": ("vlan_translation_rule", VLANTranslationRule if HAS_DIODE_SDK else None),
    "vm_interface": ("vm_interface", VMInterface if HAS_DIODE_SDK else None),
    "vrf": ("vrf", VRF if HAS_DIODE_SDK else None),
    "virtual_chassis": ("virtual_chassis", VirtualChassis if HAS_DIODE_SDK else None),
    "virtual_circuit": ("virtual_circuit", VirtualCircuit if HAS_DIODE_SDK else None),
    "virtual_circuit_termination": ("virtual_circuit_termination", VirtualCircuitTermination if HAS_DIODE_SDK else None),
    "virtual_circuit_type": ("virtual_circuit_type", VirtualCircuitType if HAS_DIODE_SDK else None),
    "virtual_device_context": ("virtual_device_context", VirtualDeviceContext if HAS_DIODE_SDK else None),
    "virtual_disk": ("virtual_disk", VirtualDisk if HAS_DIODE_SDK else None),
    "virtual_machine": ("virtual_machine", VirtualMachine if HAS_DIODE_SDK else None),
    "wireless_lan": ("wireless_lan", WirelessLAN if HAS_DIODE_SDK else None),
    "wireless_lan_group": ("wireless_lan_group", WirelessLANGroup if HAS_DIODE_SDK else None),
    "wireless_link": ("wireless_link", WirelessLink if HAS_DIODE_SDK else None),
}

SUPPORTED_ENTITY_TYPES = sorted(ENTITY_TYPE_MAP.keys())


def build_entity(entity_dict):
    """Convert a single Ansible dict to an SDK Entity protobuf.

    Args:
        entity_dict: A dict with ``type`` (str) and ``data`` (dict) keys.

    Returns:
        A protobuf Entity message.

    Raises:
        ValueError: If the entity type is unknown or the SDK is missing.
    """
    if not HAS_DIODE_SDK:
        raise ImportError(
            "netboxlabs-diode-sdk is required but not installed. "
            "Install it with: pip install netboxlabs-diode-sdk"
        )

    entity_type = entity_dict.get("type")
    if not entity_type:
        raise ValueError("Each entity must have a 'type' field")

    if entity_type not in ENTITY_TYPE_MAP:
        raise ValueError(
            "Unknown entity type '{0}'. Supported types: {1}".format(
                entity_type, ", ".join(SUPPORTED_ENTITY_TYPES)
            )
        )

    entity_kwarg, entity_cls = ENTITY_TYPE_MAP[entity_type]
    data = entity_dict.get("data", {})

    if isinstance(data, str):
        obj = entity_cls(data)
    else:
        obj = entity_cls(**data)

    return Entity(**{entity_kwarg: obj})


def build_entities(entity_dicts):
    """Convert a list of Ansible dicts to SDK Entity protobufs.

    Args:
        entity_dicts: List of dicts, each with ``type`` and ``data`` keys.

    Returns:
        List of protobuf Entity messages.
    """
    return [build_entity(item) for item in entity_dicts]
