import os
import time
import subprocess
from colorama import Fore, Style

def display_splash_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.CYAN}  ____    _    _   _  _   _ _____  ____   _____  ____  {Style.RESET_ALL}")
    print(f"{Fore.CYAN} |  _ \  / \  | | | || | | | ____|/ ___| |_   _|/ ___| {Style.RESET_ALL}")
    print(f"{Fore.CYAN} | |_) |/ _ \ | |_| || |_| |  _|  \___ \   | |  \___ \  {Style.RESET_ALL}")
    print(f"{Fore.CYAN} |  _ <| (_) ||  _  ||  _  | |___  ___) |  | |   ___) | {Style.RESET_ALL}")
    print(f"{Fore.CYAN} |_| \_\\___/ |_| |_| |_| |_|_____|____/   |_|  |____/  {Style.RESET_ALL}")
    print(f"{Fore.GREEN}Initializing...{Style.RESET_ALL}")
    time.sleep(3)

def run_bash_script():
    bash_script = """#!/bin/bash

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
    """
    with open('optimize.sh', 'w') as f:
        f.write(bash_script)
    os.chmod('optimize.sh', 0o755)  # Make the script executable
    subprocess.call(['bash', 'optimize.sh'])

def lag_free_optimizations():
    print(f"{Fore.GREEN}Applying Lag-Free Optimizations...{Style.RESET_ALL}")
    
    # Example commands for lag-free optimizations
    subprocess.call(['sysctl', '-w', 'net.ipv4.tcp_sack=1'])
    subprocess.call(['sysctl', '-w', 'net.ipv4.tcp_no_metrics_save=1'])
    subprocess.call(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=cubic'])
    subprocess.call(['sysctl', '-w', 'net.core.rmem_max=16777216'])
    subprocess.call(['sysctl', '-w', 'net.core.wmem_max=16777216'])
    subprocess.call(['sysctl', '-w', 'net.ipv4.tcp_rmem=4096 87380 16777216'])
    subprocess.call(['sysctl', '-w', 'net.ipv4.tcp_wmem=4096 65536 16777216'])
    
    print(f"{Fore.GREEN}Lag-Free optimizations applied successfully.{Style.RESET_ALL}")

def main_menu():
    while True:
        print("\nChoose your optimization options:")
        print("1. Run System Optimization")
        print("2. Apply Lag-Free Optimizations")
        print("3. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            run_bash_script()
        elif choice == '2':
            lag_free_optimizations()
        elif choice == '3':
            print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    display_splash_screen()
    main_menu()
