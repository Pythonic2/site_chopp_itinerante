from django.urls import path
from .views import home,simple_test, CardapioView, logout_view,LoginUsuario,adicionar_ao_carrinho, pagina_carrinho, remover_do_carrinho,obter_quantidade_carrinho_htmx, RegisterUser
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('pag/', simple_test, name='pag'),
    path('cardapio/', CardapioView.as_view(), name='cardapio'),
    path('adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', pagina_carrinho, name='pagina_carrinho'),
    path('remover/<int:produto_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('quantidade-carrinho/', obter_quantidade_carrinho_htmx, name='qtdcar'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
