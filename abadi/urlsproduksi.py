from django.urls import path
from . import viewsproduksi

urlpatterns = [
    path("viewaccgudang", viewsproduksi.view_accgudang, name="view_accgudang"),
    path("accgudang/<str:id>", viewsproduksi.acc_gudang, name="acc_gudang"),

    path("viewspk", viewsproduksi.view_spk, name="view_spk"),
    path("addspk", viewsproduksi.add_spk, name="add_spk"),
    path("detailspk/<str:id>", viewsproduksi.detail_spk, name="detail_spk"),
    path("deletespk/<str:id>", viewsproduksi.delete_spk, name="delete_spk"),
    path("deletedetailspk/<str:id>", viewsproduksi.delete_detailspk, name="delete_detailspk"),
    
    path("viewsppb", viewsproduksi.view_sppb, name="view_sppb"),
    path("addsppb", viewsproduksi.add_sppb, name="add_sppb"),
    path("detailsppb/<str:id>", viewsproduksi.detail_sppb, name="detail_sppb"),
    path("deletesppb/<str:id>", viewsproduksi.delete_sppb, name="delete_sppb"),
    path("deletedetailsppb/<str:id>", viewsproduksi.delete_detailsppb, name="delete_detailsppb"),

    path("viewproduksi", viewsproduksi.view_produksi, name="view_produksi"),
    path("addproduksi", viewsproduksi.add_produksi, name="add_produksi"),
    path("load_detailspk/", viewsproduksi.load_detailspk, name="load_detailspk"),
    path("updateproduksi/<str:id>", viewsproduksi.update_produksi, name="update_produksi"),
    path("deleteproduksi/<str:id>", viewsproduksi.delete_produksi, name="delete_produksi"),

    path("viewgudang", viewsproduksi.view_gudang, name="view_gudang"),
    path("viewgudangretur", viewsproduksi.view_gudangretur, name="view_gudangretur"),
    path("addgudang", viewsproduksi.add_gudang, name="add_gudang"),
    path("updategudang/<str:id>", viewsproduksi.update_gudang, name="update_gudang"),
    path("deletegudang/<str:id>", viewsproduksi.delete_gudang, name="delete_gudang"),

    path('viewksbb',viewsproduksi.view_ksbb,name='view_ksbb'),
    path('viewksbj',viewsproduksi.views_ksbj,name='views_ksbj'),
    path('viewrekapbarang',viewsproduksi.view_rekapbarang,name='view_rekapbarang')
]
