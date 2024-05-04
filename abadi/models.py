from django.db import models
import datetime

# Create your models here.
class Produk(models.Model):
    KodeProduk = models.CharField(max_length=20, primary_key=True)
    NamaProduk = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    keterangan = models.CharField(max_length=255)
    TanggalPembuatan = models.DateField(auto_now_add = True)
    Jumlahminimal = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.KodeProduk)


class Artikel(models.Model):
    KodeArtikel = models.CharField(max_length=20)
    keterangan = models.CharField(max_length=255)

    def __str__(self):
        return str(self.KodeArtikel)

class ProdukSubkon (models.Model):
    IDProdukSubkon = models.AutoField(primary_key=True)
    NamaProduk = models.CharField(max_length = 255)
    Unit = models.CharField(max_length = 20)
    KodeArtikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.NamaProduk)

class Lokasi(models.Model):
    IDLokasi = models.AutoField(primary_key=True)
    NamaLokasi = models.CharField(max_length=20)

    def __str__(self):
        return str(self.NamaLokasi)


class SuratJalanPembelian(models.Model):
    NoSuratJalan = models.CharField(max_length=255, primary_key=True)
    Tanggal = models.DateField()
    supplier = models.CharField(max_length=255)
    PO = models.CharField(max_length=255)

    def __str__(self):
        return str(str(self.NoSuratJalan))


class DetailSuratJalanPembelian(models.Model):
    IDDetailSJPembelian = models.AutoField(primary_key=True)
    NoSuratJalan = models.ForeignKey(SuratJalanPembelian, on_delete=models.CASCADE)
    KodeProduk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    Jumlah = models.IntegerField()
    KeteranganACC = models.BooleanField()
    Harga = models.FloatField()

    def __str__(self):
        return str(self.NoSuratJalan) + " " + str(self.KodeProduk)

class SPK(models.Model):
    NoSPK = models.CharField(max_length=255)
    Tanggal = models.DateField()
    Keterangan = models.CharField(max_length=255)
    KeteranganACC = models.BooleanField()

    def __str__(self):
        return str(self.NoSPK)


class DetailSPK(models.Model):
    IDDetailSPK = models.AutoField(primary_key=True)
    NoSPK = models.ForeignKey(SPK, on_delete=models.CASCADE)
    KodeArtikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    Jumlah = models.IntegerField()

    def __str__(self):
        return str(self.NoSPK) + " " + str(self.KodeArtikel)

class TransaksiGudang(models.Model):
    IDDetailTransaksiGudang = models.AutoField(primary_key=True)
    KodeProduk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    keterangan = models.CharField(max_length=20)
    jumlah = models.IntegerField()
    tanggal = models.DateField()
    KeteranganACC = models.BooleanField()
    Lokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE)
    DetailSPK = models.ForeignKey(DetailSPK,on_delete = models.CASCADE,null = True,blank=True)


    def __str__(self):
        return str(self.IDDetailTransaksiGudang)


class Penyusun(models.Model):
    IDKodePenyusun = models.AutoField(primary_key=True)
    KodeProduk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    KodeArtikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    Status = models.BooleanField()
    Lokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.KodeArtikel) + " - " + str(self.KodeProduk)


class KonversiMaster(models.Model):
    IDKodeKonversiMaster = models.AutoField(primary_key=True)
    KodePenyusun = models.ForeignKey(Penyusun, on_delete=models.CASCADE)
    Kuantitas = models.FloatField()

    def __str__(self):
        return str(self.KodePenyusun)


class Penyesuaian(models.Model):
    IDPenyesuaian = models.AutoField(primary_key=True)
    KodePenyusun = models.ForeignKey(Penyusun, on_delete=models.CASCADE)
    TanggalMulai = models.DateField()
    TanggalAkhir = models.DateField()

    def __str__(self):
        return str(self.IDPenyesuaian)


class DetailKonversiProduksi(models.Model):
    IDDetailKonversiProduksi = models.AutoField(primary_key=True)
    KodePenyesuaian = models.ForeignKey(Penyesuaian, on_delete=models.CASCADE)
    kuantitas = models.FloatField()

    def __str__(self):
        return str(self.IDDetailKonversiProduksi)




class TransaksiProduksi(models.Model):
    idTransaksiProduksi = models.AutoField(primary_key=True)
    KodeArtikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    Lokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE)
    Tanggal = models.DateField()
    Jumlah = models.IntegerField()
    Keterangan = models.CharField(max_length=255)
    Jenis = models.CharField(max_length=20)
    DetailSPK = models.ForeignKey(DetailSPK,on_delete = models.CASCADE,null = True,blank=True)


    def __str__(self):
        return f'{self.Jenis} - {self.KodeArtikel.KodeArtikel} - {self.Lokasi} - {self.Tanggal} - {self.Jumlah}'


class SPPB(models.Model):
    NoSPPB = models.CharField(max_length=255)
    Tanggal = models.DateField()
    Keterangan = models.CharField(max_length=255)

    def __str__(self):
        return str(self.NoSPPB)


class DetailSPPB(models.Model):
    IDDetailSPPB = models.AutoField(primary_key=True)
    NoSPPB = models.ForeignKey(SPPB, on_delete=models.CASCADE)
    DetailSPK = models.ForeignKey(DetailSPK, on_delete=models.CASCADE, null=True)
    Jumlah = models.IntegerField()

    def __str__(self):
        return f'{self.IDDetailSPPB} - {self.NoSPPB} - {self.DetailSPK} - {self.Jumlah}'

class TransaksiSubkon(models.Model):
    IDTransaksiSubkon = models.AutoField(primary_key=True)
    IDProdukSubkon = models.ForeignKey(ProdukSubkon, on_delete=models.CASCADE)
    Tanggal = models.DateField()
    Jumlah = models.IntegerField()

    def __str__(self):
        return str(self.IDProdukSubkon.NamaProduk) + '-' +str(self.Tanggal)


class SaldoAwalBahanBaku(models.Model):
    IDSaldoAwalBahanBaku = models.AutoField(primary_key=True)
    IDBahanBaku = models.ForeignKey(Produk, on_delete=models.CASCADE)
    IDLokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE)
    Jumlah = models.IntegerField()
    Harga = models.FloatField()
    Tanggal = models.DateField(null=True, blank =True)

    def __str__(self):
        return f'{self.IDLokasi} - {self.IDBahanBaku}- {self.Tanggal.year}'


class SaldoAwalArtikel(models.Model):
    IDSaldoAwalBahanBaku = models.AutoField(primary_key=True)
    IDArtikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    IDLokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE)
    Jumlah = models.IntegerField()
    Tanggal = models.DateField(null=True, blank =True)

    def __str__(self):
        return f"{self.IDLokasi} - {self.IDArtikel} - {self.Tanggal.year}"

class SaldoAwalSubkon(models.Model):
    IDSaldoAwalProdukSubkon = models.AutoField(primary_key=True)
    IDProdukSubkon = models.ForeignKey(ProdukSubkon,on_delete=models.CASCADE)
    Jumlah = models.IntegerField()
    Tanggal = models.DateField()

    def __str__(self):
        return str(self.IDProdukSubkon.NamaProduk)
    
class PemusnahanArtikel (models.Model):
    IDPemusnahanArtikel = models.AutoField(primary_key=True)
    Tanggal = models.DateField()
    KodeArtikel = models.ForeignKey(Artikel,on_delete = models.CASCADE)
    lokasi = models.ForeignKey(Lokasi,on_delete = models.CASCADE)
    Jumlah = models.IntegerField()

    def __str__(self):
        return str(self.KodeArtikel) + '-' + str(self.Tanggal)
    
class PemusnahanBahanBaku (models.Model):
    IDPemusnahanBahanBaku = models.AutoField(primary_key=True)
    Tanggal = models.DateField()
    KodeBahanBaku = models.ForeignKey(Produk,on_delete = models.CASCADE)
    lokasi = models.ForeignKey(Lokasi,on_delete = models.CASCADE)
    Jumlah = models.IntegerField()

    def __str__(self):
        return str(self.KodeBahanBaku) + '-' + str(self.Tanggal)