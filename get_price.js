// get_price.js
const axios = require('axios');
const { ADI } = require('./ADIAPI.js');

async function getPrice(vendor_sku, quantity) {
    const url = 'https://api.adiglobal.com/adi/api/v1/PriceAndInventory/PriceAndInventoryDetails';

    // Hardcoded API credentials and signature
    const api_key = ADI.api_key;
    const timestamp = ADI.timestamp;
    const client_request_id = ADI.client_request_id;
    const auth_signature = ADI.auth_signature;
    const customer_number = ADI.customer_number;
    const customer_suffix = ADI.customer_suffix;

    const headers = {
        'Api-Key': api_key,
        'Timestamp': timestamp,
        'Client-Request-Id': client_request_id,
        'Authentication-Signature': auth_signature,
        'Content-Type': 'application/json'
    };
    
    const payload = {
        "CustomerNumber": customer_number,
        "CustomerSuffix": customer_suffix,
        "ItemList": [
            {
                "ItemNumber": vendor_sku,
                "Quantity": quantity
            }
        ]
    };

    try {
        const response = await axios.post(url, payload, { headers: headers });
        if (response.status === 200 && response.data.ItemList.length > 0) {
            console.log(response.data.ItemList[0].ItemPrice);
        } else {
            throw new Error("No items found in the response or unexpected status code");
        }
    } catch (error) {
        console.error(error.message || "Failed to fetch product price");
    }
}

// Get command line arguments
const args = process.argv.slice(2);
if (args.length < 2) {
    console.error('Please provide vendor_sku and quantity');
    process.exit(1);
}

const vendor_sku = args[0];
const quantity = parseInt(args[1], 10);

getPrice(vendor_sku, quantity);
