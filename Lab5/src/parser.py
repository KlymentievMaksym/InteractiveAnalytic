import re
import pandas as pd

class LogParser:
    def __init__(self):  # WTF???
        self.pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<date>.*?)\].*?"(?P<url>.*?)"\s(?P<status>\d+)\s(?P<size>\d+)'
            # r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'             # %h - IP address
            # r'(?P<ident>\S+)\s+'                         # %l - identd user (often '-')
            # r'(?P<user>\S+)\s+'                          # %u - authenticated user (often '-')
            # r'\[(?P<time>[^\]]+)\]\s+'                   # %t - time [10/Oct/2025:13:55:36 +0200]
            # r'"(?P<request>[^"]*)"\s+'                   # %r - "GET /index.html HTTP/1.1"
            # r'(?P<status>\d{3})\s+'                      # %>s - status code
            # r'(?P<size>\S+)\s+'                          # %b - response size (can be '-' or number)
            # r'"(?P<referer>[^"]*)"\s+'                   # %{Referer}i
            # r'"(?P<user_agent>[^"]*)"'                   # %{User-Agent}i
        )

    def parse_logs(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        parsed = []
        for _, row in df_raw.iterrows():
            match = self.pattern.search(row["text"])
            if match:
                parsed.append(match.groupdict())
        return pd.DataFrame(parsed)
