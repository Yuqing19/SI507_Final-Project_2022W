class Museum:
    def __init__(self, json=None):
        "Initialize a Museum object with json input (a dictionary)"
        self.name = json.get("title") or "N/A"
        self.longitude = json.get("location")["longitude"] or 0
        self.exhibit_number = json.get("children_count") or 0
        self.rating_average = float(self.get_rating_average(json))
        self.languages = json.get("languages") or "N/A"
    
    def get_rating_average(self, json):
        reviews = json.get("reviews")
        if reviews:
            return reviews["rating_average"]
        else:
            return 0

  
