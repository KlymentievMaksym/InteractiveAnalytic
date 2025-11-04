import re
import pandas as pd

class LogParser:
    def __init__(self, full: bool = False):
        if full:
            self.pattern = re.compile(
                # 192.168.0.5 - john [10/Oct/2025:13:55:36 +0200] "GET /index.html HTTP/1.1" 200 1024 "http://example.com" "Mozilla/5.0" "-"
                r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'             # %h - 192.168.0.5
                r'(?P<ident>\S+)\s+'                         # %l - -
                r'(?P<user>\S+)\s+'                          # %u - john
                r'\[(?P<time>[^\]]+)\]\s+'                   # %t - [10/Oct/2025:13:55:36 +0200]
                r'"(?P<request>[^"]*)"\s+'                   # %r - "GET /index.html HTTP/1.1"
                r'(?P<status>\d{3})\s+'                      # %>s - 200
                r'(?P<size>\S+)\s+'                          # %b - 1024
                r'"(?P<referer>[^"]*)"\s+'                   # %{Referer}i "http://example.com"
                r'"(?P<user_agent>[^"]*)"\s+'                # %{User-Agent}i "Mozilla/5.0"
                r'"(?P<host>[^"]*)"'                         # %{Host} "-"
            )
        else:
            self.pattern = re.compile(
                r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<date>.*?)\].*?"(?P<url>.*?)"\s(?P<status>\d+)\s(?P<size>\d+)'
            )

    def parse_logs(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        parsed = []
        for _, row in df_raw.iterrows():
            match = self.pattern.search(row["text"])
            if match:
                parsed.append(match.groupdict())
        return pd.DataFrame(parsed)
