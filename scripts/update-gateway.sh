#!/bin/sh

GATEWAY_IP="10.10.10.10"

# Remove default docker network gateway
ip route del default

# Set OpenWrt as the gateway
ip route add default via ${GATEWAY_IP} dev eth0

echo "Gateway address changed to ${GATEWAY_IP}"

