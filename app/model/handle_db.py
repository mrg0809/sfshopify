import mysql.connector
import pandas as pd
from mysql.connector import errorcode


class HandleDB():
    def __init__(self):
        self._con = mysql.connector.connect(user='admin',
                                            password='RMs1stemas',
                                            host='ofandb.ctnnbczca24z.us-east-1.rds.amazonaws.com',
                                            database='ofandb' )
        self._cur = self._con.cursor()

    def get_model_data(self, model):
        self._cur.execute("SELECT Descripcion, Precio, Descuento, Linea, Marca, Subcategoria FROM existencias WHERE Modelo = '{}' LIMIT 1".format(model))
        data = self._cur.fetchall()
        return data
    
    def get_model_variants(self, model):
        self._cur.execute("SELECT Talla, EAN FROM existencias WHERE Modelo = '{}' ORDER BY Talla".format(model))
        variants = self._cur.fetchall()
        return variants
    
    def get_ean_inventory(self):
        self._cur.execute("select EAN, Existencia from ofandb.existencias where Existencia > 2 group by EAN")
        inventory = self._cur.fetchall()
        return inventory

    def __del__(self):
        self._con.close()

db = HandleDB()


def get_model_data(modelo):

    query = db.get_model_data(modelo)
    precio = round(float(query[0][1])*1.16)
    descuento = float(query[0][2])
    precio_tienda = precio
    if descuento > 0:
        precio_tienda = precio*(100-descuento)/100
    variants = db.get_model_variants(modelo)
    unique_variant = dict(variants)
    data = {'title': query[0][0], 'price': precio, 'descuento': round(descuento, 2), 'precio_tienda': round(precio_tienda), 'linea': query[0][3], 'marca': query[0][4], 'product_type' :query[0][5], 'handle':modelo, 'variantes':unique_variant}
    return data

def get_ean_inventory():
    df = pd.DataFrame(db.get_ean_inventory())
    df.columns=['EAN', 'INVENTARIO']
    return df