import re
import scrapy
from ..items import PropertiesInMarketItem  
#from ..scrapy_style.properties_in_market.properties_in_market.items import PropertiesInMarketItem
from scrapy.crawler import CrawlerProcess
import sys
import json

# terminal use:
# cd to location
# cd properties_in_market
# use scrapy: scrapy crawl properties (name of file at the end)


class propertySpider(scrapy.Spider):
    name = 'properties'

    custom_settings = {
#        'DOWNLOAD_DELAY': 0.25,
        'DOWNLOAD_MAXSIZE': 0,
        'CONCURRENT_REQUESTS_PER_DOMAIN':1
    }

    page_number = 1

    start_urls = [
        @@@@
    ]   # Anonymize for privacy.


    def parse(self, response):

        # Property

        all_properties = response.css(".card--listing-card")

        for property in all_properties:
            yield response.follow(
                property.css("figure a")[0],
                self.parse_property,
                #cb_kwargs={"property": self.output[i][-1]}
                cb_kwargs = {"items": property.css("figure a")[0] }
            )

            print("elements in each page",range(len(all_properties)))

        count_url = 0
        for url in propertySpider.start_urls:

            for j in re.finditer('homes[/][a-z][a-z][/][a-z]+[/]', url):
                print(j.start(), j.end())
                x = j.end()
                y = range(1,22)
                for z in y:
                    count_url += 1
                    next_page = url[:x] + str(z) + '/' + url[x:]
                    print(next_page)

        # Pagination
                    if propertySpider.page_number < count_url:
                        propertySpider.page_number += 1
                        yield  response.follow(next_page,callback = self.parse)


    def parse_property (self, response,items):

        items = PropertiesInMarketItem()

        rlp_data = response.css("#rlp-data")

        identifier = f'MLS® # {rlp_data.attrib["data-mls"]}'
        city = rlp_data.attrib["data-city"]
        price = rlp_data.attrib["data-listing-price"]
        address = rlp_data.attrib["data-address"]


        items["identifier"] = identifier
        items["city"] = city
        items["price"] = price
        try:
            items["address"] = address
        except:
            pass
        items["beds"] = rlp_data.attrib["data-beds"]
        items["baths"] = rlp_data.attrib["data-baths"]

        items["description"] = response.css("p.body-15::text").get()

        items["features"] = "; ".join(
            [
                f'{feature.css(".label::text").get()} {feature.css(".value::text").get()}'
                for feature in response.css('ul[class="property-features-list"] li')
            ]
        )

        check = 0

        for entry in response.css(".demostats-item div"):
            try:

                items[
                    entry.css("p::text")
                    .get()
                    .strip()
                    .lower()
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("-", "_")
                ] = entry.css("span::text").get()


                # add each item name to list, then check if uni_below bach is in the list, if not replace
                lista_entry = []
                lista_entry.append(entry.css("p::text")
                                   .get()
                                   .strip()
                                   .lower()
                                   .replace(" ", "_")
                                   .replace("/", "_")
                                   .replace("(", "")
                                   .replace(")", "")
                                   .replace("-", "_"))
                if "university_certificate_below_bachelor" in lista_entry: 
                    print("BACHELOR FOUND !!!")
                elif "university_certificate_below_bachelor" not in lista_entry:
                    items["university_certificate_below_bachelor"] = '0%'
                    print('NO BELOW_BACHELOW HERE ... ')
                else:
                    pass


            except AttributeError:
                continue


        rlp_demo_data = json.loads(response.css("#rlp-demo-data::text").get())
        items[
            "one_person"
        ] = f"{rlp_demo_data['household_composition']['single_person']*100:.2f}%"
        items[
            "one_family"
        ] = f"{rlp_demo_data['household_composition']['single_family']*100:.2f}%"
        items[
            "two_plus_people"
        ] = f"{rlp_demo_data['household_composition']['multi_person']*100:.2f}%"
        items[
            "two_plus_families"
        ] = f"{rlp_demo_data['household_composition']['multi_family']*100:.2f}%"

        for age in rlp_demo_data["population_age"]:
            items[f"age{age}"] = f"{rlp_demo_data['population_age'][age] * 100:.2f}%"

        for language in rlp_demo_data["official_language_knowledge"]:
            items[
                language
            ] = f"{rlp_demo_data['official_language_knowledge'][language] * 100:.2f}%"
        items["mother_tongue"] = "; ".join(
            [
                f"{language}: {percentage*100:.2f}%"
                for language, percentage in rlp_demo_data["mother_tongue"].items()
            ]
        )
        items["owners"] = f"{rlp_demo_data['housing_tenancy']['owners'] * 100:.2f}%"
        items["renters"] = f"{rlp_demo_data['housing_tenancy']['renters'] * 100:.2f}%"

        yield items

