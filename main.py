from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()
        fob = float(data['fob'])
        largo = data.get('largo')
        ancho = data.get('ancho')
        alto = data.get('alto')
        cbm = float(data['cbm']) if data['cbm'] else (
            float(largo) * float(ancho) * float(alto) if largo and ancho and alto else 0
        )
        tarifa_flete = float(data['tarifa_flete'])
        unidades_por_caja = int(data['unidades_por_caja']) if data['unidades_por_caja'] else 0
        arancel = float(data['arancel'])

        if cbm > 0 and unidades_por_caja > 0:
            costo_flete_caja = round(cbm * tarifa_flete, 4)
            costo_flete_unidad = round(costo_flete_caja / unidades_por_caja, 6)
            cfr = round((fob + costo_flete_unidad) / 0.92, 4)
        else:
            cfr = round(fob / 0.92, 4)

        precio_total = round(cfr * (1 + arancel / 100) * 1.06, 4)

        resultado = [
            {"FOB por unidad": round(fob, 4)},
            {"CFR por unidad": cfr},
            {"Precio total puesto en Ecuador": precio_total}
        ]
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)