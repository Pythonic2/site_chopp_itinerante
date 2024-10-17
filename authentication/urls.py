from django.urls import path
from .views import logout_view,LoginUsuario,RegisterUser,EventoView, PedidosView,adicionar_ao_carrinho, pagina_carrinho, remover_do_carrinho,obter_quantidade_carrinho_htmx
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastrar-evento/', EventoView.as_view(), name='cad-evento'),
    path('minhas-compras/', PedidosView.as_view(), name='minhas_compras'),
    path('adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', pagina_carrinho, name='pagina_carrinho'),
    path('remover/<int:produto_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('quantidade-carrinho/', obter_quantidade_carrinho_htmx, name='qtdcar'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)