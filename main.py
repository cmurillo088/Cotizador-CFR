
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder='templates')

def calcular_cfr(fob, cbm, tarifa_flete, unidades_por_caja, arancel):
    costo_flete_caja = cbm * tarifa_flete
    costo_flete_unidad = costo_flete_caja / unidades_por_caja
    cfr = ((fob + costo_flete_unidad) / 0.92) #8%SAM
    precio_total = cfr + (cfr * (arancel / 100))
    return [
        {"FOB por unidad": round(fob, 4)},
        {"CFR por unidad": round(cfr, 4)},
        {"Precio total puesto en Ecuador": round(precio_total, 4)}
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()
        fob = float(data['fob'])
        cbm = float(data['cbm']) if data['cbm'] else float(data['largo']) * float(data['ancho']) * float(data['alto'])
        tarifa_flete = float(data['tarifa_flete'])
        unidades_por_caja = int(data['unidades_por_caja'])
        arancel = float(data['arancel'])

        resultado = calcular_cfr(fob, cbm, tarifa_flete, unidades_por_caja, arancel)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)})

app.run(host='0.0.0.0', port=8080)
