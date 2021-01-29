from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'setores', views.SetorViewSet)
router.register(r'cargos', views.CargoViewSet)
router.register(r'premios', views.PremiosViewSet)
router.register(r'transacoes', views.TransacaViewSet)
router.register(r'transacao-premios', views.TransacaoPremiosViewSet)
router.register(r'colaboradores', views.ColaboradorViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('enviar-moedas/', views.send_coins),
    path('listar-doacoes-colaborador/<int:id_colaborador>/', views.lista_doacoes_colaborador),
    path('resgatar-premio/', views.resgatar_premio),
    path('current_user/', views.current_user),
    path('users/', views.UserList.as_view())
]
