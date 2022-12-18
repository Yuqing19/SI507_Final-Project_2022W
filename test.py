from bs4 import BeautifulSoup
import requests

response = requests.get('https://www.google.com/search?q=Leeton+Museum+and+Gallery&newwindow=1&ei=OHSdY4HGAvaJptQP9LOEqAQ&ved=0ahUKEwiBwvD0lID8AhX2hIkEHfQZAUUQ4dUDCBA&uact=5&oq=Leeton+Museum+and+Gallery&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwA0oECEEYAEoECEYYAFAAWABg4QRoAXABeACAAQCIAQCSAQCYAQDIAQfAAQE&sclient=gws-wiz-serp')
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())
score_board = soup.find_all('img')
print(score_board)
# print(score_board["audiencescore"])
# print(score_board["tomatometerscore"])