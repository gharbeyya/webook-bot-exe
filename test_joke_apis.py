import requests
import json
import time

# =====================================================
#   Joke API Tests - اختبارات لمصادر النكات المختلفة
# =====================================================

def test_official_joke_api():
    """اختبار Official Joke API"""
    print("\n🧪 اختبار Official Joke API...")
    print("="*50)
    
    try:
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        print("✅ الاتصال: نجح")
        print(f"📚 المصدر: {data.get('type', 'general')}")
        print(f"😂 النكتة: {data['setup']}")
        print(f"   {data['punchline']}")
        return True
    except Exception as e:
        print(f"❌ الخطأ: {str(e)}")
        return False


def test_dad_jokes_api():
    """اختبار icanhazdadjoke.com"""
    print("\n🧪 اختبار Dad Jokes API...")
    print("="*50)
    
    try:
        response = requests.get(
            "https://icanhazdadjoke.com/?format=json",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        print("✅ الاتصال: نجح")
        print(f"😂 النكتة: {data['joke']}")
        return True
    except Exception as e:
        print(f"❌ الخطأ: {str(e)}")
        return False


def test_multiple_jokes(count=5):
    """اختبار جلب نكات متعددة"""
    print(f"\n🧪 اختبار جلب {count} نكات متعددة...")
    print("="*50)
    
    success_count = 0
    error_count = 0
    
    for i in range(count):
        try:
            print(f"\n📌 النكتة #{i+1}:")
            response = requests.get(
                "https://official-joke-api.appspot.com/random_joke",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"  {data['setup']}")
            print(f"  {data['punchline']}")
            success_count += 1
            
            # تأخير لتجنب الضغط على الـ API
            time.sleep(0.5)
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            error_count += 1
    
    print(f"\n📊 النتائج: {success_count} نجح، {error_count} فشل")


def test_api_limits():
    """اختبار حدود الـ API"""
    print("\n🧪 اختبار حدود الـ API...")
    print("="*50)
    
    print("\nجلب 10 نكات متتالية بسرعة...")
    start_time = time.time()
    
    success = 0
    for i in range(10):
        try:
            response = requests.get(
                "https://official-joke-api.appspot.com/random_joke",
                timeout=5
            )
            if response.status_code == 200:
                success += 1
        except:
            pass
    
    elapsed_time = time.time() - start_time
    
    print(f"✅ نجح: {success}/10")
    print(f"⏱️  الوقت المستغرق: {elapsed_time:.2f} ثانية")
    print(f"📊 المتوسط: {elapsed_time/10:.2f} ثانية لكل طلب")


def test_api_response_time():
    """اختبار وقت الاستجابة"""
    print("\n🧪 اختبار أوقات الاستجابة...")
    print("="*50)
    
    apis = {
        "Official Joke API": "https://official-joke-api.appspot.com/random_joke",
        "Dad Jokes": "https://icanhazdadjoke.com/?format=json"
    }
    
    for api_name, api_url in apis.items():
        try:
            start = time.time()
            response = requests.get(api_url, timeout=5)
            elapsed = time.time() - start
            
            print(f"\n📚 {api_name}:")
            print(f"   ✅ الحالة: {response.status_code}")
            print(f"   ⏱️  وقت الاستجابة: {elapsed*1000:.2f} ms")
        except Exception as e:
            print(f"\n📚 {api_name}:")
            print(f"   ❌ الخطأ: {str(e)}")


# =====================================================
#   تشغيل جميع الاختبارات
# =====================================================

if __name__ == "__main__":
    print("🎭 برنامج اختبار مصادر النكات 🎭")
    print("="*50)
    
    # اختبار كل مصدر على حدة
    test_official_joke_api()
    time.sleep(1)
    
    test_dad_jokes_api()
    time.sleep(1)
    
    # اختبار النكات المتعددة
    test_multiple_jokes(count=5)
    time.sleep(1)
    
    # اختبار أوقات الاستجابة
    test_api_response_time()
    time.sleep(1)
    
    # اختبار حدود الـ API
    test_api_limits()
    
    print("\n" + "="*50)
    print("✅ انتهت جميع الاختبارات!")
    print("="*50)
