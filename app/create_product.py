from model.handle_db import get_model_data
from functions import upload_product_to_shopify, check_product_existence
import shopify

modelo = 'TPHP6458'

data = get_model_data(modelo)

title = data['title']
product_type = data['product_type']
product_vendor = 'Sportsfan'
handle = data['handle']
tags = data['product_type']
options = [{"name": "Talla", "values": []}]
variants = []
print(data['variantes'])
for key in data['variantes']:
    variant_data = data['variantes'][key]
    variant = shopify.Variant({
        'option1': key,
        'price': data['price'],
        'sku': variant_data,
        'inventory_quantity': 0,
        'inventory_management': 'SHOPIFY'
    })
    variants.append(variant)
    

if check_product_existence(modelo):
    print('Producto ya existe')
else:         
    upload_product_to_shopify(title,'', product_type, handle, tags, options, variants)
