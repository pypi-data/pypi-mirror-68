import json 
from mechanize import Browser
from lxml import html

def getCity(city=""):
    
    if city != "":
        if city.lower() == "de haan" or city.lower() == "den haan":
            city = "Den Haan"

        # Selects city
        browser = Browser()
        browser.open('https://www.surf-forecast.com')

        def select_form(form):
            return form.attrs.get('action', None) == '/breaks/catch'

        browser.select_form(predicate=select_form)
        
        browser.form["query"] = city

        res = browser.submit()
        
        # Requests data from page
        content = res.read()
        tree = html.fromstring(content)

        # Checks for errors
        errors = len(tree.xpath('//*[@id="flash_error"]'))
        
        if errors != 0:
            raise ValueError("City does not exist.")
        if errors == 0:
            if tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[4]/b/span[3]/text()')[0] == "C":
                temp_unit = "Celsius"
            elif tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[4]/b/span[3]/text()')[0] == "F":
                temp_unit = "Fahrenheit"

            if city != "Den Haan":
                city_name = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[4]/b/span[1]/text()')[0][:-1]
            else:
                city_name = "De Haan"

            country = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[1]/a[2]/text()')[0]
            date = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[2]/text()')[0].replace("7 Day Weather and Surf, issued ", "")
            last_updated = '-' + tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[4]/div[3]/div[1]/h2/span/text()')[0].replace(" ago", "")
            temp = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[4]/b/span[2]/text()')[0]
            temp_mean = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[4]/span/i/span[1]/text()')[0]
            temp_min = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[4]/span/i/span[3]/text()')[0]
            temp_max = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/section/div/div[2]/div[4]/span/i/span[2]/text()')[0]
            wind = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[4]/div[3]/div[1]/div[1]/div[1]/span[1]/text()')[0]
            wind_unit = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[4]/div[3]/div[1]/div[1]/div[1]/span[2]/text()')[0]
            wind_dir = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[4]/div[3]/div[1]/div[1]/div[2]/text()')[0]
            active_coastal_zone = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[4]/div[3]/div[1]/div[2]/text()')[0]

            # Returns json of data
            data = {
                'location': {
                    'city': city_name,
                    'country': country,
                },
                'time': {
                    'date': date,
                    'last_updated': last_updated,
                },
                'main': {
                    'temp': float(temp),
                    'temp_mean': float(temp_mean),
                    'temp_min': float(temp_min),
                    'temp_max': float(temp_max),
                    'temp_unit': temp_unit
                },
                'wind': {
                    'wind': float(wind),
                    'wind_unit': wind_unit,
                    'wind_dir': wind_dir
                },
                'active_coastal': {
                    'zone': active_coastal_zone
                }
            }

            data = json.dumps(data, indent=4, ensure_ascii=False)

            return data

    else:
        raise ValueError("City is not defined.")