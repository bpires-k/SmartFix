CREATE TABLE "Cliente" (
	"NIF"	INTEGER NOT NULL,
	"Nome"	TEXT NOT NULL,
	"Data Nascimento"	TEXT NOT NULL,
	"Sexo"	TEXT NOT NULL,
	"Nr Telemovel"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL,
	PRIMARY KEY("NIF")
);
CREATE TABLE "Estado" (
	"ID"	INTEGER NOT NULL,
	"NomeEstado"	TEXT NOT NULL,
	PRIMARY KEY("ID")
);
CREATE TABLE "Reparacao" (
	"IDReparacao"	INTEGER NOT NULL,
	"NIF"	INTEGER NOT NULL,
	"IDTelemovel"	INTEGER NOT NULL,
	"Obs"	TEXT NOT NULL,
	"DtInicio"	TEXT NOT NULL,
	"DtPrevistaFim"	TEXT NOT NULL,
	"DtFim"	TEXT,
	"ValorPecas"	NUMERIC NOT NULL,
	"ValorReparacao"	NUMERIC NOT NULL,
	PRIMARY KEY("IDReparacao"),
	FOREIGN KEY("IDTelemovel") REFERENCES "Telemovel"("ID"),
	FOREIGN KEY("NIF") REFERENCES "Cliente"("NIF")
);
CREATE TABLE "Telemovel" (
	"ID"	INTEGER NOT NULL,
	"Marca"	TEXT NOT NULL,
	"Modelo"	TEXT NOT NULL,
	"RAM"	TEXT NOT NULL,
	"Disco"	TEXT NOT NULL,
	"Estado"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("Estado") REFERENCES "Estado"("ID")
)