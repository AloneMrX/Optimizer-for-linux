#!/bin/bash

# Update package list and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# Install performance tools
sudo apt install -y \
    preload \
    zram-config \
    iotop \
    iftop \
    nmon \
    sysbench \
    lm-sensors \
    cpufrequtils \
    tlp \
    thermald

# Enable and start TLP for power management
sudo tlp start

# Enable zram (compresses RAM usage)
sudo systemctl enable zram-config

# Optimize swappiness (default is 60, lower for less swapping)
echo "Setting swappiness to 10..."
echo "10" | sudo tee /proc/sys/vm/swappiness

# Optimize dirty ratio
echo "Setting dirty ratio..."
echo "10" | sudo tee /proc/sys/vm/dirty_ratio
echo "5" | sudo tee /proc/sys/vm/dirty_background_ratio

# Set CPU governor to performance
echo "Setting CPU governor to performance..."
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do
    echo "performance" | sudo tee "$cpu/cpufreq/scaling_governor"
done

# Enable necessary systemd services for performance
sudo systemctl enable cpufrequtils

# Increase file handles limit
echo "fs.file-max = 100000" | sudo tee -a /etc/sysctl.conf
echo "root soft nofile 100000" | sudo tee -a /etc/security/limits.conf
echo "root hard nofile 100000" | sudo tee -a /etc/security/limits.conf
echo "session required pam_limits.so" | sudo tee -a /etc/pam.d/common-session

# Clear cache
sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"

# Optimize background services
sudo systemctl disable apport.service

# Install and configure `ufw` for security without sacrificing performance
sudo apt install -y ufw
sudo ufw enable

# Install `earlyoom` to kill processes using too much memory
sudo apt install -y earlyoom
sudo systemctl enable earlyoom

# Set up Swap if not already configured
if [ ! -f /swapfile ]; then
    echo "Setting up swap file..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    sudo swapon -a
fi

# Final message
echo "Optimization complete! Please restart your system for changes to take effect."
