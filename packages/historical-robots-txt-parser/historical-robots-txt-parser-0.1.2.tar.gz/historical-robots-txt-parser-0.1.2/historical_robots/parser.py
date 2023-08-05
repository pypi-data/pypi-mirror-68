import requests
import re


class RobotTxtParser:
    def __init__(self, url, accept_allow=False):
        self._url = url
        self._accept_allow = accept_allow

    def make_request(self):
        return requests.get(self._url).text

    def check_valid_line(self, line):
        regex_pattern = (
            r"^((dis)?allow|user)" if self._accept_allow else r"^(disallow|user)"
        )
        return line and bool(re.match(regex_pattern, line.strip(), flags=re.IGNORECASE))

    def parse_lines(self, text):
        lines = [line for line in text.splitlines() if self.check_valid_line(line)]
        data_dict = {}
        user_agent = None
        for line in lines:
            if "user agent" in line.lower():
                line = re.sub(r"user\sagent:", line, "user-agent", flags=re.IGNORECASE)
            rule, *values = filter(None, re.split(r"\s+|\t+", line.strip()))
            rule = rule or ""
            value = values[0] if len(values) else ""
            if rule.lower().startswith("user-agent"):
                user_agent = value
                if user_agent not in data_dict:
                    data_dict[user_agent] = {}
            else:
                if not user_agent:
                    user_agent = "*"
                    if user_agent not in data_dict:
                        data_dict[user_agent] = {}
                data_dict[user_agent][value] = rule[:-1]
        # Remove user agents with empty dicts rather than
        # using slow, complex regex in check_valid_line
        return {k: v for k, v in data_dict.items() if v}

    def parse(self):
        txt_file = self.make_request()
        return self.parse_lines(txt_file)


def parse_robots_txt(url, accept_allow=False):
    return RobotTxtParser(url, accept_allow).parse()
