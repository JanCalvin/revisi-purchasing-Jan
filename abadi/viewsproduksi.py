from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.db.models import Sum
from datetime import datetime
from django.db import IntegrityError

# Create your views here.
# Dashboard Gudang
def view_accgudang(request):
    datatgudang = models.TransaksiGudang.objects.filter(KeteranganACC=False)

    return render(request, "produksi/acc_gudang.html", {"datatgudang": datatgudang})


def acc_gudang(request, id):
    datatgudang = models.TransaksiGudang.objects.get(IDDetailTransaksiGudang=id)
    datatgudang.KeteranganACC = True
    datatgudang.save()

    return redirect("view_accgudang")


# SPK
def view_spk(request):
    dataspk = models.SPK.objects.all()

    return render(request, "produksi/view_spk.html", {"dataspk": dataspk})


def add_spk(request):
    dataartikel = models.Artikel.objects.all()
    if request.method == "GET":
        return render(request, "produksi/add_spk.html",{'data':dataartikel})

    if request.method == "POST":
        nomor_spk = request.POST["nomor_spk"]
        tanggal = request.POST["tanggal"]
        keterangan = request.POST["keterangan"]

        dataspk = models.SPK.objects.filter(NoSPK=nomor_spk).exists()
        if dataspk:
            messages.error(request, "Nomor SPK sudah ada")
            return redirect("add_spk")
        else:
            messages.success(request, "Data berhasil disimpan")
            data_spk = models.SPK(
                NoSPK=nomor_spk,
                Tanggal=tanggal,
                Keterangan=keterangan,
                KeteranganACC=False,
            ).save()

            artikel_list = request.POST.getlist('artikel[]')
            jumlah_list = request.POST.getlist('quantity[]')
            no_spk = models.SPK.objects.get(NoSPK=nomor_spk)

            for produk, jumlah in zip(artikel_list, jumlah_list):
                # Pisahkan KodeArtikel dari jumlah dengan delimiter '/'
                kode_artikel = models.Artikel.objects.get(KodeArtikel=produk)
                jumlah_produk = jumlah
                
                # Simpan data ke dalam model DetailSPK
                datadetailspk = models.DetailSPK(
                    NoSPK=no_spk,
                    KodeArtikel=kode_artikel,
                    Jumlah=jumlah_produk
                )
                datadetailspk.save()
            
            return redirect("view_spk")


def detail_spk(request,id):
    dataartikel = models.Artikel.objects.all()
    dataspk = models.SPK.objects.get(id=id)
    datadetail = models.DetailSPK.objects.filter(NoSPK=dataspk.id)

    if request.method == "GET":
        tanggal = datetime.strftime(dataspk.Tanggal, "%Y-%m-%d")

        return render(request,'produksi/detail_spk.html',{'data':dataartikel,'dataspk':dataspk,'datadetail':datadetail, 'tanggal':tanggal})
    
    elif request.method == 'POST':
        nomor_spk = request.POST["nomor_spk"]
        tanggall = request.POST["tanggal"]
        keterangan = request.POST["keterangan"]
        artikel_list = request.POST.getlist('artikel[]')
        jumlah_list = request.POST.getlist('quantity[]')


        dataspk.NoSPK = nomor_spk
        dataspk.Tanggal = tanggall
        dataspk.Keterangan = keterangan
        dataspk.save()

        for detail, artikel_id, jumlah in zip(datadetail, artikel_list, jumlah_list):
            kode_artikel = models.Artikel.objects.get(KodeArtikel=artikel_id)
            detail.KodeArtikel = kode_artikel
            detail.Jumlah = jumlah
            detail.save()

        no_spk = models.SPK.objects.get(NoSPK=nomor_spk)

        for artikel_id, jumlah in zip(artikel_list[len(datadetail):], jumlah_list[len(datadetail):]):
            kode_artikel = models.Artikel.objects.get(KodeArtikel=artikel_id)
            new_detail = models.DetailSPK.objects.create(
                NoSPK=no_spk,  # Assuming NoSPK is the ForeignKey field to SPK in DetailSPK model
                KodeArtikel=kode_artikel,
                Jumlah=jumlah
            )
            try:
                new_detail.save()
            except IntegrityError:
                # Handle if there's any IntegrityError, such as violating unique constraint
                pass
        
        return redirect('detail_spk', id=id)


def delete_spk(request, id):
    dataspk = models.SPK.objects.get(id=id)
    dataspk.delete()
    return redirect("view_spk")


def delete_detailspk(request, id):
    datadetailspk = models.DetailSPK.objects.get(IDDetailSPK=id)
    dataspk = models.SPK.objects.get(NoSPK=datadetailspk.NoSPK)
    datadetailspk.delete()
    return redirect('detail_spk', id=dataspk.id)

# SPPB
def view_sppb(request):
    datasppb = models.SPPB.objects.all()

    return render(request, "produksi/view_sppb.html", {"datasppb": datasppb})


def add_sppb(request):
    datadetailspk = models.DetailSPK.objects.all()
    if request.method == "GET":
        return render(request, "produksi/add_sppb.html",{'data':datadetailspk})

    if request.method == "POST":
        nomor_sppb = request.POST["nomor_sppb"]
        tanggal = request.POST["tanggal"]
        keterangan = request.POST["keterangan"]

        datasppb = models.SPPB.objects.filter(NoSPPB=nomor_sppb).exists()
        if datasppb:
            messages.error(request, "Nomor SPPB sudah ada")
            return redirect("add_sppb")
        else:
            messages.success(request, "Data berhasil disimpan")
            data_sppb = models.SPPB(
                NoSPPB=nomor_sppb, Tanggal=tanggal, Keterangan=keterangan
            ).save()

            artikel_list = request.POST.getlist('artikel[]')
            jumlah_list = request.POST.getlist('quantity[]')
            no_sppb = models.SPPB.objects.get(NoSPPB=nomor_sppb)

            for artikel, jumlah in zip(artikel_list, jumlah_list):
                # Pisahkan KodeArtikel dari jumlah dengan delimiter '/'
                kode_artikel = models.DetailSPK.objects.get(IDDetailSPK=artikel)
                jumlah_produk = jumlah
                
                # Simpan data ke dalam model DetailSPK
                datadetailspk = models.DetailSPPB(
                    NoSPPB=no_sppb,
                    DetailSPK=kode_artikel,
                    Jumlah=jumlah_produk
                )
                datadetailspk.save()

            return redirect("view_sppb")


def detail_sppb(request,id):
    datadetailspk = models.DetailSPK.objects.all()
    datasppb = models.SPPB.objects.get(id=id)
    datadetailsppb = models.DetailSPPB.objects.filter(NoSPPB=datasppb.id)

    if request.method == "GET":
        tanggal = datetime.strftime(datasppb.Tanggal, "%Y-%m-%d")

        return render(request,'produksi/detail_sppb.html',{'data':datadetailspk,'datasppb':datasppb,'datadetail':datadetailsppb, 'tanggal':tanggal})
    
    elif request.method == 'POST':
        nomor_sppb = request.POST["nomor_sppb"]
        tanggall = request.POST["tanggal"]
        keterangan = request.POST["keterangan"]
        artikel_list = request.POST.getlist('artikel[]')
        jumlah_list = request.POST.getlist('quantity[]')

        datasppb.NoSPPB = nomor_sppb
        datasppb.Tanggal = tanggall
        datasppb.Keterangan = keterangan
        datasppb.save()

        for detail, artikel_id, jumlah in zip(datadetailsppb, artikel_list, jumlah_list):
            kode_artikel = models.DetailSPK.objects.get(IDDetailSPK=artikel_id)
            detail.DetailSPK = kode_artikel
            detail.Jumlah = jumlah
            detail.save()

        no_sppb = models.SPPB.objects.get(NoSPPB=nomor_sppb)

        for artikel_id, jumlah in zip(artikel_list[len(datadetailsppb):], jumlah_list[len(datadetailsppb):]):
            kode_artikel = models.DetailSPK.objects.get(IDDetailSPK=artikel_id)
            new_detail = models.DetailSPPB.objects.create(
                NoSPPB=no_sppb,  # Assuming NoSPK is the ForeignKey field to SPK in DetailSPK model
                DetailSPK=kode_artikel,
                Jumlah=jumlah
            )
            try:
                new_detail.save()
            except IntegrityError:
                # Handle if there's any IntegrityError, such as violating unique constraint
                pass
        
        return redirect('detail_sppb', id=id)


def delete_sppb(request, id):
    datasppb = models.SPPB.objects.get(id=id)
    datasppb.delete()
    return redirect("view_sppb")

def delete_detailsppb(request, id):
    datadetailsppb = models.DetailSPPB.objects.get(IDDetailSPPB=id)
    datasppb = models.SPPB.objects.get(NoSPPB=datadetailsppb.NoSPPB)
    datadetailsppb.delete()
    return redirect('detail_sppb', id=datasppb.id)

# Transaksi Produksi
def view_produksi(request):
    dataproduksi = models.TransaksiProduksi.objects.filter(Jenis="Mutasi")

    return render(
        request, "produksi/view_produksi.html", {"dataproduksi": dataproduksi}
    )


def add_produksi(request):
    if request.method == "GET":
        data_artikel = models.Artikel.objects.all()
        data_lokasi = models.Lokasi.objects.all()

        return render(
            request,
            "produksi/add_produksi.html",
            {"kode_artikel": data_artikel, "nama_lokasi": data_lokasi},
        )

    if request.method == "POST":
        kode_artikel = request.POST["kode_artikel"]
        lokasi = request.POST["nama_lokasi"]
        tanggal = request.POST["tanggal"]
        jumlah = request.POST["jumlah"]
        keterangan = request.POST["keterangan"]

        artikelref = models.Artikel.objects.get(KodeArtikel=kode_artikel)
        lokasiref = models.Lokasi.objects.get(IDLokasi=lokasi)

        data_produksi = models.TransaksiProduksi(
            KodeArtikel=artikelref,
            Lokasi=lokasiref,
            Tanggal=tanggal,
            Jumlah=jumlah,
            Keterangan=keterangan,
            Jenis="Mutasi",
        ).save()
        messages.success(request, "Data berhasil disimpan")

        return redirect("view_produksi")


def update_produksi(request, id):
    produksiobj = models.TransaksiProduksi.objects.get(idTransaksiProduksi=id)
    data_artikel = models.Artikel.objects.all()
    data_lokasi = models.Lokasi.objects.all()
    if request.method == "GET":
        tanggal = datetime.strftime(produksiobj.Tanggal, "%Y-%m-%d")
        return render(
            request,
            "produksi/update_produksi.html",
            {
                "produksi": produksiobj,
                "tanggal": tanggal,
                "kode_artikel": data_artikel,
                "nama_lokasi": data_lokasi,
            },
        )

    elif request.method == "POST":
        kode_artikel = request.POST["kode_artikel"]
        getartikel = models.Artikel.objects.get(KodeArtikel=kode_artikel)
        lokasi = request.POST["nama_lokasi"]
        getlokasi = models.Lokasi.objects.get(IDLokasi=lokasi)
        tanggal = request.POST["tanggal"]
        jumlah = request.POST["jumlah"]
        keterangan = request.POST["keterangan"]

        produksiobj.KodeArtikel = getartikel
        produksiobj.Lokasi = getlokasi
        produksiobj.Tanggal = tanggal
        produksiobj.Jumlah = jumlah
        produksiobj.Keterangan = keterangan
        produksiobj.save()
        messages.success(request, "Data berhasil diupdate")

        return redirect("view_produksi")


def delete_produksi(request, id):
    dataproduksi = models.TransaksiProduksi.objects.get(idTransaksiProduksi=id)
    dataproduksi.delete()
    messages.success(request, "Data Berhasil dihapus")
    return redirect("view_produksi")


# Transaksi Gudang
def view_gudang(request):
    datagudang = models.TransaksiGudang.objects.filter(jumlah__gt=0)

    return render(request, "produksi/view_gudang.html", {"datagudang": datagudang})


def view_gudangretur(request):
    datagudang = models.TransaksiGudang.objects.filter(jumlah__lt=0)
    for data in datagudang:
        jumlah_baru = -data.jumlah
        data.retur = jumlah_baru

    return render(request, "produksi/view_gudangretur.html", {"datagudang": datagudang})


def add_gudang(request):
    if request.method == "GET":
        data_produk = models.Produk.objects.all()
        data_lokasi = models.Lokasi.objects.all()
        data_spk = models.SPK.objects.all()

        return render(
            request,
            "produksi/add_gudang.html",
            {"kode_produk": data_produk, "nama_lokasi": data_lokasi,"data_spk":data_spk},
        )

    if request.method == "POST":
        kode_produk = request.POST["kode_produk"]
        lokasi = request.POST["nama_lokasi"]
        tanggal = request.POST["tanggal"]
        jumlah = request.POST["jumlah"]
        keterangan = request.POST["keterangan"]
        detail_spk = request.POST["detail_spk"]

        produkref = models.Produk.objects.get(KodeProduk=kode_produk)
        lokasiref = models.Lokasi.objects.get(IDLokasi=lokasi)
        detailspkref = models.DetailSPK.objects.get(IDDetailSPK=detail_spk)

        data_gudang = models.TransaksiGudang(
            KodeProduk=produkref,
            Lokasi=lokasiref,
            tanggal=tanggal,
            jumlah=jumlah,
            keterangan=keterangan,
            KeteranganACC=False,
            DetailSPK = detailspkref
        ).save()
        messages.success(request, "Data berhasil disimpan")

        return redirect("view_gudang")


def load_detailspk(request):
    no_spk = request.GET.get('nomor_spk')
    id_spk = models.SPK.objects.get(NoSPK=no_spk)
    detailspk = models.DetailSPK.objects.filter(NoSPK=id_spk.id)

    return render(request, "produksi/opsi_spk.html", {"detailspk":detailspk})


def update_gudang(request, id):
    gudangobj = models.TransaksiGudang.objects.get(IDDetailTransaksiGudang=id)
    data_produk = models.Produk.objects.all()
    data_lokasi = models.Lokasi.objects.all()
    data_spk = models.SPK.objects.all()
    data_detailspk = models.DetailSPK.objects.all()

    if request.method == "GET":
        tanggal = datetime.strftime(gudangobj.tanggal, "%Y-%m-%d")
        return render(
            request,
            "produksi/update_gudang.html",
            {
                "gudang": gudangobj,
                "tanggal": tanggal,
                "kode_produk": data_produk,
                "nama_lokasi": data_lokasi,
                "data_spk":data_spk,
                "data_detailspk":data_detailspk
            },
        )

    elif request.method == "POST":
        kode_produk = request.POST["kode_produk"]
        getproduk = models.Produk.objects.get(KodeProduk=kode_produk)
        lokasi = request.POST["nama_lokasi"]
        getlokasi = models.Lokasi.objects.get(IDLokasi=lokasi)
        tanggal = request.POST["tanggal"]
        jumlah = request.POST["jumlah"]
        keterangan = request.POST["keterangan"]
        detail_spk = request.POST["detail_spk"]

        gudangobj.KodeProduk = getproduk
        gudangobj.Lokasi = getlokasi
        gudangobj.tanggal = tanggal
        gudangobj.jumlah = jumlah
        gudangobj.keterangan = keterangan
        gudangobj.DetailSPK = detail_spk

        gudangobj.save()
        messages.success(request, "Data berhasil diupdate")

        return redirect("view_gudang")


def delete_gudang(request, id):
    datagudang = models.TransaksiGudang.objects.get(IDDetailTransaksiGudang=id)
    datagudang.delete()
    messages.success(request, "Data Berhasil dihapus")

    return redirect("view_gudang")


# Rekapitulasi
def view_ksbb(request):
    if len(request.GET) == 0:
        return render(request, "produksi/view_ksbb.html")
    else:
        try:
            produk = models.Produk.objects.get(KodeProduk=request.GET["kodebarang"])
            nama = produk.NamaProduk
            satuan = produk.unit
        except:
            messages.error(request, "Data Produk tidak ditemukan")
            return redirect('view_ksbb')

        if request.GET['periode']:
            tahun = int(request.GET['periode'])
        else:
            sekarang = datetime.now()
            tahun = sekarang.year
        
        tanggal_mulai = datetime(year=tahun, month=1, day=1)
        tanggal_akhir = datetime(year=tahun, month=12, day=31)

        datagudang = models.TransaksiGudang.objects.filter(KodeProduk=produk,tanggal__range=(tanggal_mulai,tanggal_akhir))

        # Mendapatkan semua penyusun yang terkait dengan produk
        penyusun_produk = models.Penyusun.objects.filter(KodeProduk=produk)

        # Mendapatkan artikel yang terkait dengan penyusun produk
        artikel_penyusun = [penyusun.KodeArtikel for penyusun in penyusun_produk]

        # Memfilter transaksi produksi berdasarkan artikel yang terkait dengan penyusun produk
        dataproduksi = models.TransaksiProduksi.objects.filter(KodeArtikel__in=artikel_penyusun,Jenis="Mutasi",Tanggal__range=(tanggal_mulai,tanggal_akhir)).values('KodeArtikel','Tanggal').annotate(Jumlah=Sum('Jumlah'))

        kuantitas_konversi = {}
        for penyusun in penyusun_produk:
            konversi = models.KonversiMaster.objects.filter(KodePenyusun=penyusun)
            if konversi.exists():
                kuantitas_konversi[penyusun.IDKodePenyusun] = konversi[0].Kuantitas
            else:
                kuantitas_konversi[penyusun.IDKodePenyusun] = 0

        tanggalmasuk = datagudang.values_list("tanggal", flat=True)
        tanggalkeluar = dataproduksi.values_list("Tanggal", flat=True)

        listtanggal = sorted(list(set(tanggalmasuk.union(tanggalkeluar))))

        try:
            saldoawal = models.SaldoAwalBahanBaku.objects.get(IDBahanBaku=request.GET['kodebarang'], IDLokasi=1,Tanggal__range=(tanggal_mulai,tanggal_akhir))
            saldo = saldoawal.Jumlah
        except models.SaldoAwalBahanBaku.DoesNotExist:
            saldo = 0

        sisa = saldo

        data = []
        for i in listtanggal:
            try:
                datamasuk = datagudang.filter(tanggal=i)
                masuk = 0
                for k in datamasuk:
                    masuk += k.jumlah
            except:
                masuk = 0

            detail = []
            try:
                is_first_iteration = True
                datakeluar = dataproduksi.filter(Tanggal=i)
                for keluar in datakeluar:
                    kode_artikel = models.Artikel.objects.filter(id=keluar['KodeArtikel'])
                    for kode in kode_artikel:
                        if kode in artikel_penyusun:
                            konversi = 0
                            penyusun = models.Penyusun.objects.filter(KodeProduk=produk, KodeArtikel=kode)
                            for j in penyusun:
                                konversi += kuantitas_konversi[j.IDKodePenyusun] + (kuantitas_konversi[j.IDKodePenyusun]*2.5/100)

                    jumlah = keluar['Jumlah']
                    fkonversi = round(konversi,6)
                    keluar = jumlah*konversi
                    fkeluar = round(keluar,6)
                    if is_first_iteration:
                        sisa = sisa + masuk - fkeluar
                        is_first_iteration = False
                    else:
                        sisa = sisa - fkeluar
                    
                    fsisa = round(sisa,4)
                            
                    dummy = {
                            "nama" : kode_artikel,
                            "jumlah" : jumlah,
                            "konversi" : fkonversi,
                            "keluar" : fkeluar,
                            "sisa" : fsisa
                        }
                    detail.append(dummy)
            except:
                pass

            if not detail:
                sisa = sisa + masuk
                fsisa = round(sisa,4)
                deta = {
                        "nama" : 0,
                        "jumlah" : 0,
                        "konversi" : 0,
                        "keluar" : 0,
                        "sisa" : fsisa
                    }
                detail.append(deta)
            
            dumy = {
                "tanggal" : i,
                "detail" : detail,
                "masuk" : masuk,
            }
            data.append(dumy)
      
        return render(request, "produksi/view_ksbb.html", {"kodebarang":request.GET['kodebarang'],
                                                  'nama':nama,
                                                  'satuan':satuan,
                                                  'data':data,
                                                  'saldo':saldo,
                                                  'tahun':tahun
                                                  })


def views_ksbj(request):
    if len(request.GET) == 0:
        dataartikel = models.Artikel.objects.all()
        return render(request,'produksi/view_ksbj.html',{'dataartikel' : dataartikel})
    else:   
        print(request.GET)
        lokasi = request.GET['lokasi']
        tahun = request.GET['tahun']
        kodeartikel = request.GET['kodeartikel']
        lokasiobj = models.Lokasi.objects.get(NamaLokasi = lokasi)
        saldoawalobj = models.SaldoAwalArtikel.objects.filter(IDArtikel__KodeArtikel =kodeartikel,IDLokasi=lokasiobj.IDLokasi)

        # Cek apabila Kode Artikel user tidak ada
        try :
            artikel = models.Artikel.objects.get(KodeArtikel = kodeartikel)
        except:
            messages.error(request,"Kode Artikel Tidak ditemukan")
            return redirect('views_ksbj')
        # Cek apabila penyusun utama belum di setting
        try:
            getbahanbakuutama = models.Penyusun.objects.get(KodeArtikel = artikel.id,Status = 1 )
        except models.Penyusun.DoesNotExist:
            messages.error(request,'Bahan Baku utama belum di set')
            return redirect('views_ksbj')

        data = models.TransaksiProduksi.objects.filter(KodeArtikel = artikel.id)
        # if lokasi == "WIP":
        # # print(tanggallist)
        listdata = []


        if lokasi == 'WIP':
            data = data.filter(Lokasi = lokasiobj.IDLokasi)
            try:
                saldoakhirgte = saldoawalobj.filter(Tanggal__year__gt = tahun).order_by('Tanggal').first()
                saldoawallte = saldoawalobj.filter(Tanggal__year__lte = tahun).order_by('-Tanggal').first()
                print('Ini saldo gte : ', saldoakhirgte)
                print('Ini Saldo LTE : ', saldoawallte)
                print('Tahun saat ini : ',tahun)
                print('Saldo Awal Tahun : ',saldoawallte)
                print('Saldo Akhir Tahun : ',saldoakhirgte)
            except:
                saldoawallte = None
                saldoakhirgte = None
            print(saldoawalobj)

            if saldoawallte and saldoakhirgte:
                tanggalawal = saldoawallte.Tanggal
                tanggalakhir = saldoakhirgte.Tanggal
            elif saldoawallte and not saldoakhirgte:
                tanggalawal = saldoawallte.Tanggal
                tanggalakhir = datetime.max
            elif not saldoawallte and saldoakhirgte:
                print('data awal tidak ditemukan')
                tanggalawal = datetime.min
                tanggalakhir = saldoakhirgte.Tanggal
            else :
                print('Tidak ditemukan data awal dan akhir')
                tanggalawal = datetime.min
                tanggalakhir = datetime.max
            
            tanggallist = data.filter(Tanggal__range = (tanggalawal,tanggalakhir)).values_list("Tanggal",flat=True).order_by('Tanggal').distinct()

            saldoawalobj = saldoawallte

            if saldoawalobj:
                saldoawal = saldoawalobj.Jumlah
            else:
                saldoawal = 0
            # print('ini WIP')
            saldoawaltaun = saldoawal
            for i in tanggallist:
                
                jumlahhasil = 0
                jumlahmasuk = 0
                # print(data)
                print(i)
                filtertanggal=data.filter(Tanggal = i)
                print(filtertanggal)
                if filtertanggal:
                    jumlahmasuk = filtertanggal.filter(Jenis = "Produksi").aggregate(total=Sum('Jumlah'))['total']
                    print(jumlahmasuk)
                    if jumlahmasuk is None:
                        jumlahmasuk = 0
                    jumlahhasil = filtertanggal.filter(Jenis = "Mutasi").aggregate(total=Sum('Jumlah'))['total']
                    if jumlahhasil is None:
                        jumlahhasil = 0
                    print(jumlahhasil)


                
                    # Cari data konversi bahan baku utama pada artikel terkait
                
                konversimasterobj = models.KonversiMaster.objects.get(KodePenyusun = getbahanbakuutama.IDKodePenyusun)
                # print('Konversi', konversimasterobj.Kuantitas + ( konversimasterobj.Kuantitas*0.025))
                masukpcs = round(jumlahmasuk/((konversimasterobj.Kuantitas + ( konversimasterobj.Kuantitas*0.025)))*0.893643879)
                    # Cari data penyesuaian
                saldoawal = saldoawal - jumlahhasil +masukpcs
                if saldoawal < 0 :
                    messages.warning(
                    request,
                    "Sisa stok menjadi negatif pada tanggal {}.\nCek kembali mutasi barang".format(
                        i
                    ))
                # listdata.append([i,getbahanbakuutama,jumlahmasuk,jumlahhasil,masukpcs,sisa])
                listdata.append({
                    'Tanggal':i,
                    'Bahanbakuutama':getbahanbakuutama,
                    'Jumlahmasuk':jumlahmasuk,
                    'Jumlahhasil' : jumlahhasil,
                    'Masukpcs' : masukpcs,
                    'Sisa' : saldoawal
                })

            stockopname = 0
            if saldoakhirgte:
                stockopname = saldoakhirgte.Jumlah - saldoawal
            print(saldoakhirgte)

            return render(request,'produksi/view_ksbj.html',{'data':data,"kodeartikel":kodeartikel,"lokasi":lokasi,'listdata':listdata,'saldoawal':saldoawalobj,'tahun':tahun,'stockopname':stockopname,'saldoakhir':saldoakhirgte})
                
                
            #     print(getbahanbakuutama)

        else : 
            data = data.filter(Lokasi = 1)
            saldoawalperiode = saldoawalobj.values_list('Tanggal__year',flat=True).distinct().order_by("-Tanggal")
            print(saldoawalperiode)
            try:
                saldoakhirgte = saldoawalobj.filter(Tanggal__year__gt = tahun).order_by('Tanggal').first()
                saldoawallte = saldoawalobj.filter(Tanggal__year__lte = tahun).order_by('-Tanggal').first()
                print('Ini saldo gte : ', saldoakhirgte)
                print('Ini Saldo LTE : ', saldoawallte)
                print('Tahun saat ini : ',tahun)
                print('Saldo Awal Tahun : ',saldoawallte)
                print('Saldo Akhir Tahun : ',saldoakhirgte)
            except ValueError:
                saldoawallte = None
                saldoakhirgte = None


            # IF Saldo awal LTE kosong --> Data saldoawal belum di set --> Harusnya di set semua pertahun
            if saldoawallte and saldoakhirgte:
                tanggalawal = saldoawallte.Tanggal
                tanggalakhir = saldoakhirgte.Tanggal
            elif saldoawallte and not saldoakhirgte:
                tanggalawal = saldoawallte.Tanggal
                tanggalakhir = datetime.max
            elif not saldoawallte and saldoakhirgte:
                print('data awal tidak ditemukan')
                tanggalawal = datetime.min
                tanggalakhir = saldoakhirgte.Tanggal
            else :
                print('Tidak ditemukan data awal dan akhir')
                tanggalawal = datetime.min
                tanggalakhir = datetime.max
            # IF Saldo Akhir GT kosong --> Data filter data tahun saat ini
            tanggallist = data.filter(Tanggal__range = (tanggalawal,tanggalakhir)).values_list("Tanggal",flat=True).distinct()

            saldoawalobj = saldoawallte

            if saldoawalobj:
                saldoawal = saldoawalobj.Jumlah
            else:
                saldoawal = 0
            sppb = models.DetailSPPB.objects.filter(DetailSPK__KodeArtikel__KodeArtikel = kodeartikel, NoSPPB__Tanggal__range = (tanggalawal,tanggalakhir))
            tanggalsppb = sppb.values_list('NoSPPB__Tanggal',flat=True).distinct()
            # print(tanggalsppb)
            tanggallist = sorted(list(set(tanggallist.union(tanggalsppb))))
            # print(tanggallist)

            # print('ini FG')
            saldoawaltaun = saldoawal
            for i in tanggallist:
                jumlahhasil = 0
                jumlahmasuk = 0
                totalmasuk = 0
                totalkeluar = 0
                nosppb =[]
                nospk = []
                jumlah = []
                listsppbobj = []

                penyerahanwip = models.TransaksiProduksi.objects.filter(Tanggal = i, KodeArtikel__KodeArtikel = kodeartikel,Jenis = "Mutasi",Lokasi__NamaLokasi="WIP")
                detailsppbobj = sppb.filter(NoSPPB__Tanggal = i)
                # print(detailsppbobj)
                if penyerahanwip:
                    # print('data penyerahan ada ',i)
                    totalmasuk=penyerahanwip.aggregate(total=Sum('Jumlah'))['total']
                
                    # print(totalmasuk)
                if detailsppbobj:
                    # print('data Pengiriman Ada',i)
                    totalkeluar = detailsppbobj.aggregate(total=Sum('Jumlah'))['total']
                    # print(totalkeluar)
                    for j in detailsppbobj:
                        nosppb.append(j.NoSPPB)
                        nospk.append(j.DetailSPK.NoSPK)
                        jumlah.append(j.Jumlah)
                saldoawal += totalmasuk-totalkeluar
                if saldoawal < 0 :
                     messages.warning(
                    request,
                    "Sisa stok menjadi negatif pada tanggal {}.\nCek kembali mutasi barang".format(
                        i
                    ),
                )
                # print('Tanggal : ',i)
                # print('Jumlah Penyerahan dari WIP : ',totalmasuk)
                # print('SPPB : ', nosppb)
                # print('SPK : ',nospk)
                # print('Jumlah Kirim : ',jumlah)
                # print('Sisa : ')
                # print('\n')

                listdata.append({
                    'Tanggal' : i,
                    'JumlahPenyerahan' : totalmasuk,
                    'SPPB' : nosppb,
                    'SPK' : nospk,
                    'Jumlahkirim' :jumlah,
                    'Sisa' : saldoawal
                })


            print('ini saldo awal',saldoawalobj)
            # print('saldoakhir ', saldoakhirgte.Jumlah)
            stockopname = 0
            if saldoakhirgte :
                stockopname = saldoakhirgte.Jumlah - saldoawal
                print(stockopname)
            
            return render(request,'produksi/view_ksbj.html',{'data':data,"kodeartikel":kodeartikel,"lokasi":'FG','listdata':listdata,'saldoawal':saldoawalobj,'tahun':tahun,'saldoakhir':saldoakhirgte,'stockopname':stockopname})
    


def view_rekapbarang(request):
    if len(request.GET) == 0:
        return render(request, "produksi/rekap_barang.html")
    else:
        if request.GET['periode']:
            tahun = int(request.GET['periode'])
        else:
            sekarang = datetime.now()
            tahun = sekarang.year
        
        tanggal_mulai = datetime(year=tahun, month=1, day=1)
        tanggal_akhir = datetime(year=tahun, month=12, day=31)

        kode_artikel_produk = (
            models.TransaksiProduksi.objects.filter(
                Jenis="Mutasi", Lokasi=1, Tanggal__range=(tanggal_mulai, tanggal_akhir)
            )
            .values("KodeArtikel")
            .annotate(kuantitas=Sum("Jumlah"))
        )

        # Ambil data penyusun berdasarkan kode artikel yang memiliki transaksi produksi
        penyusun_per_artikel = []
        for kode_artikel in kode_artikel_produk:
            penyusun = models.Penyusun.objects.filter(
                KodeArtikel=kode_artikel["KodeArtikel"]
            )
            konversi = models.KonversiMaster.objects.filter(KodePenyusun__in=penyusun)
            penyusun_per_artikel.append(
                {
                    "KodeArtikel": kode_artikel["KodeArtikel"],
                    "Jumlah": kode_artikel["kuantitas"],
                    "Penyusun": penyusun,
                    "Konversi": konversi,
                }
            )

        # Dictionary untuk menyimpan jumlah total untuk setiap kode produk penyusun
        total_per_produk = {}

        # Output data penyusun per kode artikel
        for item in penyusun_per_artikel:
            for penyusun in item["Penyusun"]:
                konversi = item["Konversi"].filter(KodePenyusun=penyusun)
                total_kuantitas = sum(konv.Kuantitas for konv in konversi) + (sum(konv.Kuantitas for konv in konversi)*2.5/100)
                total = total_kuantitas * item["Jumlah"]
                if penyusun.KodeProduk in total_per_produk:
                    total_per_produk[penyusun.KodeProduk] += total
                else:
                    total_per_produk[penyusun.KodeProduk] = total

        databarang = models.Produk.objects.all()

        datagudang = (
            models.TransaksiGudang.objects.filter(
                Lokasi=1, tanggal__range=(tanggal_mulai, tanggal_akhir)
            )
            .values("KodeProduk")
            .annotate(kuantitas=Sum("jumlah"))
        )

        datagudang = models.TransaksiGudang.objects.filter(Lokasi=1,tanggal__range=(tanggal_mulai,tanggal_akhir)).values('KodeProduk').annotate(kuantitas=Sum('jumlah'))

        # Output hasil perhitungan
        for barang in databarang:
            kode_produk = barang.KodeProduk
            kode = models.Produk.objects.get(KodeProduk=kode_produk)
            try:
                saldoawal = models.SaldoAwalBahanBaku.objects.get(IDBahanBaku=kode, IDLokasi=1,Tanggal__range=(tanggal_mulai,tanggal_akhir))
                saldo = saldoawal.Jumlah
            except models.SaldoAwalBahanBaku.DoesNotExist:
                saldo = 0

            kuantitas = saldo + next((item["kuantitas"] for item in datagudang if item["KodeProduk"] == kode_produk),0,)
            if kode in total_per_produk:
                kuantitas -= total_per_produk[kode]
            barang.kuantitas = round(kuantitas,4)

        return render(request, "produksi/rekap_barang.html", {"databarang": databarang})
