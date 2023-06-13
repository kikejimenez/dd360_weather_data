import scrape_reg_exp

if __name__ == "__main__":
    cities = ["ciudad-de-mexico", "monterrey", "merida", "wakanda"]
    for city in cities:
        scrape_reg_exp.scrape_weather_data(city)