import requests


class JustEatClient:
    API_URL = "https://uk.api.just-eat.io/restaurants/bypostcode/"

    def by_postcode(self, postcode):
        url = f"{self.API_URL}{postcode}"
        response = self.make_request(url)
        return self.parse_response(response)

    def make_request(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request: {str(e)}")

    def parse_response(self, response):
        try:
            restaurants = []
            for restaurant_data in response.get("Restaurants", []):
                cuisines = [
                    cuisine["Name"] for cuisine in restaurant_data.get("Cuisines", [])
                ]
                restaurant = {
                    "Name": restaurant_data.get("Name"),
                    "Rating": restaurant_data.get("RatingStars"),
                    "Cuisines": cuisines,
                }
                restaurants.append(restaurant)
            return restaurants
        except Exception as e:
            raise Exception(f"Error parsing response: {str(e)}")


if __name__ == "__main__":
    client = JustEatClient()
    postcode = "your_postcode_here"
    try:
        restaurants = client.by_postcode(postcode)
        print(restaurants)
    except Exception as e:
        print(f"Error: {str(e)}")
