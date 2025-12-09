import requests

class Api:
    BASE_URL = "https://automationexercise.com/api" # base url of the api we will be calling(used for all endpoints)


    def get_all_products(self) -> requests.Response:
        url = f"{self.BASE_URL}/productsList"   # productsList endpoint returns all products

        #send a get request to retrieve product data from the server
        #get means w request data only ! WE DO NOT MODIFY,DELETE,ADD ANYTHING!!
        return requests.get(url) # return the server's raw HTTTP response to be valdiated later.

    def get_all_products_should_return_200(self) -> dict: #main test validation function = returns parsed json

        response = self.get_all_products()  # wil contatin status code + headers + body

        #validate that the status code is 200 (success)
        #if it is not 200,the test must fail because the api did not respond succesfully

        if response.status_code !=200: #raise assertionerror stops the test and prints a clear failure message
            raise AssertionError(
                f"expected status 200, got {response.status_code}. Body:  {response.text}"
            ) #assertionerror means expected condition did NOT met ->test fail

        # Try to convert the response body into JSON format
        # If this fails, the server returned invalid data (not JSON)
        try:
            data = response.json()  # Convert the raw response text into Python dictionary
        except ValueError:  # Raised when JSON decoding fails
                raise AssertionError(f"Invalid JSON. Body: {response.text}")  # Fail if JSON is broken

        # Check if the JSON contains the required key "products"
        # This is essential because we expect the product list to be inside this key
        if "products" not in data:
            raise AssertionError(f"'products' key missing. JSON: {data}")

        # Acces the first product in the list to be inspect its structure and confirm valid content
        first = data["products"][0]

        # Validate that the first product contains required fields: id, name, price
        # These keys must exist - otherwise the API data is incomplete and incorrect

        for key in ("id", "name", "price"):
            if key not in first:
                raise AssertionError(
                    f"Missing key '{key}' in first product. Product: {first}"
                )

        return data # All checks passed -> return the JSON data back to Robot Framework for additional verification

    #### api 2 Post/productlists(negative test)

    def post_products_list(self) -> requests.Response:
        url = f"{self.BASE_URL}/productsList"

        return requests.post(url) # send the Post request - this is the "wrong method" for this endpoint.

    def post_products_list_should_return_405(self) -> dict:

        response = self.post_products_list() # we call the method above to trigger POST request.
        if response.status_code != 200:
            raise AssertionError(
                f"expected HTTP 200 wrapper, got {response.status_code}. Body: {response.text}"
            )
        try:
            data = response.json()
            # Convert response body to JSON.
            # If conversion fails → response is not valid JSON → FAIL.
        except ValueError:
            raise AssertionError(
                f"Invalid JSON. Body: {response.text}"
            )

        # Second validation: Response JSON must indicate method is not allowed.
        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, got {data.get('responseCode')}. "f"JSON: {data}"
            )

        return data # if we reach here both validations passed - > API is behaving correctly
        # return structured JSOn for robot framework test usage

    ###API 3 GET ALL BRANDS LIST

    def get_all_brands(self) -> requests.Response:
        url = f"{self.BASE_URL}/brandsList"
        return requests.get(url)

    def get_all_brands_should_return_200(self) -> dict:
        response = self.get_all_brands()
        if response.status_code != 200:
            raise AssertionError(
                f"Expected status 200, got {response.status_code}. Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")

        if "brands" not in data:
            raise AssertionError(f"'brands' key missing. JSON: {data}")

        return data


    ## API 4

    def put_brands_list(self) -> requests.Response:
        url = f"{self.BASE_URL}/brandsList"
        return requests.put(url)

    def put_brands_list_should_return_405(self) -> dict:
        response = self.put_brands_list()

    # Validation 1
        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200 wrapper, got {response.status_code}. "
                f"Body: {response.text}"
            )
    #validation 2f
        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")
    #Validation 3

        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, got {data.get('responseCode')}. "f"JSON: {data}"
            )

        return data



