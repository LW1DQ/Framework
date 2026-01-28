#!/usr/bin/env python3
"""
Smoke Test for A2A Framework
Verifies that NS-3 Python bindings are working and a minimal simulation can run.
"""

import sys
import unittest
import os
from pathlib import Path

# Add NS-3 paths
# Assuming standard setup or sourced environment
# The test runner should ensure PYTHONPATH is set, but we try to help
NS3_DIR = os.getenv("NS3_DIR", os.path.expanduser("~/ns3"))
if "PYTHONPATH" not in os.environ:
    sys.path.insert(0, str(Path(NS3_DIR) / "build/lib/python3"))
    sys.path.insert(0, str(Path(NS3_DIR) / "build/bindings/python"))

try:
    import ns.core
    import ns.network
    import ns.internet
    import ns.mobility
    import ns.wifi
    import ns.applications
    NS3_AVAILABLE = True
except ImportError:
    NS3_AVAILABLE = False


class TestNS3Environment(unittest.TestCase):
    def setUp(self):
        if not NS3_AVAILABLE:
            self.fail("NS-3 Python bindings not installed or not found in PYTHONPATH")

    def test_ns3_version(self):
        """Test if we can access NS-3 version"""
        print(f"NS-3 Version: {ns.core.Version()}")
        self.assertTrue(True)

    def test_minimal_simulation(self):
        """Run a minimal WiFi simulation (0.1s) to verify binding stability"""
        print("Running minimal simulation...")
        
        # 1. Create Nodes
        nodes = ns.network.NodeContainer()
        nodes.Create(2)
        
        # 2. Setup WiFi
        wifi = ns.wifi.WifiHelper()
        wifi.SetStandard(ns.wifi.WIFI_STANDARD_80211a)
        
        phy = ns.wifi.YansWifiPhyHelper()
        channel = ns.wifi.YansWifiChannelHelper.Default()
        phy.SetChannel(channel.Create())
        
        mac = ns.wifi.WifiMacHelper()
        mac.SetType("ns3::AdhocWifiMac")
        
        devices = wifi.Install(phy, mac, nodes)
        
        # 3. Internet Stack
        stack = ns.internet.InternetStackHelper()
        stack.Install(nodes)
        
        address = ns.internet.Ipv4AddressHelper()
        address.SetBase(ns.network.Ipv4Address("10.1.1.0"), 
                        ns.network.Ipv4Mask("255.255.255.0"))
        interfaces = address.Assign(devices)
        
        # 4. Applications (UDP Echo)
        echoServer = ns.applications.UdpEchoServerHelper(9)
        serverApps = echoServer.Install(nodes.Get(0))
        serverApps.Start(ns.core.Seconds(0.0))
        serverApps.Stop(ns.core.Seconds(0.1))
        
        echoClient = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(0), 9)
        echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
        echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(0.1)))
        echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
        
        clientApps = echoClient.Install(nodes.Get(1))
        clientApps.Start(ns.core.Seconds(0.05))
        clientApps.Stop(ns.core.Seconds(0.1))
        
        # 5. Run
        ns.core.Simulator.Stop(ns.core.Seconds(0.1))
        ns.core.Simulator.Run()
        ns.core.Simulator.Destroy()
        
        print("Minimal simulation completed successfully.")
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
