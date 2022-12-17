# FindMuseum

## Prerequisite:
(P.S. Prerequisite 1 & 2 are for interactions.)
1. [flask](https://flask.palletsprojects.com/en/2.2.x/): `pip3 install flask`
2. [requests](https://requests.readthedocs.io/en/latest/): `pip3 install requests`
3. Visit the izi travel website(https://www.izi.travel/en/api) to get the database for museums. You can send an email to [support@izi.travel] to receive an API key. You can edit the parameter 'API_KEY' in the file named 'cache_api.py' and put your own key.

## Run the code:
1. Download the code.
2. Run 'python3 main.py' and access the link in the terminal (e.g. http://127.0.0.1:5000/)
3. You should answer four questions and we will provide 5(by default) museums which meet your requirements. If you want to find more museums, you can change the number on the website. You can press 'reroll' to get another branch of museums meeting your requirements and 'Try again' to change your answers. By clicking the name of the museum, you can access the google webpage for the specific museum to find more information.
4. Press CTRL+C to quit.
