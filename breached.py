import requests
import re
import json
from datetime import datetime

class PhoneOSINT:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Breached-OSINT/1.0)"
        }

    def validate_phone(self, phone):
        phone = re.sub(r'\D', '', phone)
        if len(phone) < 10:
            return {"valid": False}
        return {"valid": True, "formatted": f"+{phone}"}

    def telecom_lookup(self, phone, api_key=None):
        if not api_key:
            return {"info": "No API key provided"}

        try:
            url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone}"
            res = requests.get(url, timeout=10)
            data = res.json()

            if data.get("valid"):
                return {
                    "country": data.get("country_name"),
                    "carrier": data.get("carrier"),
                    "line_type": data.get("line_type")
                }
        except:
            pass

        return {"info": "Lookup failed"}

    def generate_dorks(self, phone):
        return [
            f'"{phone}"',
            f'"{phone}" site:facebook.com',
            f'"{phone}" site:instagram.com',
            f'"{phone}" site:linkedin.com',
            f'"{phone}" site:twitter.com',
            f'"{phone}" "whatsapp"',
            f'"{phone}" filetype:pdf',
            f'"{phone}" "resume"',
        ]

    def run(self, phone, api_key=None):
        print("="*60)
        print("🔍 Breached - Phone OSINT Tool")
        print("="*60)

        result = {}
        validation = self.validate_phone(phone)

        if not validation["valid"]:
            print("❌ Invalid phone number")
            return

        phone = validation["formatted"]
        result["phone"] = phone

        print(f"📱 Phone: {phone}")

        telecom = self.telecom_lookup(phone, api_key)
        result["telecom"] = telecom

        print("\n📡 Telecom Info:")
        for k, v in telecom.items():
            print(f"   {k}: {v}")

        dorks = self.generate_dorks(phone)
        result["dorks"] = dorks

        print("\n🔍 Google Dorks:")
        for d in dorks:
            link = f"https://google.com/search?q={requests.utils.quote(d)}"
            print(f"   {link}")

        with open("output.json", "w") as f:
            json.dump(result, f, indent=4)

        print("\n💾 Results saved to output.json")
        print("="*60)
        print("⚖️ Use ethically and legally only")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Breached - Phone OSINT Tool")
    parser.add_argument("phone", help="Phone number")
    parser.add_argument("--api", help="NumVerify API key", required=False)

    args = parser.parse_args()

    tool = PhoneOSINT()
    tool.run(args.phone, args.api)
