#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
echo "♾️ กำลังเริ่มระบบออโต้อัมตะ..."

# หาไฟล์ core แล้วรันแบบหาพอร์ตว่างเอง
python3 critical_auto.py &
sleep 5

if [ -f critical_port.txt ]; then
  PORT=$(cat critical_port.txt)
  echo ""
  echo "✅ หัวใจตื่นแล้วที่พอร์ต $PORT"
  echo "🌐 กำลังเปิดประตูสู่โลกภายนอก..."
  echo ""
  cloudflared tunnel --url http://localhost:$PORT 2>&1 | grep -E "trycloudflare|INF.*https"
else
  echo "❌ หาพอร์ตไม่เจอ"
fi
