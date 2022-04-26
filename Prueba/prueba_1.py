
#lista = list()

# for dato in range(0,2):
#     if lista:
#         if ['niño'] not in lista:
#             lista.append(['pepe', 3])
#     else:
#         lista.append(['niño',2])
#         print("Esta lista está vacía")

# lista = ["Juan", "Pedro", "Hugo", "Alberto", "Martin"]
# p = 0
# n = 3
# for nom in lista[p:n]:
#     print("Bienvenido " + nom + " me alegro de verte")

# hola = 'RESULTADO "Real Madrid" VS "Villarreal" TEMPORADA <2019-2020>'.strip()
# hola = hola.split()
# cadena = ''
# for i in hola:
#     cadena+= i
# print(hola)


import re
demo = ' RESULTADO "Real Madrid" VS "Villarreal" TEMPORADA 2019-2020>'

demo = re.sub(r"\s*(\W)", "", demo)
# demo = re.sub(r"\s*TEMPORADA\s*", "TEMPORADA", demo)
print(demo)
