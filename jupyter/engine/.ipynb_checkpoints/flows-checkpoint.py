FLOWS = {

"curso_por_perfil": {

"start": {
"text": "¿Para quién buscas el curso?",
"options": {
"Niños": "ninos",
"Jóvenes": "jovenes",
"Adultos": "adultos"
}
},

"ninos": {
"text": "¿Qué edad tiene el niño?",
"options": {
"0-5 años": "infants",
"6-15 años": "juniors"
}
},

"infants": {
"text": """
Curso Infants

Precio: $70 semestre
Clases: martes a jueves 3PM
""",
"options": {
"Requisitos": "requisitos",
"Info general": "info"
}
}

}
}