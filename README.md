# OpenWrt Docker (WIP)
A containerized OpenWrt network for testing and developing configs. This project creates an isolated Docker network where client containers route traffic through an OpenWrt router container, enabling testing of network configurations, bandwidth throttling, etc.

## Getting Started

### 1. Build images and start the containers
```bash
docker compose up -d --build
```

### 2. Access the Network Dashboard
Open `localhost:4000` and verify that traffic is routing correctly through the OpenWrt container.

### 3. Access OpenWrt Web Interface
1. Open `localhost:4080` in your browser
2. Login with no password (default configuration)

**Note:** If LuCI doesn't load, install it [manually](https://openwrt.org/docs/guide-user/luci/luci.essentials#tab__for_stable_releases_up_to_2410):
```bash
docker exec -it router sh
opkg update
opkg install luci
```

### 4. Test Network Performance
Simulate heavy traffic to test bandwidth controls:
```bash
docker exec -it client-heavy sh
curl -o /dev/null https://ash-speed.hetzner.com/100MB.bin
```
