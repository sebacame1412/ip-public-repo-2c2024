# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport

def getAllImages(input=None):
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = transport.getAllImages(input) #Función getAllImages de la carpeta transport (trae una lista de objetos).

    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    
    for o in json_collection:
        card = translator.fromRequestIntoCard(o) #Convierte los objetos de la variable json_collection en card con la función fromRequestIntoCard de la carpeta translator.
        if card: #Si existe una card.
            images.append(card) #Agrega la card en la lista images.

    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    
    fav = translator.fromTemplateIntoCard(request) # transformamos un request del template en una Card.
    fav.user = request.user # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base de datos.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(user) #buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list: #recorro cada favorito del usuario.
            card = translator.fromRepositoryIntoCard(favourite) # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)   #a cada favorito en formato card lo agrego a la lista mapped_favourites.

        return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.