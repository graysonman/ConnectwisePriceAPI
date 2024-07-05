import requests
import json
import base64
# connectwiseAPI is a separate .py file that stores variables like API keys
import connectwiseAPI

# This function takes the vendorSKU passed in and gets the id from connectwise API
def get_product_id_by_vendor_sku(vendor_sku, headers, base_url):

    endpoint = f"/procurement/catalog"
    # URL with a filter for the venderSKU
    url = f"{base_url}{endpoint}?conditions=vendorSku like '%{vendor_sku}%'"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        products = response.json()
        if products and len(products) > 0:
            return products[0]['id']
        else:
            print(f"No product found with identifier: {vendor_sku}")
            return None
    else:
        print(f"Failed to fetch product by identifier. Status code: {response.status_code}")
        print(response.text)
        return None

#This function takes the found id and sends a patch request with the ADI cost and multiplied price
def patch_product(product_id, new_price, new_cost, headers, base_url):

    endpoint = f"/procurement/catalog/{product_id}"

    url = f"{base_url}{endpoint}"

    payload = [
        {"op": "replace", "path": "/price", "value": new_price},
        {"op": "replace", "path": "/cost", "value": new_cost}
    ]

    response = requests.patch(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        product = response.json()
        print(f"Product {product_id} updated successfully:")
        print(json.dumps(product, indent=4))
    else:
        print(f"Failed to update product. Status code: {response.status_code}")
        print(response.text)
        
#This function calls the connectwise API then calls search to find the product id
def connectwise_API(vendor_sku, new_price, new_cost):

    company_id = connectwiseAPI.company_id
    public_key = connectwiseAPI.public_key
    private_key = connectwiseAPI.private_key
    client_id = connectwiseAPI.client_id
    base_url = connectwiseAPI.base_url

    # Connectwise requires encoding of public key and private to connect since addition of Client_id
    auth_string = f"{company_id}+{public_key}:{private_key}"
    encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    headers = {
        'clientId': client_id,
        'Authorization': f'Basic {encoded_auth_string}',
        'Content-Type': 'application/json'
    }

    product_id = get_product_id_by_vendor_sku(vendor_sku, headers, base_url)
    if product_id:
        patch_product(product_id, new_price, new_cost, headers, base_url)
        
# This function will call the ADI API to get price of product
# Then it will call the connectwise API to update that product in the catalog
def main():
    vendor_sku = 'SK-5230'
    new_price = 200
    new_cost = 100
    
    connectwise_API(vendor_sku, new_price, new_cost)


if __name__ == '__main__':
    main()
