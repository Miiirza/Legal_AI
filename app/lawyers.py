import json
from fuzzywuzzy import process

lawyers_region = {
    "Albacete": {
        "abogado": {"nombre": "Miguel Ángel Ruiz", "dni": "11112222A", "telefono": "967112233", "direccion": "Calle Mayor, 10, Albacete"},
        "procurador": {"nombre": "Raquel Fernández Soto", "dni": "22223333B", "telefono": "967334455", "direccion": "Avenida de España, 5, Albacete"}
    },
    "Alicante": {
        "abogado": {"nombre": "Sergio López Cano", "dni": "33334444C", "telefono": "965112233", "direccion": "Explanada de España, 15, Alicante"},
        "procurador": {"nombre": "Lorena García Torres", "dni": "44445555D", "telefono": "965556677", "direccion": "Calle San Fernando, 7, Alicante"}
    },
    "Almería": {
        "abogado": {"nombre": "Esteban Muñoz Gil", "dni": "55556666E", "telefono": "950112233", "direccion": "Paseo de Almería, 12, Almería"},
        "procurador": {"nombre": "Clara Domínguez Herrera", "dni": "66667777F", "telefono": "950556677", "direccion": "Calle Real, 9, Almería"}
    },
    "Araba/Álava": {
        "abogado": {"nombre": "Jon Etxebarria Landa", "dni": "77778888G", "telefono": "945112233", "direccion": "Plaza de la Virgen Blanca, 2, Vitoria-Gasteiz"},
        "procurador": {"nombre": "Maite Orozco Mendieta", "dni": "88889999H", "telefono": "945556677", "direccion": "Calle Dato, 3, Vitoria-Gasteiz"}
    },
    "Asturias": {
        "abogado": {"nombre": "Fernando Suárez Álvarez", "dni": "99990000I", "telefono": "984112233", "direccion": "Calle Uría, 14, Oviedo"},
        "procurador": {"nombre": "Isabel Menéndez López", "dni": "00001111J", "telefono": "984556677", "direccion": "Plaza de la Escandalera, 6, Oviedo"}
    },
    "Ávila": {
        "abogado": {"nombre": "Jorge Martín González", "dni": "11112222K", "telefono": "920112233", "direccion": "Plaza del Mercado Chico, 1, Ávila"},
        "procurador": {"nombre": "Patricia Sánchez Rubio", "dni": "22223333L", "telefono": "920556677", "direccion": "Calle San Segundo, 4, Ávila"}
    },
    "Badajoz": {
        "abogado": {"nombre": "Pedro Gómez Morales", "dni": "33335555M", "telefono": "924112233", "direccion": "Calle Menacho, 8, Badajoz"},
        "procurador": {"nombre": "Teresa Castillo Rivas", "dni": "55557777N", "telefono": "924556677", "direccion": "Plaza Alta, 3, Badajoz"}
    },
    "Balears, Illes": {
        "abogado": {"nombre": "Joan Ferrer Puig", "dni": "66669999O", "telefono": "971112233", "direccion": "Paseo Marítimo, 15, Palma de Mallorca"},
        "procurador": {"nombre": "Marta Serra Oliver", "dni": "99991111P", "telefono": "971556677", "direccion": "Calle Sindicat, 9, Palma de Mallorca"}
    },
    "Bizkaia": {
        "abogado": {"nombre": "Iñaki Bilbao Etxeberria", "dni": "11223344Q", "telefono": "944112233", "direccion": "Gran Vía, 20, Bilbao"},
        "procurador": {"nombre": "Nerea Garmendia Zabaleta", "dni": "55667788R", "telefono": "944556677", "direccion": "Calle Hurtado de Amézaga, 5, Bilbao"}
    },
    "Burgos": {
        "abogado": {"nombre": "Alberto Rodríguez Alonso", "dni": "22334455S", "telefono": "947112233", "direccion": "Plaza Mayor, 7, Burgos"},
        "procurador": {"nombre": "Cristina Sanz Martín", "dni": "66778899T", "telefono": "947556677", "direccion": "Calle Vitoria, 12, Burgos"}
    },
    "Cáceres": {
        "abogado": {"nombre": "Luis Moreno Díaz", "dni": "99887766A", "telefono": "927112233", "direccion": "Calle Pintores, 5, Cáceres"},
        "procurador": {"nombre": "Sofía Ramírez Torres", "dni": "11223344B", "telefono": "927556677", "direccion": "Plaza Mayor, 8, Cáceres"}
    },
    "Cádiz": {
        "abogado": {"nombre": "Manuel Ortega Ríos", "dni": "77665544C", "telefono": "956112233", "direccion": "Avenida del Puerto, 3, Cádiz"},
        "procurador": {"nombre": "Elisa Fernández Gómez", "dni": "33445566D", "telefono": "956556677", "direccion": "Plaza de España, 6, Cádiz"}
    },
    "Cantabria": {
        "abogado": {"nombre": "Andrés González Pardo", "dni": "55443322E", "telefono": "942112233", "direccion": "Paseo de Pereda, 12, Santander"},
        "procurador": {"nombre": "Natalia Martín Vega", "dni": "44556677F", "telefono": "942556677", "direccion": "Calle San Fernando, 9, Santander"}
    },
    "Castellón/Castelló": {
        "abogado": {"nombre": "Raúl Doménech Soler", "dni": "22334455G", "telefono": "964112233", "direccion": "Avenida Rey Don Jaime, 15, Castellón"},
        "procurador": {"nombre": "Verónica Ferrer Blasco", "dni": "55667788H", "telefono": "964556677", "direccion": "Calle Mayor, 20, Castellón"}
    },
    "Ciudad Real": {
        "abogado": {"nombre": "Santiago López Roldán", "dni": "11223344I", "telefono": "926112233", "direccion": "Calle Toledo, 11, Ciudad Real"},
        "procurador": {"nombre": "Lucía Gómez Herrera", "dni": "77889900J", "telefono": "926556677", "direccion": "Plaza Mayor, 4, Ciudad Real"}
    },
    "Córdoba": {
        "abogado": {"nombre": "Antonio Márquez Luque", "dni": "88990011K", "telefono": "957112233", "direccion": "Calle Cruz Conde, 6, Córdoba"},
        "procurador": {"nombre": "Silvia Rodríguez Muñoz", "dni": "99001122L", "telefono": "957556677", "direccion": "Plaza de las Tendillas, 2, Córdoba"}
    },
    "Coruña, A": {
        "abogado": {"nombre": "Xoán Fernández Pereira", "dni": "33445566M", "telefono": "981112233", "direccion": "Rúa Real, 9, A Coruña"},
        "procurador": {"nombre": "María Seoane Castro", "dni": "66778899N", "telefono": "981556677", "direccion": "Plaza de María Pita, 5, A Coruña"}
    },
    "Cuenca": {
        "abogado": {"nombre": "Luis Martínez García", "dni": "12345678Z", "telefono": "969123456", "direccion": "Calle del Sol, 8, Cuenca"},
        "procurador": {"nombre": "Ana Sánchez Ruiz", "dni": "87654321X", "telefono": "969654321", "direccion": "Plaza Mayor, 3, Cuenca"}
    },
    "Gipuzkoa": {
        "abogado": {"nombre": "Javier Pérez López", "dni": "23456789Y", "telefono": "943234567", "direccion": "Avenida de la Libertad, 10, Gipuzkoa"},
        "procurador": {"nombre": "Irene González Martín", "dni": "98765432W", "telefono": "943876543", "direccion": "Calle Easo, 12, Gipuzkoa"}
    },
    "Girona": {
        "abogado": {"nombre": "Carlos Romero Martínez", "dni": "34567890V", "telefono": "972345678", "direccion": "Carrer de la Rambla, 5, Girona"},
        "procurador": {"nombre": "Marta Torres Fernández", "dni": "87654321U", "telefono": "972765432", "direccion": "Avinguda de Jaume I, 7, Girona"}
    },
    "Granada": {
        "abogado": {"nombre": "José Ruiz Sánchez", "dni": "45678901T", "telefono": "958456789", "direccion": "Calle de la Reina, 9, Granada"},
        "procurador": {"nombre": "Clara Martín Pérez", "dni": "76543210S", "telefono": "958123456", "direccion": "Plaza de la Constitución, 4, Granada"}
    },
    "Guadalajara": {
        "abogado": {"nombre": "Ricardo López García", "dni": "56789012R", "telefono": "949567890", "direccion": "Calle del Mercado, 11, Guadalajara"},
        "procurador": {"nombre": "Elena Ruiz Gómez", "dni": "65432109Q", "telefono": "949876543", "direccion": "Avenida de Castilla, 15, Guadalajara"}
    },
    "Huelva": {
        "abogado": {"nombre": "Manuel Ortega Pérez", "dni": "67890123P", "telefono": "959678901", "direccion": "Calle Nueva, 13, Huelva"},
        "procurador": {"nombre": "Sofía Díaz Ramírez", "dni": "54321098O", "telefono": "959234567", "direccion": "Plaza de las Monjas, 2, Huelva"}
    },
    "Huesca": {
        "abogado": {"nombre": "Fernando Gómez Sánchez", "dni": "78901234N", "telefono": "974789012", "direccion": "Calle Mayor, 16, Huesca"},
        "procurador": {"nombre": "Pilar García Ruiz", "dni": "43210987M", "telefono": "974123456", "direccion": "Avenida de los Pirineos, 8, Huesca"}
    },
    "Jaén": {
        "abogado": {"nombre": "Antonio Fernández Ruiz", "dni": "89012345L", "telefono": "953890123", "direccion": "Calle del Sol, 4, Jaén"},
        "procurador": {"nombre": "Beatriz Martín Sánchez", "dni": "32109876K", "telefono": "953567890", "direccion": "Plaza de la Paz, 6, Jaén"}
    },
    "León": {
        "abogado": {"nombre": "Ricardo Fernández Álvarez", "dni": "12398765P", "telefono": "987654321",
                    "direccion": "Calle San Martín, 12, León"},
        "procurador": {"nombre": "Laura González García", "dni": "56789012Q", "telefono": "987123456",
                       "direccion": "Plaza Mayor, 3, León"}
    },
    "Lleida": {
        "abogado": {"nombre": "David López Martínez", "dni": "23456789R", "telefono": "973234567",
                    "direccion": "Carrer de Magí Morera, 10, Lleida"},
        "procurador": {"nombre": "Sonia Rodríguez Sánchez", "dni": "87654321S", "telefono": "973876543",
                       "direccion": "Avinguda Catalunya, 5, Lleida"}
    },
    "Lugo": {
        "abogado": {"nombre": "Juan Pérez López", "dni": "34567890T", "telefono": "982345678",
                    "direccion": "Calle de la Cruz, 7, Lugo"},
        "procurador": {"nombre": "Marta Gómez Rodríguez", "dni": "76543210U", "telefono": "982765432",
                       "direccion": "Plaza del Campo, 2, Lugo"}
    },
    "Madrid": {
        "abogado": {"nombre": "Carlos Sánchez Jiménez", "dni": "45678901V", "telefono": "914567890",
                    "direccion": "Calle Gran Vía, 20, Madrid"},
        "procurador": {"nombre": "Elena Torres Pérez", "dni": "65432109W", "telefono": "914123456",
                       "direccion": "Avenida de América, 15, Madrid"}
    },
    "Málaga": {
        "abogado": {"nombre": "José Martín Ruiz", "dni": "56789012X", "telefono": "952678901",
                    "direccion": "Calle Larios, 10, Málaga"},
        "procurador": {"nombre": "Isabel Díaz Fernández", "dni": "54321098Y", "telefono": "952345678",
                       "direccion": "Plaza de la Constitución, 6, Málaga"}
    },
    "Murcia": {
        "abogado": {"nombre": "Antonio Rodríguez Pérez", "dni": "67890123Z", "telefono": "968789012",
                    "direccion": "Calle Mayor, 5, Murcia"},
        "procurador": {"nombre": "Clara Martín Gómez", "dni": "43210987A", "telefono": "968123456",
                       "direccion": "Avenida de la Libertad, 8, Murcia"}
    },
    "Navarra": {
        "abogado": {"nombre": "Marcos García Sánchez", "dni": "78901234B", "telefono": "948567890",
                    "direccion": "Calle Estella, 3, Navarra"},
        "procurador": {"nombre": "Beatriz López Ramírez", "dni": "32109876C", "telefono": "948234567",
                       "direccion": "Avenida Carlos III, 12, Navarra"}
    },
    "Ourense": {
        "abogado": {"nombre": "Fernando Díaz Pérez", "dni": "89012345D", "telefono": "988890123",
                    "direccion": "Calle del Sol, 4, Ourense"},
        "procurador": {"nombre": "Sofía Sánchez Gómez", "dni": "21098765E", "telefono": "988765432",
                       "direccion": "Plaza de la Feria, 7, Ourense"}
    },
    "Palencia": {
        "abogado": {"nombre": "Luis García Martín", "dni": "90123456F", "telefono": "979123456",
                    "direccion": "Calle del Carmen, 6, Palencia"},
        "procurador": {"nombre": "Ana Torres González", "dni": "10987654G", "telefono": "979234567",
                       "direccion": "Plaza Mayor, 8, Palencia"}
    },
    "Las Palmas": {
        "abogado": {"nombre": "Antonio Pérez Morales", "dni": "12345678H", "telefono": "928654321", "direccion": "Calle Triana, 22, Las Palmas"},
        "procurador": {"nombre": "Laura Rodríguez López", "dni": "87654321G", "telefono": "928123456", "direccion": "Plaza de Santa Ana, 5, Las Palmas"}
    },
    "Pontevedra": {
        "abogado": {"nombre": "David García Pérez", "dni": "23456789J", "telefono": "986234567", "direccion": "Calle del Mar, 4, Pontevedra"},
        "procurador": {"nombre": "Marta Fernández Sánchez", "dni": "76543210K", "telefono": "986876543", "direccion": "Rúa do Paseo, 10, Pontevedra"}
    },
    "La Rioja": {
        "abogado": {"nombre": "Carlos Martínez López", "dni": "34567890L", "telefono": "941345678", "direccion": "Calle del Laurel, 18, La Rioja"},
        "procurador": {"nombre": "Isabel Gómez Ruiz", "dni": "65432109M", "telefono": "941765432", "direccion": "Avenida de la Paz, 7, La Rioja"}
    },
    "Salamanca": {
        "abogado": {"nombre": "José Sánchez Rodríguez", "dni": "45678901N", "telefono": "923456789", "direccion": "Calle Mayor, 2, Salamanca"},
        "procurador": {"nombre": "Clara Torres García", "dni": "54321098O", "telefono": "923234567", "direccion": "Plaza Mayor, 14, Salamanca"}
    },
    "Santa Cruz de Tenerife": {
        "abogado": {"nombre": "Marcos Díaz Fernández", "dni": "56789012P", "telefono": "922678901", "direccion": "Avenida de Anaga, 3, Santa Cruz de Tenerife"},
        "procurador": {"nombre": "Beatriz López Martín", "dni": "43210987Q", "telefono": "922345678", "direccion": "Calle del Castillo, 8, Santa Cruz de Tenerife"}
    },
    "Segovia": {
        "abogado": {"nombre": "Luis Fernández González", "dni": "67890123R", "telefono": "921789012", "direccion": "Calle Real, 6, Segovia"},
        "procurador": {"nombre": "Elena Pérez Sánchez", "dni": "32109876S", "telefono": "921234567", "direccion": "Plaza del Azoguejo, 1, Segovia"}
    },
    "Sevilla": {
        "abogado": {"nombre": "Antonio Martín Pérez", "dni": "78901234T", "telefono": "954567890", "direccion": "Calle Tetuán, 12, Sevilla"},
        "procurador": {"nombre": "Sofía Gómez Ramírez", "dni": "21098765U", "telefono": "954234567", "direccion": "Plaza de San Francisco, 3, Sevilla"}
    },
    "Soria": {
        "abogado": {"nombre": "Juan López Jiménez", "dni": "89012345V", "telefono": "975123456", "direccion": "Calle El Collado, 8, Soria"},
        "procurador": {"nombre": "Lucía Rodríguez García", "dni": "10987654W", "telefono": "975234567", "direccion": "Plaza Mayor, 5, Soria"}
    },
    "Tarragona": {
        "abogado": {"nombre": "Javier Sánchez García", "dni": "12345678Z", "telefono": "977654321", "direccion": "Carrer de la Llibertat, 9, Tarragona"},
        "procurador": {"nombre": "María López Fernández", "dni": "87654321Y", "telefono": "977123456", "direccion": "Plaza Imperial Tarraco, 5, Tarragona"}
    },
    "Teruel": {
        "abogado": {"nombre": "Carlos Martínez Pérez", "dni": "23456789X", "telefono": "978234567", "direccion": "Calle del Sol, 4, Teruel"},
        "procurador": {"nombre": "Lucía Gómez Rodríguez", "dni": "76543210W", "telefono": "978876543", "direccion": "Plaza de la Catedral, 7, Teruel"}
    },
    "Toledo": {
        "abogado": {"nombre": "José Fernández Gómez", "dni": "34567890V", "telefono": "925345678", "direccion": "Calle del Alcázar, 10, Toledo"},
        "procurador": {"nombre": "Elena Rodríguez Sánchez", "dni": "65432109U", "telefono": "925234567", "direccion": "Plaza de Zocodover, 3, Toledo"}
    },
    "Valencia/València": {
        "abogado": {"nombre": "Juan López Martínez", "dni": "45678901T", "telefono": "963678901", "direccion": "Carrer de la Pau, 15, València"},
        "procurador": {"nombre": "Clara Pérez Sánchez", "dni": "54321098S", "telefono": "963123456", "direccion": "Avenida del Oeste, 6, València"}
    },
    "Valladolid": {
        "abogado": {"nombre": "Antonio Ruiz Sánchez", "dni": "56789012R", "telefono": "983234567", "direccion": "Calle Duque de la Victoria, 11, Valladolid"},
        "procurador": {"nombre": "Sofía Martín Pérez", "dni": "43210987Q", "telefono": "983876543", "direccion": "Plaza Mayor, 9, Valladolid"}
    },
    "Zamora": {
        "abogado": {"nombre": "Ricardo Gómez Martín", "dni": "67890123P", "telefono": "980789012", "direccion": "Calle de la Feria, 8, Zamora"},
        "procurador": {"nombre": "Ana Torres Fernández", "dni": "32109876N", "telefono": "980234567", "direccion": "Plaza Mayor, 4, Zamora"}
    },
    "Zaragoza": {
        "abogado": {"nombre": "Carlos Martínez Sánchez", "dni": "78901234M", "telefono": "976456789", "direccion": "Calle Coso, 20, Zaragoza"},
        "procurador": {"nombre": "Isabel López Ruiz", "dni": "21098765L", "telefono": "976123456", "direccion": "Plaza del Pilar, 5, Zaragoza"}
    },
    "Ceuta": {
        "abogado": {"nombre": "David Fernández López", "dni": "89012345K", "telefono": "956789012", "direccion": "Calle Real, 3, Ceuta"},
        "procurador": {"nombre": "Marta Gómez Pérez", "dni": "10987654J", "telefono": "956123456", "direccion": "Plaza de África, 8, Ceuta"}
    },
    "Melilla": {
        "abogado": {"nombre": "José Pérez Ramírez", "dni": "90123456H", "telefono": "952234567", "direccion": "Calle de la Marina, 5, Melilla"},
        "procurador": {"nombre": "Lucía Sánchez Díaz", "dni": "10987653G", "telefono": "952876543", "direccion": "Plaza de España, 2, Melilla"}
    }
}

def obtain_lawyer(region:str) -> str:
    true_region, score = process.extractOne(region, lawyers_region.keys())
    print(true_region)
    return json.dumps(lawyers_region[true_region], indent=4)