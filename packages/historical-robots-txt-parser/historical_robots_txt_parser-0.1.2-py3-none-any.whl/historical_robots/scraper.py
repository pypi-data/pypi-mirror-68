import requests
import time
import csv
from urllib.parse import urlencode
from historical_robots.parser import parse_robots_txt


class WaybackScraper:
    def __init__(self, domain, **kwargs):
        self._domain = domain
        self.skip_sleep_interval = False
        self.accept_allow = False
        self.sleep_interval = 0.05
        self.params = {}
        self.__dict__.update(kwargs)

    def get_cdx_records(self):
        uniques = []
        custom_params = f"&{urlencode(self.params)}" if self.params else ""
        request_url = (
            "http://web.archive.org/cdx/search/cdx"
            f"?url={self._domain}/robots.txt&output=csv"
            "&showDupeCount=true&collapse=digest"
            "&filter=statuscode:200&filter=mimetype:text/plain"
            "&fl=timestamp,dupecount"
            f"{custom_params}"
        )

        with requests.get(request_url, stream=True) as res:
            lines = [line for line in res.iter_lines(decode_unicode=True)]
            data = csv.reader(lines, delimiter=" ")
            for item in data:
                if item[1] == "0":
                    uniques.append(item[0])

        print(f"Retrieved {len(uniques)} unique records")

        return uniques

    def scrape_and_serialize(self, file_path):
        iterable_records = self.get_cdx_records()
        writable_data = self.retrieve_data(iterable_records)
        self.write_data(file_path, writable_data)

    def retrieve_data(self, records_to_iterate):
        data_dict = {}
        prev_keys = []
        for timestamp in records_to_iterate:
            parsed_time = time.strptime(timestamp, "%Y%m%d%H%M%S")
            clean_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", parsed_time)
            request_url = (
                "https://web.archive.org/web/"
                f"{timestamp}i_/"
                f"{self._domain}/"
                "robots.txt"
            )
            keys = []
            print(f"Requesting data for {clean_timestamp}")
            data = parse_robots_txt(request_url, self.accept_allow)
            for agent, paths in data.items():
                for path, rule in paths.items():
                    key = "_".join([agent, path, rule])
                    keys.append(key)
                    if key not in data_dict:
                        vals = [agent, path, clean_timestamp, None]
                        if self.accept_allow:
                            vals.append(rule)

                        data_dict[key] = vals

            removed_rules = [key for key in prev_keys if key not in keys]
            for rule in removed_rules:
                if not data_dict[rule][3]:
                    data_dict[rule][3] = clean_timestamp

            prev_keys = keys

            if not self.skip_sleep_interval:
                time.sleep(self.sleep_interval)

        return list(data_dict.values())

    def write_data(self, file_path, data):
        with open(file_path, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            fieldnames = ["User Agent", "Path", "Date Added", "Date Removed"]
            if self.accept_allow:
                fieldnames.append("Rule")
            csv_writer.writerow(fieldnames)
            csv_writer.writerows(data)
            print(f"Data written to {file_path}")


def historical_scraper(domain, file_path, **kwargs):
    WaybackScraper(domain, **kwargs).scrape_and_serialize(file_path)
    return True
