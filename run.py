from bs4 import BeautifulSoup
from urllib.request import urlopen
import itertools

base_url = 'https://www.evarzytynes.lt'

escapes = ''.join([chr(char) for char in range(1, 32)])

def auction_parser(url):
    auction_page = urlopen(url)
    auction_soup = BeautifulSoup(auction_page, 'html.parser')
    max_price_so_far = auction_soup.find('span', attrs={'id': 'maxBid'}).contents[0].strip()
    
    auction_desc = auction_soup.find('div', attrs={'class': 'load_block'})
    product_descs = auction_soup.find_all('div', attrs={'class': 'product_desc'})
    for product_desc in product_descs:

        product_property_tuples = list(zip(product_desc.find('ul', attrs={'class': 'list'}).find_all('span', attrs={'class': 'left'}),
                product_desc.find('ul', attrs={'class': 'list'}).find_all('span', attrs={'class': 'right'})))

        auction_property_tuples = list(zip(auction_desc.find('ul', attrs={'class': 'list'}).find_all('span', attrs={'class': 'left'}),
                auction_desc.find('ul', attrs={'class': 'list'}).find_all('span', attrs={'class': 'right'})))

        properties = {}
        for product_property_tuple in product_property_tuples:
            properties.setdefault(product_property_tuple[0].text.strip(), product_property_tuple[1].text.strip())

        for auction_property_tuple in auction_property_tuples:
            properties.setdefault(auction_property_tuple[0].text.strip(), auction_property_tuple[1].text.strip())

        properties.setdefault('url', url)
        yield properties

def auction_list_parser():
    content_exists = True
    result = []
    page_id = 0

    while content_exists:
        url = f'{base_url}/evs/pages/auctions.do?estateType=1&estateSubtype=1&stateType=PASKELBTA-IR-VYKSTA&page={page_id}'
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        sub_result = soup.find_all('div', attrs={'class': 'no'})
        if sub_result:
            result.append(sub_result)
            page_id += 1
            print(f'Reading page {page_id}')

        else:
            content_exists = False
    return result
    
if __name__ == '__main__':
    auction_urls = len(list(itertools.chain(*auction_list_parser())))
    print(f'Found {auction_urls} auctions')


    result = []
    for i in list(itertools.chain(*auction_urls)):
        auction_url = base_url + i.find('a')['href']
        for auction_object in auction_parser(auction_url):
            result.append(pd.DataFrame.from_dict(auction_object, orient='index').T)

    if result:    
        final = pd.concat(result)

        final['Bendras plotas:'] = final['Bendras plotas:'].apply(lambda x: str(x).translate(escapes).replace('\n', '').replace('\r', ''))
        final['Užstatytas plotas:'] = final['Užstatytas plotas:'].apply(lambda x: str(x).translate(escapes).replace('\n', '').replace('\r', ''))

        final.to_excel('evarzytines.xlsx', index=False)

        
        
        
        
        
        
        
          
        
# final['Pradinė pardavimo kaina, Eur:'] = (final['Pradinė pardavimo kaina:']
#                                      .apply(lambda x: float(''.join(c for c in x if c.isdigit())
#                                                            )
#                                            )
#                                     )



# def parsed_area(x):
#     result = (''.join(c for c in x.split('a.')[0] if c.isdigit()))
#     if result:
#         return float(result)
#     return None

# final['Bendras plotas (a):'] = (final['Bendras plotas:']
#                                      .apply(lambda x: parsed_area(x)
#                                            )
#                                     )





# final['Vieno aro pradine kaina, Eur:'] = final['Pradinė pardavimo kaina:'] / final['Bendras plotas (a):']



# (final[(final['Turto potipis:'] == 'Sklypai') &
#      (final['Parduodama turto dalis:'] == '1/1') &
#       (final['Vieno aro pradine kaina, Eur:'] < 15) & 
#       (final['Bendras plotas (a):'] > 15)]
#  .sort_values('Vieno aro pradine kaina, Eur:')
# [['Vieno aro pradine kaina, Eur:',
#   'Bendras plotas:',
#   'Adresas:', 
#  'Pradinė pardavimo kaina:',
#   'Pabaigos data:',
#   'Būsena:',
#        'Dalyvio mokestis:',
#   'Dalyvio registracijos tvirtinimo trukmė d. d.:',
#        'Garantinis įnašas:',
#   'Interneto nuoroda:', 
#   'Kadastrinis Nr.:',
#        'Kambarių/patalpų skaičius:', 
#    'Aprašymas:',
#   'Pagrindas',
#        'Parduodama turto dalis:',
#        'Pradinė NT pardavimo kaina iš bendros pradinės pardavimo kainos:',
       
#        'Pradinė žemės sklypo pardavimo kaina iš bendros pradinės pardavimo kainos:',
#        'Pradinė žemės sklypo vertė žemės sklypo mokesčiui apskaičiuoti:',
#        'Pradžios data:', 'Registracijos pabaiga:', 'Registracijos pradžia:',
#        'Registravimo mokestis:', 'Savininkai:', 'Sklypas:', 'Tipas:',
#        'Turtas PVM objektas:', 'Turto nuosavybės apribojimai:',
#        'Turto potipis:', 'Turto sąrašas:', 'Unikalus Nr.:',
#        'Užstatytas plotas:', 'url', 'Bendras plotas (a):'
#        ]]
# )
