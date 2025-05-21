import scrapy
import pandas as pd
import re


class PartylistAttributesSpider(scrapy.Spider):
    name = "partylist_attributes"
    allowed_domains = ["en.wikipedia.org"]

    def start_requests(self):
        df = pd.read_csv("partylist_template.csv")

        for _, row in df.iterrows():
            url = row.get("party_url")
            party_name = row.get("party_name")
            if pd.notna(url):
                yield scrapy.Request(
                    url,
                    callback=self.parse_infobox,
                    meta={"party_list": party_name, "source": url}
                )

    def parse_infobox(self, response):
        item = {
            "party_list": response.meta["party_list"],
            "source": response.meta["source"]
        }

        # Look for infobox
        infobox = response.css("table.infobox")

        for row in infobox.css("tr"):
            label = row.css("th::text, th a::text").get()
            if not label:
                continue

            key = (
                label.strip()
                .lower()
                .replace("–", "-")
                .replace("—", "-")
                .replace(" ", "_")
            )

            # Extract both linked and plain text from the value cell
            value_cell = row.css("td")
            value_parts = value_cell.css("a::text").getall() + value_cell.css("::text").getall()
            values = [v.strip() for v in value_parts if v.strip() and not v.strip().startswith("[")]

            if values:
                # Combine into string or list depending on count
                item[key] = values if len(values) > 1 else values[0]

        yield item
