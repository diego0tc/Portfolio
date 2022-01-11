from itemadapter import ItemAdapter # useful for handling different item types with a single interface
import mysql.connector
from .items import PropertiesInMarketItem



class PropertiesInMarketPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = '@@@@',
            user = '@@@@',
            passwd = '@@@@!',
            database = 'housing_market'
        )   # This information was anonymize for privacy reasons
        self.curr = self.conn.cursor()


    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS housing_market_333""")   
        self.curr.execute(""" CREATE TABLE housing_market_333(
                    identifier VARCHAR(100),
                    city TEXT,
                    price CHAR(100),
                    address VARCHAR(100),   
                    beds CHAR(100),
                    baths CHAR(100),
                    description TEXT,
                    features TEXT,
                    one_person CHAR(100),
                    one_family CHAR(100),
                    two_plus_people CHAR(100),
                    two_plus_families CHAR(100),
                    age0_to_4 CHAR(100),
                    age5_to_9 CHAR(100),
                    age10_to_14 CHAR(100),
                    age15_to_19 CHAR(100),
                    age20_to_34 CHAR(100),
                    age35_to_49 CHAR(100),
                    age50_to_64 CHAR(100),
                    age65_to_79 CHAR(100),
                    age80_plus CHAR(100),
                    en_only CHAR(100),
                    fr_only CHAR(100),
                    en_and_fr CHAR(100),
                    other CHAR(100),
                    mother_tongue TEXT,
                    owners  CHAR(100),
                    renters CHAR(100),
                    
                    life_stage TEXT,
                    employment_type TEXT,
                    average_household_income CHAR(100),
                    average_number_of_children CHAR(100),
                    
                    no_certificate_diploma_degree CHAR(100),
                    high_school_certificate_or_equivalent CHAR(100),
                    apprenticeship_trade_certificate_diploma CHAR(100),
                    college_non_university_certificate CHAR(100),
                    university_certificate_below_bachelor CHAR(100),
                    university_degree CHAR(50),
                    
                    by_car CHAR(100),
                    by_public_transit CHAR(100),
                    by_walking CHAR(100),
                    by_bicycle CHAR(100),
                    by_other_methods CHAR(100),
                    
                    apartments_low_and_high_rise CHAR(100),
                    houses CHAR(100)
                    

        )""")   # initially, the table is going to accept in the most simple format. The change should be made in the cleaning process


    def process_item(self, property,spider):

        self.store_db(property)
        return property


    def store_db(self, property):   #
        self.curr.execute("""insert into housing_market_333 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(
            property['identifier'],
            property['city'],
            property['price'],
            property['address'],
            property['beds'],

            property['baths'],
            property['description'],
            property['features'],
            property['one_person'],
            property['one_family'],

            property['two_plus_people'],
            property['two_plus_families'],
            property['age0_to_4'],
            property['age5_to_9'],
            property['age10_to_14'],

            property['age15_to_19'],
            property['age20_to_34'],
            property['age35_to_49'],
            property['age50_to_64'],
            property['age65_to_79'],

            property['age80_plus'],
            property['en_only'],
            property['fr_only'],
            property['en_and_fr'],
            property['other'],

            property['mother_tongue'],
            property['owners'],
            property['renters'],



            property['life_stage'],
            property['employment_type'],
            property['average_household_income'],
            property['average_number_of_children'],
            property['no_certificate_diploma_degree'],

            property['high_school_certificate_or_equivalent'],
            property['apprenticeship_trade_certificate_diploma'],
            property['college_non_university_certificate'],
            property['university_certificate_below_bachelor'],
            property['university_degree'],

            property['by_car'],
            property['by_public_transit'],
            property['by_walking'],
            property['by_bicycle'],
            property['by_other_methods'],

            property['apartments_low_and_high_rise'],
            property['houses']


        ))
        self.conn.commit()

