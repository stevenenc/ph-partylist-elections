import scrapy
import re

class PartylistTemplateSpider(scrapy.Spider):
    name = "partylist_template"
    allowed_domains = ["en.wikipedia.org"]

    def start_requests(self):
        years = [1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
        template_pages = [
            f"https://en.wikipedia.org/wiki/Template:{year}_Philippine_House_party-list_election_results"
            for year in years
        ]
        for url in template_pages:
            yield scrapy.Request(url, callback=self.parse_template)

    def parse_template(self, response):
        year_match = re.search(r'Template:(\d{4})_', response.url)
        year = year_match.group(1) if year_match else None

        for table in response.css("table.wikitable"):
            for row in table.css("tr")[1:]:
                cols = row.css("td")
                if not cols or len(cols) < 2:
                    continue

                # Detect party name column
                party_cell_index = 0
                first_text = cols[0].css("::text").get(default="").strip()
                first_link = cols[0].css("a::text").get(default="").strip()
                if not first_text and not first_link:
                    party_cell_index = 1

                party_td = cols[party_cell_index]
                party_name = party_td.css("a::text").get() or party_td.css("::text").get()
                if not party_name:
                    continue
                party_name = party_name.strip()

                if party_name.lower() in ["total", "valid votes", "invalid/blank votes"]:
                    continue

                party_url = party_td.css("a::attr(href)").get()
                party_url = response.urljoin(party_url) if party_url else None

                remaining = cols[party_cell_index + 1:]
                values = [td.css("::text").get(default="").strip() for td in remaining]
                values += [None] * (6 - len(values))

                votes, vote_pct, pct_change, seats, seat_change = values[:5]

                yield {
                    "year": year,
                    "party_name": party_name,
                    "party_url": party_url,
                    "votes": votes,
                    "vote_percentage": vote_pct,
                    "percent_change": pct_change,
                    "seats": seats,
                    "seat_change": seat_change,
                    "source": response.url,
                }
