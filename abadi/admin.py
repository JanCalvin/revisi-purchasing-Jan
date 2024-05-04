from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Artikel)
admin.site.register(models.DetailKonversiProduksi)
admin.site.register(models.DetailSPK)
admin.site.register(models.DetailSPPB)
admin.site.register(models.DetailSuratJalanPembelian)
admin.site.register(models.KonversiMaster)
admin.site.register(models.Penyesuaian)
admin.site.register(models.Produk)
admin.site.register(models.SPK)
admin.site.register(models.SPPB)
admin.site.register(models.SuratJalanPembelian)
admin.site.register(models.TransaksiGudang)
admin.site.register(models.TransaksiProduksi)
admin.site.register(models.Penyusun)
admin.site.register(models.Lokasi)
admin.site.register(models.SaldoAwalArtikel)
admin.site.register(models.SaldoAwalBahanBaku)

