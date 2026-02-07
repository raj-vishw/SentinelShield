#!/bin/bash
echo "=========================================="
echo "   SentinelShield Unified Startup Script"
echo "=========================================="

PROJECT_ROOT="$(pwd)"

BACKEND_APP="$PROJECT_ROOT/backend_app.py"
WAF_APP="$PROJECT_ROOT/waf_gateway.py"
UI_DIR="$PROJECT_ROOT/sentinelshield-ui"

echo "[*] Cleaning old processes..."

pkill -f backend_app.py
pkill -f waf_gateway.py
pkill -f "npm run dev"

sleep 2

echo "[*] Starting Backend Application (Port 9000)..."
python "$BACKEND_APP" &
BACKEND_PID=$!

sleep 2

echo "[*] Starting SentinelShield WAF (Port 5000)..."
python "$WAF_APP" &
WAF_PID=$!

sleep 2

echo "[*] Starting Dashboard UI (Port 5173)..."
cd "$UI_DIR" || exit
npm run dev &
UI_PID=$!

cd "$PROJECT_ROOT"

echo ""
echo "=========================================="
echo " SentinelShield Running Successfully"
echo "------------------------------------------"
echo " Backend App   : http://127.0.0.1:9000"
echo " WAF Gateway   : http://127.0.0.1:5000"
echo " Dashboard UI  : http://localhost:5173"
echo "=========================================="
echo ""
echo "Press CTRL+C to stop everything"

trap "echo 'Stopping services...'; kill $BACKEND_PID $WAF_PID $UI_PID; exit" SIGINT

wait
