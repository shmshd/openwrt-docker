#!/bin/sh

set -e

GATEWAY_IP="10.10.10.10"

# Remove default docker network gateway
ip route delete default

# Set OpenWrt as the gateway
ip route add default via "$GATEWAY_IP" dev eth0

echo "Gateway address changed to $GATEWAY_IP"
