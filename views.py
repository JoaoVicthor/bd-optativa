from flask import *
import mysql_db

app = Flask(__name__)
app.secret_key = "whatever"

@app.route('/', methods=['GET', 'POST'])
def page_index():
	return render_template("index.html")

@app.route('/candidatos_lingua')
def page_candidatos_lingua():
	return return_template(output = criar_tabela(mysql_db.consulta_candidatos_lingua()))

@app.route('/candidatos_estado')
def page_candidatos_estado():
	return return_template(output = criar_tabela(mysql_db.consulta_candidatos_estado()))

@app.route('/acertos_categoria')
def page_acertos_categoria():
	return render_template("output.html", output = criar_tabela(mysql_db.consulta_acertos_categoria()))

def return_template(output):
	return render_template("output.html", output = output)


def criar_tabela(resultado):
	dict_keys = resultado[0].keys()
	result = "<table><tr>"
	for key in dict_keys:
		result += "<th>" + str(key) +"</th>"
	result += "</tr>"
	for entry in resultado:
		result += "<tr>"
		for key in dict_keys:
			result += "<td>"+ str(entry[key]) +"</td>"
		result += "</tr>"
	result += "</table>"
	return result

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)