from django.urls import path
from . import viewsppic

urlpatterns = [
    path("laporanstokfg", viewsppic.laporanbarangjadi, name="laporanstokfg"),
    path("laporanbarangmasuk", viewsppic.laporanbarangmasuk, name="laporanbarangmasuk"),
    path('laporanbarangmasukexcel',viewsppic.excel_laporanbarangmasuk,name='laporanbarangmasukexcel'),
    path("laporanbarangkeluar", viewsppic.laporanbarangkeluar, name="laporanbarangkeluar"),
    path("laporanpersediaanbarang",viewsppic.laporanpersediaanbarang,name="laporanpersediaanbarang"),
]