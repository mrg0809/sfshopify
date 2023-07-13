import requests
import shopify
from dotenv import load_dotenv
import os

#Datos para autenticarse en la API se Shopify
load_dotenv()

shopify.Session.setup(api_key=os.getenv('api_key'), secret=os.getenv('secret'))

shop_url = 'sports-fan-mexico.myshopify.com'
api_version = '2023-04'
private_password = os.getenv('private_password')

session = shopify.Session(shop_url, api_version, os.getenv('private_password'))
shopify.ShopifyResource.activate_session(session)

#Funcion para checar si un producto ya existe
def check_product_existence(handle):
    products = shopify.Product.find(handle=handle)
    return len(products) > 0

#Funcion para dar de alta un articulo nuevo con sus variantes
def upload_product_to_shopify(title, body_html, product_type, handle, tags, options, variants):
    product = shopify.Product()
    product.title = title
    product.body_html = body_html
    product.vendor = 'Sportsfan'
    product.product_type = product_type
    product.handle = handle
    product.tags = tags
    product.options = options
    product.variants = variants

    success = product.save()
    if success:
        print("Producto guardado exitosamente en Shopify")
    else:
        print("Error al guardar el producto en Shopify")

# Funcion para obtener sku de shopify
def get_shopify_skus():
    skus = []

    products = shopify.Product.find()
    while True:
        for product in products:
            for variant in product.variants:
                sku = variant.sku
                skus.append(sku)

        if not products.has_next_page():
            break

        products = products.next_page()
    return skus

# Actualiza el inventario de shopify obteniendo df con sku e inv
def actualizar_inventario_en_shopify(df):
    for index, row in df.iterrows():
        sku = row['EAN']  # SKU y EAN son lo mismo
        
        try:
            # Obtener el producto de Shopify por SKU
            producto = shopify.Product.find(sku)
            print(sku)
            print(producto)
            
            # Obtener la variante del producto
            variante = producto.variants[0]  # Suponiendo que solo hay una variante
            print(variante)
            # Obtener el inventario del DataFrame
            inventario = row['INVENTARIO']
            
            # Actualizar el inventario de la variante
            variante.inventory_quantity = inventario
            variante.save()
            
            print(f"Inventario actualizado en Shopify para SKU: {sku}")
        except Exception as e:
            print(f"Error al actualizar el inventario en Shopify para SKU: {sku}")
            print(f"Error: {str(e)}")


def actualizar_inventario_en_shopify(inventario):
    variantes = shopify.Variant.find()

    for variante in variantes:
        sku = variante.sku
        nuevo_inventario = inventario[sku]

        variante.inventory_quantity = nuevo_inventario
        variante.save()

    print("Inventario actualizado en Shopify de forma masiva.")

