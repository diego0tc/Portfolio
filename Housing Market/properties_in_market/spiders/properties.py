import re

import scrapy
from ..items import PropertiesInMarketItem  # does not work with the run method, use terminal
#from ..scrapy_style.properties_in_market.properties_in_market.items import PropertiesInMarketItem
from scrapy.crawler import CrawlerProcess
import sys
import json

# terminal use:
# cd to location: cd scrapy_style
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

        'https://www.royallepage.ca/en/search/homes/qc/montral/?property_type=&house_type=&features=&listing_type=&lat=45.51240000000007&lng=-73.55468999999994&bypass=&address=Montr%C3%A9al&address_type=city&city_name=Montr%C3%A9al&prov_code=QC&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Montr%C3%A9al%2C+QC%2C+CAN&id_search_str=Montr%C3%A9al%2C+QC%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/on/toronto/?property_type=&house_type=&features=&listing_type=&lat=43.648690000000045&lng=-79.38543999999996&bypass=&address=Toronto&address_type=city&city_name=Toronto&prov_code=ON&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Toronto%2C+ON%2C+CAN&id_search_str=Toronto%2C+ON%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/on/mississauga/?property_type=&house_type=&features=&listing_type=&lat=43.58726000000007&lng=-79.64493999999996&bypass=&address=Mississauga&address_type=city&city_name=Mississauga&prov_code=ON&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Mississauga%2C+ON%2C+CAN&id_search_str=Mississauga%2C+ON%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/ab/calgary/?property_type=&house_type=&features=&listing_type=&lat=51.04532000000006&lng=-114.06300999999996&bypass=&address=Calgary&address_type=city&city_name=Calgary&prov_code=AB&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Calgary%2C+AB%2C+CAN&id_search_str=Calgary%2C+AB%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/on/ottawa/?property_type=&house_type=&features=&listing_type=&lat=45.42178000000007&lng=-75.69115999999997&bypass=&address=Ottawa&address_type=city&city_name=Ottawa&prov_code=ON&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Ottawa%2C+ON%2C+CAN&id_search_str=Ottawa%2C+ON%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/ab/edmonton/?property_type=&house_type=&features=&listing_type=&lat=53.54624000000007&lng=-113.49036999999998&bypass=&address=Edmonton&address_type=city&city_name=Edmonton&prov_code=AB&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Edmonton%2C+AB%2C+CAN&id_search_str=Edmonton%2C+AB%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/on/mississauga/?property_type=&house_type=&features=&listing_type=&lat=43.58726000000007&lng=-79.64493999999996&bypass=&address=Mississauga&address_type=city&city_name=Mississauga&prov_code=ON&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Mississauga%2C+ON%2C+CAN&id_search_str=Mississauga%2C+ON%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/mb/winnipeg/?property_type=&house_type=&features=&listing_type=&lat=49.89953000000003&lng=-97.14112999999998&bypass=&address=Winnipeg&address_type=city&city_name=Winnipeg&prov_code=MB&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Winnipeg%2C+MB%2C+CAN&id_search_str=Winnipeg%2C+MB%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/bc/vancouver/?property_type=&house_type=&features=&listing_type=&lat=49.260380000000055&lng=-123.11335999999994&bypass=&address=Vancouver&address_type=city&city_name=Vancouver&prov_code=BC&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Vancouver%2C+BC%2C+CAN&id_search_str=Vancouver%2C+BC%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/on/brampton/?property_type=&house_type=&features=&listing_type=&lat=43.68431000000004&lng=-79.75871999999998&bypass=&address=Brampton&address_type=city&city_name=Brampton&prov_code=ON&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Brampton%2C+ON%2C+CAN&id_search_str=Brampton%2C+ON%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=',
        'https://www.royallepage.ca/en/search/homes/on/hamilton/?property_type=&house_type=&features=&listing_type=&lat=43.261970000000076&lng=-79.88799999999998&bypass=&address=Hamilton&address_type=city&city_name=Hamilton&prov_code=ON&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Hamilton%2C+ON%2C+CAN&id_search_str=Hamilton%2C+ON%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword='

    ]

#    def __init__(self, *args, **kwargs):
 #       super().__init__(*args, **kwargs)
  #      self.output = [[] for i in range(len(self.start_urls))]

   # def start_requests(self):
    #    for i, url in enumerate(self.start_urls):
     #       yield scrapy.Request(url, cb_kwargs={"i": i})



    def parse(self, response):

        # Property

        all_properties = response.css(".card--listing-card")

        for property in all_properties:
    #        self.output[0].append(items)

            yield response.follow(
                property.css("figure a")[0],
                self.parse_property,
                #cb_kwargs={"property": self.output[i][-1]}
                cb_kwargs = {"items": property.css("figure a")[0] }
            )

            print("elements in each page",range(len(all_properties)))

        count_url = 0
        #page_number = 1
        #pageNa = str(page_number)
        for url in propertySpider.start_urls:

            for j in re.finditer('homes[/][a-z][a-z][/][a-z]+[/]', url):
                print(j.start(), j.end())
                x = j.end()

                y = range(1,22)
                for z in y:
                    count_url += 1
                    next_page = url[:x] + str(z) + '/' + url[x:]
                    print(next_page)

        ### Pagination
        #next_page = 'https://www.royallepage.ca/en/search/homes/qc/montral/' + str(propertySpider.page_number) + '/' + '?property_type=&house_type=&features=&listing_type=&lat=45.51240000000007&lng=-73.55468999999994&bypass=&address=Montr%C3%A9al&address_type=city&city_name=Montr%C3%A9al&prov_code=QC&display_type=gallery-view&da_id=&travel_time=&school_id=&search_str=Montr%C3%A9al%2C+QC%2C+CAN&id_search_str=Montr%C3%A9al%2C+QC%2C+CAN&school_search_str=&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword='
        #next_page= 'https://www.royallepage.ca/en/search/' + extraction + str(propertySpider.page_number) + rest_extrac


#                    if propertySpider.page_number < 22:
 #                       propertySpider.page_number += 1
  #                      yield response.follow(next_page,callback = self.parse)

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
        # if price ...
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
#                if items[entry.css("p::text")] == None:
 #                   items[entry.css("p::text")] = entry.css("span::text").get().strip().replace("",None)

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
                if "university_certificate_below_bachelor" in lista_entry:  #FIX P::TEXT
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



if __name__ == "__main__":
    if len(sys.argv) == 1:
        process = CrawlerProcess()
        process.crawl(propertySpider, start_urls=[input("URL: ").strip()])
        process.start()
    else:
        with open(sys.argv[1], encoding="utf-8") as f:
            links = f.read().split()
        process = CrawlerProcess()
        process.crawl(propertySpider, start_urls=links)
        process.start()




"""




"""