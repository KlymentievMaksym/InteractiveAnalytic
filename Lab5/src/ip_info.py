import requests

class IPInfo:
    def __init__(self):
        self.site_root = "http://ip-api.com/json/"

    def get_info(self, ip: str):
        response = requests.get(self.site_root + ip)
        data = response.json()
        if data["status"] == "success":
            return {key: value for key, value in data.items()}
        else:
            return {"error": data["message"]}


if __name__ == "__main__":
    ipinfo = IPInfo()
    print(ipinfo.get_info("46.125.249.79"))
