#!/bin/bash
# security_audit.sh

echo "====================================="
echo " SECURITY AUDIT REPORT "
echo " Date: $(date)"
echo "====================================="
echo ""


echo "1. Open Ports (Listening Services):"
ss -tuln

echo ""
echo "2. Running Services (Top 5 by Memory):"
ps aux --sort=-%mem | head -6

echo ""
echo "3. Failed Login Attempts (Last 10):"
sudo grep "Failed Password" /var/login/auth.log 2>/dev/null | tail -10

echo ""
echo "4. Users with Root Privileges (UID 0):"
grep ':0:' /etc/passwd

echo ""
echo "5. Active Network Connections:"
ss -s

echo ""
echo "================================================="
echo " AUDIT COMPLETE "
echo "================================================="
