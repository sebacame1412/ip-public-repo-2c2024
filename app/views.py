# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()  #Función getAllImages que retorna una lista con las card.
    favourite_list = services.getAllFavourites(request)  #Función getAllFavourites de services. esta función retorna los favs del usuario en formato card.

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images = services.getAllImages(input=search_msg)  #Usa la función getAllImages de la carpeta service usando como parametro la variable search_msg.
        return render(request, 'home.html', {'images': images})
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)  #Traigo la función que retorna la lista de favs del usuario desde services.
    return render(request, 'favourites.html', { 'favourite_list': favourite_list }) #Lo muestro en el templates favourites.html

@login_required
def saveFavourite(request):
   fav = services.saveFavourite(request) #Desde services traigo la función que me permite guardar el personaje en la base de datos. 
   return redirect('home')  #Lo redirigo a la plantilla de home.

@login_required
def deleteFavourite(request):
    delete = services.deleteFavourite(request) #Desde services traigo la función que me permite borrar un favorito por su ID.
    return redirect('/favourites/')  #Lo redirigo a la plantilla de favoritos.

@login_required
def exit(request):
    logout(request)  #Función de Django para cerrar sesion
    return render(request, 'index.html')  #Vuelve al index.html