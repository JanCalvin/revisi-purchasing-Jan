from django.urls import path
from . import viewspurchasing

urlpatterns = [
    # notif purchasing +spk
    path(
        "notif_purchasing",
        viewspurchasing.notif_barang_purchasing,
        name="notif_purchasing",
    ),
    path(
        "update_verif_purchasing/<str:id>",
        viewspurchasing.verifikasi_data,
        name="update_verif_purchasing",
    ),
    path("acc_spk/<str:id>", viewspurchasing.acc_notif_spk, name="acc_spk"),
    # R penyusun
    path("penyusun", viewspurchasing.views_penyusun, name="penyusun"),
    # CR kebutuhan barang
    path("kebutuhan_barang", viewspurchasing.kebutuhan_barang, name="kebutuhan_barang"),
    # path("kebutuhan_barang/",viewspurchasing.kebutuhan_barang,name="kebutuhan_barang"),
    # barang_masuk
    path("barang_masuk", viewspurchasing.barang_masuk, name="barang_masuk"),
    path(
        "update_barang_masuk/<str:id>",
        viewspurchasing.update_barang_masuk,
        name="update_barang_masuk",
    ),
    # rekap purchasing(gudang+produksi)
    path("rekap_purchasing", viewspurchasing.rekap_purchasing, name="rekap_purchasing"),
    path("rekapgudang2", viewspurchasing.rekap_gudang, name="rekapgudang2"),
    path(
        "viewrekapbarang2", viewspurchasing.view_rekapbarang, name="view_rekapbarang2"
    ),
    # CRUD PRODUK
    path("read_produk", viewspurchasing.read_produk, name="read_produk"),
    path("create_produk", viewspurchasing.create_produk, name="create_produk"),
    path("update_produk/<str:id>", viewspurchasing.update_produk, name="update_produk"),
    path("delete_produk/<str:id>", viewspurchasing.delete_produk, name="delete_produk"),
    # CRUD SPPB
    path("viewsppb2", viewspurchasing.view_sppb, name="view_sppb2"),
    path("addsppb2", viewspurchasing.add_sppb, name="add_sppb2"),
    path("detailsppb2/<str:id>", viewspurchasing.detail_sppb, name="detail_sppb2"),
    path("delete_sppb2/<str:id>", viewspurchasing.delete_sppb, name="delete_sppb2"),
    path(
        "delete_detailsppb2/<str:id>",
        viewspurchasing.delete_detailsppb,
        name="delete_detailsppb2",
    ),
    # R PO
    path("read_po", viewspurchasing.read_po, name="read_po"),
    # R SPK
    path("read_spk", viewspurchasing.read_spk, name="read_spk"),
    path("trackspk/<str:id>",viewspurchasing.track_spk, name="trackspk" ),
    # R REKAP HARGA
    path("rekap_harga", viewspurchasing.views_rekapharga, name="rekapharga"),
]
