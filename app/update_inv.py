import pandas as pd
import shopify
from model.handle_db import get_ean_inventory
from functions import get_shopify_skus, actualizar_inventario_en_shopify, actualizar_inventario_en_shopify


awsinventory = get_ean_inventory()


sku = get_shopify_skus()
df = pd.DataFrame(sku)
df.columns=['EAN']



def shopifyinv():
    inv = pd.merge(df,
                   awsinventory,
                   on='EAN',
                   how='left')
    inv['INVENTARIO'] = inv['INVENTARIO'].fillna(0)
    inv['INVENTARIO'] = inv['INVENTARIO'].astype(float)
    inv['INVENTARIO'] = inv['INVENTARIO'].astype(int)
    return inv

inventory = shopifyinv()

inventory_dict = inventory.set_index('EAN')['INVENTARIO'].to_dict()


actualizar_inventario_en_shopify(inventory_dict)