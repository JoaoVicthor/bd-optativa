import pymongo 
client = pymongo.MongoClient()
db = client['vestibular_documento']


def consulta_count_candidatos_questao_x(x = 34):
	str_x = adiciona_zero_a_esquerda(x)
	cursor = db.candidato_questionario.aggregate([{ "$match": {
	    "questionario.q"+str_x+".id_questao": x
	    }
	},
	{ "$group": {
	    "_id": "$questionario.q"+str_x+".resposta_literal"+str_x,
	    "_candidatos": { "$addToSet": "$id_candidato" }, 
    	"questao" : { "$first": "$questionario.q"+str_x+".questao_literal"+str_x }
	    }
	},
	{ "$project": {
	    "_id": 0,
	    "Questão" : "$questao",
	    "Resposta": "$_id",
	    "Total respondido": {"$size": "$_candidatos"}
	    }
	},
	{ "$sort": {
	    "Total respondido": -1
	     }
	}
	])

	result = list(cursor)
	return result

def consulta_candidatos_por_meio_de_transporte(meio_de_transporte = "Outros"):
	cursor = db.candidato_questionario.aggregate([{ "$match": {
    "questionario.q27.id_questao": 27
    , "questionario.q27.resposta_literal27": meio_de_transporte
    }
	},
	{ "$group": {
	    "_id": "$questionario.q27.resposta_literal27", 
	    "Candidatos": { "$addToSet": "$id_candidato" }
	    }
	},
	{ "$sort": {
	     "_id":1
	     }
	}
	])

	return list(cursor)[0]['Candidatos']

def consulta_candidatos_sem_computador_em_casa():
	cursor = db.candidato_questionario.aggregate([{ "$match": {
    "questionario.q25.id_questao": 25
    , "questionario.q25.resposta_literal25": "Não"
    }
	},
	{ "$group": {
	    "_id" : "$questionario.q25.resposta_literal25", 
	    "Candidatos": { "$addToSet": "$id_candidato" }
	    }
	},
	{ "$sort": {
	     "_id":1
	     }
	}])
	# print(list(cursor))
	# raise SystemError(0)
	return list(cursor)[0]['Candidatos']

def consulta_fez_vestibular_duas_vezes():
	cursor = db.candidato_questionario.aggregate([{ "$match": {
    "questionario.q12.id_questao": 12
    , "questionario.q12.resposta_literal12": "Duas"
    }
	},
	{ "$group": {
	    "_id": "$questionario.q12.resposta_literal12", 
	    "Candidatos": { "$addToSet": "$id_candidato" }
	    }
	},
	{ "$sort": {
	     "_id":1
	     }
	}])
	return list(cursor)[0]['Candidatos']

def consulta_possiveis_meios_de_transporte():
	# possiveis respostas: 
	# Bicicleta
	# Carro próprio ou da família
	# Moto
	# Ônibus
	# Outros
	return ['Bicicleta', 'Carro próprio ou da família', 'Moto', 'Ônibus', "Outros"]

def adiciona_zero_a_esquerda(x):
	str_x = str(x)
	if (len(str_x) == 1):
		str_x = "0" + str_x
	return str_x