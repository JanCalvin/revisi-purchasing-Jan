from django.urls import path
from . import viewsgudang

urlpatterns = [
    path("viewgudang", viewsgudang.view_gudang, name="viewgudang"),
    path("accgudang/<str:id>", viewsgudang.accgudang, name='accgudang'),
    path("baranggudang", viewsgudang.masuk_gudang, name='baranggudang'),
    path("updategudang/<str:id>", viewsgudang.update_gudang, name='updategudang'),
    path("deletegudang/<str:id>", viewsgudang.delete_gudang, name='deletegudang'),
    path("addgudang", viewsgudang.add_gudang, name='addgudang'),
    path("addgudang2", viewsgudang.add_gudang2, name='addgudang2'),
    path("detailbarang", viewsgudang.detail_barang, name='detailbarang'),

    path("rekapgudang", viewsgudang.rekap_gudang, name='rekapgudang'),
    path("barangkeluar/", viewsgudang.barang_keluar, name='barangkeluar'),
    path("barangretur/", viewsgudang.barang_retur, name='barangretur'),
    path("accgudang2/<str:id>/<str:date>/<str:date2>/<str:lok>", viewsgudang.accgudang2, name='accgudang2'),
    path("accgudang3/<str:id>/<str:date>/<str:date2>/<str:lok>", viewsgudang.accgudang3, name='accgudang3'),
    path('cobaform',viewsgudang.cobaform,name='coba')
    
]
