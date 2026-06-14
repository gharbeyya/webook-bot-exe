import asyncio
import httpx
import random
import logging
from datetime import datetime

# --- 1. إعدادات المراقبة والـ Logs (تم تصحيح المسافة الزائدة) ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("WebookBot")

# --- 2. ملف الإعدادات المركزي (Configuration) ---
CONFIG = {
    "EVENT_ID": "match-event-2026", 
    "TARGET_ZONES": ["113", "114"],  
    "MAX_TICKETS_PER_ACCOUNT": 5,
    "REQUEST_DELAY": 0.5,           
    
    "PROXIES": [
        "http://username:password@proxy_ip1:port",
        "http://username:password@proxy_ip2:port"
    ],
    
    "ACCOUNTS": [
        {"email": "yusefagha@outlook.sa", "auth_token": "ACCESS_TOKEN_HERE_1"},
        {"email": "fesasuperx@gmail.com", "auth_token": "ACCESS_TOKEN_HERE_2"}
    ],
    
    "CAPTCHA_API_KEY": "YOUR_CAPTCHA_SOLVER_API_KEY"
}

class WebookBotEngine:
    def __init__(self, config):
        self.config = config
        self.is_running = False
        self.session_clients = {}

    # --- 3. محرك تخطي الحماية ---
    async def fetch_captcha_token(self, client):
        if not self.config["CAPTCHA_API_KEY"]:
            return None
        
        payload = {
            "clientKey": self.config["CAPTCHA_API_KEY"],
            "task": {
                "type": "AntiTurnstileTaskMini", 
                "websiteURL": "https://webook.com",
                "websiteKey": "SITE_KEY_EXTRACTED_FROM_F12"
            }
        }
        try:
            await asyncio.sleep(0.1)
            return "mock_captcha_token_xyz123"
        except Exception as e:
            logger.error(f"❌ فشل جلب توكن تخطي الكابتشا: {e}")
            return None

    # --- 4. محرك الطلبات الأساسي لكل حساب ---
    async def start_account_worker(self, account):
        email = account["email"]
        token = account["auth_token"]
        
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://webook.com",
            "Referer": "https://webook.com/"
        }

        proxy = random.choice(self.config["PROXIES"]) if self.config["PROXIES"] else None
        
        async with httpx.AsyncClient(proxies=proxy, headers=headers, timeout=3.0) as client:
            logger.info(f"🟢 تم تشغيل الـ Worker للحساب: {email} | البروكسي: {proxy if proxy else 'مباشر'}")
            
            while self.is_running:
                for zone in self.config["TARGET_ZONES"]:
                    try:
                        captcha_token = await self.fetch_captcha_token(client)
                        reserve_url = f"https://webook.com/api/v1/events/{self.config['EVENT_ID']}/book"
                        
                        payload = {
                            "zone_prefix": zone,
                            "quantity": 1,
                            "captcha_token": captcha_token
                        }
                        
                        logger.info(f"📡 [محاولة حجز] الحساب: {email} يرسل طلباً للمربع {zone}...")
                        
                        response = await client.post(reserve_url, json=payload)
                        
                        if response.status_code == 200:
                            res_data = response.json()
                            hold_token = res_data.get("hold_token")
                            # تم تصحيح الدالة هنا من logger.all إلى logger.info
                            logger.info(f"🎉 [نجاح مذهل] تم خطف المقعد للحساب {email}! الرمز: {hold_token}")
                            break
                        elif response.status_code == 429:
                            logger.warning(f"⚠️ [Rate Limit] الحساب {email} يواجه ضغطاً كبيراً، جاري التهدئة...")
                            await asyncio.sleep(2)
                        else:
                            logger.error(f"❌ [فشل] استجابة السيرفر للحساب {email}: {response.status_code} | {response.text}")
                            
                    except httpx.HTTPError as http_err:
                        logger.error(f"⚠️ [خطأ شبكة] الحساب {email}: {http_err}")
                    except Exception as e:
                        logger.error(f"⚠️ [خطأ غير متوقع] في الحساب {email}: {e}")
                
                await asyncio.sleep(self.config["REQUEST_DELAY"])

    # --- 5. مدير تشغيل الحسابات بالتوازي ---
    async def run_engine(self):
        self.is_running = True
        logger.info("🚀 جاري تشغيل نظام الأتمتة...")
        
        tasks = [self.start_account_worker(acc) for acc in self.config["ACCOUNTS"]]
        await asyncio.gather(*tasks)

    def stop_engine(self):
        self.is_running = False
        logger.info("🛑 تم إرسال أمر إيقاف النظام بالكامل.")

if __name__ == "__main__":
    engine = WebookBotEngine(CONFIG)
    try:
        asyncio.run(engine.run_engine())
    except KeyboardInterrupt:
        engine.stop_engine()
        logger.info("النظام توقف بواسطة المستخدم.")
