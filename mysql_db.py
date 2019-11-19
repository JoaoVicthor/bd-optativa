import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1234",
  database='vestibular_relacional'
)

cursor = db.cursor()

def consulta_candidatos_lingua():
	cursor.execute("SELECT l.id_lingua AS '#Lingua', l.descricao_lingua AS 'Lingua Estrangeira' \
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_lingua=l.id_lingua AND c2.id_evento=15) AS 'Vestibular 2008'\
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_lingua=l.id_lingua AND c2.id_evento=16) AS 'Vestibular 2009'\
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_lingua=l.id_lingua AND c2.id_evento=20) AS 'Vestibular 2010'\
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_lingua=l.id_lingua AND c2.id_evento=25) AS 'Vestibular 2011'\
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_lingua=l.id_lingua AND c2.id_evento=28) AS 'Vestibular 2012'\
, COUNT(c.id_candidato) AS 'Total Candidatos' FROM lingua l INNER JOIN candidato c ON c.id_lingua=l.id_lingua GROUP BY l.id_lingua")
	columns = cursor.description
	return [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

def consulta_candidatos_estado():
	cursor.execute("SELECT r.nome_regiao AS 'Região', e.nome_UF AS 'Estado' \
, COUNT(c.id_candidato) AS 'Total Candidatos' \
FROM candidato c \
INNER JOIN bairro b ON b.id_bairro=c.id_bairro \
INNER JOIN municipio m ON m.id_municipio=b.id_municipio \
INNER JOIN estado e ON e.id_UF=m.id_UF \
INNER JOIN regiao r ON r.id_regiao=e.id_regiao \
GROUP BY e.id_UF \
ORDER BY r.id_regiao, e.nome_UF")
	columns = cursor.description
	return [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

def consulta_acertos_categoria():
	cursor.execute("SELECT cat.id_categoria AS '#', cat.nome_categoria AS 'Categoria' \
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=15) AS '2008: Candidatos' \
, (SELECT CAST( AVG(c2.acertos_total) AS DECIMAL (4,2) ) FROM candidato c2 \
	WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=15) AS 'Média' \
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=16) AS '2009: Candidatos' \
, (SELECT CAST( AVG(c2.acertos_total) AS DECIMAL (4,2) ) FROM candidato c2 \
	WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=16) AS 'Média' \
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=20) AS '2010: Candidatos' \
, (SELECT CAST( AVG(c2.acertos_total) AS DECIMAL (4,2) ) FROM candidato c2 \
	WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=20) AS 'Média' \
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=25) AS '2011: Candidatos' \
, (SELECT CAST( AVG(c2.acertos_total) AS DECIMAL (4,2) ) FROM candidato c2 \
	WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=25) AS 'Média' \
, (SELECT COUNT(c2.id_candidato) FROM candidato c2 WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=28) AS '2012: Candidatos' \
, (SELECT CAST( AVG(c2.acertos_total) AS DECIMAL (4,2) ) FROM candidato c2 \
	WHERE c2.id_categoria=cat.id_categoria AND c2.id_evento=28) AS 'Média' \
, COUNT(can.id_candidato) AS 'Total Candidatos' \
, CAST( AVG(can.acertos_total) AS DECIMAL (4,2) ) AS 'Média Acertos' \
FROM categoria cat \
INNER JOIN candidato can ON can.id_categoria=cat.id_categoria \
 GROUP BY cat.id_categoria")
	columns = cursor.description
	return [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]