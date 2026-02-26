# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Unit tests for entity_builder module_utils."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_sdk(monkeypatch):
    """Patch the SDK imports so entity_builder can be tested without the real SDK."""
    mock_ingester = MagicMock()

    mock_classes = {}
    class_names = [
        "ASN", "ASNRange", "Aggregate", "Cable", "CablePath", "CableTermination",
        "Circuit", "CircuitGroup", "CircuitGroupAssignment", "CircuitTermination",
        "CircuitType", "Cluster", "ClusterGroup", "ClusterType", "ConsolePort",
        "ConsoleServerPort", "Contact", "ContactAssignment", "ContactGroup",
        "ContactRole", "CustomField", "CustomFieldChoiceSet", "CustomLink",
        "Device", "DeviceBay", "DeviceConfig", "DeviceRole", "DeviceType",
        "Entity", "FHRPGroup", "FHRPGroupAssignment", "FrontPort",
        "IKEPolicy", "IKEProposal", "IPAddress", "IPRange", "IPSecPolicy",
        "IPSecProfile", "IPSecProposal", "Interface", "InventoryItem",
        "InventoryItemRole", "JournalEntry", "L2VPN", "L2VPNTermination",
        "Location", "MACAddress", "Manufacturer", "Module", "ModuleBay",
        "ModuleType", "ModuleTypeProfile", "Owner", "OwnerGroup", "Platform",
        "PowerFeed", "PowerOutlet", "PowerPanel", "PowerPort", "Prefix",
        "Provider", "ProviderAccount", "ProviderNetwork", "RIR", "Rack",
        "RackReservation", "RackRole", "RackType", "RearPort", "Region",
        "Role", "RouteTarget", "Service", "Site", "SiteGroup", "Tag",
        "Tenant", "TenantGroup", "Tunnel", "TunnelGroup", "TunnelTermination",
        "VLAN", "VLANGroup", "VLANTranslationPolicy", "VLANTranslationRule",
        "VMInterface", "VRF", "VirtualChassis", "VirtualCircuit",
        "VirtualCircuitTermination", "VirtualCircuitType",
        "VirtualDeviceContext", "VirtualDisk", "VirtualMachine",
        "WirelessLAN", "WirelessLANGroup", "WirelessLink",
    ]
    for name in class_names:
        mock_cls = MagicMock()
        mock_cls.__name__ = name
        mock_cls.return_value = MagicMock(name="{0}_instance".format(name))
        mock_classes[name] = mock_cls
        setattr(mock_ingester, name, mock_cls)

    import sys
    sys.modules["netboxlabs"] = MagicMock()
    sys.modules["netboxlabs.diode"] = MagicMock()
    sys.modules["netboxlabs.diode.sdk"] = MagicMock()
    sys.modules["netboxlabs.diode.sdk.ingester"] = mock_ingester

    for name, cls in mock_classes.items():
        monkeypatch.setattr(
            "netboxlabs.diode.sdk.ingester.{0}".format(name), cls
        )

    if "ansible_collections.my0373.diode.plugins.module_utils.entity_builder" in sys.modules:
        del sys.modules["ansible_collections.my0373.diode.plugins.module_utils.entity_builder"]

    from ansible_collections.my0373.diode.plugins.module_utils import entity_builder
    entity_builder.HAS_DIODE_SDK = True

    for type_name, (kwarg, _) in list(entity_builder.ENTITY_TYPE_MAP.items()):
        cls_name_map = {
            "asn": "ASN", "asn_range": "ASNRange", "aggregate": "Aggregate",
            "cable": "Cable", "cable_path": "CablePath",
            "cable_termination": "CableTermination", "circuit": "Circuit",
            "circuit_group": "CircuitGroup",
            "circuit_group_assignment": "CircuitGroupAssignment",
            "circuit_termination": "CircuitTermination",
            "circuit_type": "CircuitType", "cluster": "Cluster",
            "cluster_group": "ClusterGroup", "cluster_type": "ClusterType",
            "console_port": "ConsolePort",
            "console_server_port": "ConsoleServerPort",
            "contact": "Contact", "contact_assignment": "ContactAssignment",
            "contact_group": "ContactGroup", "contact_role": "ContactRole",
            "custom_field": "CustomField",
            "custom_field_choice_set": "CustomFieldChoiceSet",
            "custom_link": "CustomLink",
            "device": "Device", "device_bay": "DeviceBay",
            "device_config": "DeviceConfig", "device_role": "DeviceRole",
            "device_type": "DeviceType",
            "fhrp_group": "FHRPGroup",
            "fhrp_group_assignment": "FHRPGroupAssignment",
            "front_port": "FrontPort", "ike_policy": "IKEPolicy",
            "ike_proposal": "IKEProposal", "interface": "Interface",
            "inventory_item": "InventoryItem",
            "inventory_item_role": "InventoryItemRole",
            "ip_address": "IPAddress", "ip_range": "IPRange",
            "ip_sec_policy": "IPSecPolicy", "ip_sec_profile": "IPSecProfile",
            "ip_sec_proposal": "IPSecProposal",
            "journal_entry": "JournalEntry",
            "l2vpn": "L2VPN", "l2vpn_termination": "L2VPNTermination",
            "location": "Location", "mac_address": "MACAddress",
            "manufacturer": "Manufacturer", "module": "Module",
            "module_bay": "ModuleBay", "module_type": "ModuleType",
            "module_type_profile": "ModuleTypeProfile",
            "owner": "Owner", "owner_group": "OwnerGroup",
            "platform": "Platform", "power_feed": "PowerFeed",
            "power_outlet": "PowerOutlet", "power_panel": "PowerPanel",
            "power_port": "PowerPort", "prefix": "Prefix",
            "provider": "Provider", "provider_account": "ProviderAccount",
            "provider_network": "ProviderNetwork",
            "rack": "Rack", "rack_reservation": "RackReservation",
            "rack_role": "RackRole", "rack_type": "RackType",
            "rear_port": "RearPort", "region": "Region",
            "rir": "RIR", "role": "Role",
            "route_target": "RouteTarget", "service": "Service",
            "site": "Site", "site_group": "SiteGroup",
            "tag": "Tag", "tenant": "Tenant",
            "tenant_group": "TenantGroup", "tunnel": "Tunnel",
            "tunnel_group": "TunnelGroup",
            "tunnel_termination": "TunnelTermination",
            "vlan": "VLAN", "vlan_group": "VLANGroup",
            "vlan_translation_policy": "VLANTranslationPolicy",
            "vlan_translation_rule": "VLANTranslationRule",
            "vm_interface": "VMInterface", "vrf": "VRF",
            "virtual_chassis": "VirtualChassis",
            "virtual_circuit": "VirtualCircuit",
            "virtual_circuit_termination": "VirtualCircuitTermination",
            "virtual_circuit_type": "VirtualCircuitType",
            "virtual_device_context": "VirtualDeviceContext",
            "virtual_disk": "VirtualDisk",
            "virtual_machine": "VirtualMachine",
            "wireless_lan": "WirelessLAN",
            "wireless_lan_group": "WirelessLANGroup",
            "wireless_link": "WirelessLink",
        }
        sdk_cls_name = cls_name_map.get(type_name)
        if sdk_cls_name and sdk_cls_name in mock_classes:
            entity_builder.ENTITY_TYPE_MAP[type_name] = (kwarg, mock_classes[sdk_cls_name])

    return mock_classes, entity_builder


class TestBuildEntity:
    def test_build_device_entity(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        result = entity_builder.build_entity({
            "type": "device",
            "data": {"name": "switch-01", "status": "active"},
        })
        mock_classes["Device"].assert_called_once_with(name="switch-01", status="active")
        mock_classes["Entity"].assert_called_once()

    def test_build_site_entity(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        result = entity_builder.build_entity({
            "type": "site",
            "data": {"name": "NYC-DC1", "status": "active"},
        })
        mock_classes["Site"].assert_called_once_with(name="NYC-DC1", status="active")

    def test_build_ip_address_entity(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        result = entity_builder.build_entity({
            "type": "ip_address",
            "data": {"address": "10.0.1.1/24", "status": "active"},
        })
        mock_classes["IPAddress"].assert_called_once_with(
            address="10.0.1.1/24", status="active"
        )

    def test_build_entity_with_string_data(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        result = entity_builder.build_entity({
            "type": "site",
            "data": "NYC-DC1",
        })
        mock_classes["Site"].assert_called_once_with("NYC-DC1")

    def test_build_entity_unknown_type_raises(self, mock_sdk):
        _, entity_builder = mock_sdk
        with pytest.raises(ValueError, match="Unknown entity type 'nonexistent'"):
            entity_builder.build_entity({"type": "nonexistent", "data": {}})

    def test_build_entity_missing_type_raises(self, mock_sdk):
        _, entity_builder = mock_sdk
        with pytest.raises(ValueError, match="must have a 'type' field"):
            entity_builder.build_entity({"data": {"name": "test"}})

    def test_build_entity_empty_data(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        result = entity_builder.build_entity({"type": "device"})
        mock_classes["Device"].assert_called_once_with()


class TestBuildEntities:
    def test_build_multiple_entities(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        entities = entity_builder.build_entities([
            {"type": "site", "data": {"name": "Site A"}},
            {"type": "device", "data": {"name": "Device A"}},
            {"type": "ip_address", "data": {"address": "10.0.0.1/24"}},
        ])
        assert len(entities) == 3
        mock_classes["Site"].assert_called_once_with(name="Site A")
        mock_classes["Device"].assert_called_once_with(name="Device A")
        mock_classes["IPAddress"].assert_called_once_with(address="10.0.0.1/24")

    def test_build_empty_list(self, mock_sdk):
        _, entity_builder = mock_sdk
        entities = entity_builder.build_entities([])
        assert entities == []


class TestSupportedEntityTypes:
    def test_supported_types_is_sorted(self, mock_sdk):
        _, entity_builder = mock_sdk
        types = entity_builder.SUPPORTED_ENTITY_TYPES
        assert types == sorted(types)

    def test_all_core_types_present(self, mock_sdk):
        _, entity_builder = mock_sdk
        core_types = [
            "device", "site", "ip_address", "prefix", "vlan", "vrf",
            "interface", "rack", "manufacturer", "platform", "tenant",
            "circuit", "provider", "cluster", "virtual_machine",
        ]
        for t in core_types:
            assert t in entity_builder.SUPPORTED_ENTITY_TYPES

    def test_entity_type_map_consistency(self, mock_sdk):
        _, entity_builder = mock_sdk
        for type_name, (kwarg, cls) in entity_builder.ENTITY_TYPE_MAP.items():
            assert kwarg, "kwarg must not be empty for {0}".format(type_name)
            assert cls is not None, "class must not be None for {0}".format(type_name)


class TestDeviceEntityFields:
    def test_device_with_all_common_fields(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        entity_builder.build_entity({
            "type": "device",
            "data": {
                "name": "switch-01",
                "device_type": "Catalyst 9300",
                "site": "NYC-DC1",
                "role": "access-switch",
                "status": "active",
                "serial": "ABC123",
                "asset_tag": "ASSET-001",
                "platform": "ios-xe",
                "manufacturer": "Cisco",
                "tags": ["managed", "production"],
            },
        })
        mock_classes["Device"].assert_called_once_with(
            name="switch-01",
            device_type="Catalyst 9300",
            site="NYC-DC1",
            role="access-switch",
            status="active",
            serial="ABC123",
            asset_tag="ASSET-001",
            platform="ios-xe",
            manufacturer="Cisco",
            tags=["managed", "production"],
        )


class TestEntityTypeCoverage:
    """Verify every entity type in the map can be built."""

    def test_all_entity_types_buildable(self, mock_sdk):
        mock_classes, entity_builder = mock_sdk
        for type_name in entity_builder.SUPPORTED_ENTITY_TYPES:
            entity_builder.build_entity({
                "type": type_name,
                "data": {},
            })
