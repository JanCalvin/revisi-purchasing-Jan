from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from . import models
from django.db.models import Sum
from datetime import datetime
from django.db.models.functions import ExtractYear

def view_gudang(request) :
    getretur = models.TransaksiGudang.objects.filter(KeteranganACC = False).filter(jumlah__lt=0).order_by('tanggal')
    getkeluar = models.TransaksiGudang.objects.filter(KeteranganACC = False).filter(jumlah__gt=0).order_by('tanggal')
    
    print(getkeluar)
    print(getretur)
    if len(getretur) == 0 :
        messages.info(request, "Tidak ada barang retur yang belum ACC")
    elif len(getkeluar) == 0 :
        messages.info(request, "Tidak ada barang keluar yang belum ACC")
    
    else :
        for a in getretur :
            a.jumlah = a.jumlah*-1
    
    return render(request,"gudang/viewgudang.html", {'getkeluar' : getkeluar, 
                                                   'getretur' : getretur,
                                                   })

def masuk_gudang(request) :
    datasjb = models.DetailSuratJalanPembelian.objects.all().order_by('NoSuratJalan__Tanggal')
    if len(datasjb) == 0 :
        messages.info(request, "Tidak ada barang masuk ke gudang")
    
    return render(request, "gudang/baranggudang.html", {'datasjb' : datasjb})

def add_gudang(request) :
    if request.method == "GET" :
        detailsjp = models.DetailSuratJalanPembelian.objects.all()
        detailsj = models.SuratJalanPembelian.objects.all()
        getproduk = models.Produk.objects.all()

        return render(request, 'gudang/addgudang.html', {
            'detailsjp' : detailsjp,
            'detailsj' : detailsj,
            'getproduk' : getproduk
        })
    if request.method == "POST" :
        print(request.POST)
        kode = request.POST.getlist('kodeproduk')
        # print(kode[1])
        # print(type(request.POST['kodeproduk']))
        nosuratjalan = request.POST["nosuratjalan"]
        tanggal = request.POST['tanggal']
        supplier = request.POST['supplier']
        nomorpo = request.POST['nomorpo']
        if nomorpo == '':
            nomorpo = '-'
        if supplier == '':
            supplier = "-"
        nosuratjalanobj = models.SuratJalanPembelian(
            NoSuratJalan = nosuratjalan,
            Tanggal = tanggal,
            supplier = supplier,
            PO = nomorpo
        )
        nosuratjalanobj.save()
        nosuratjalanobj = models.SuratJalanPembelian.objects.get(NoSuratJalan = nosuratjalan)
        for kodeproduk, jumlah in zip(request.POST.getlist('kodeproduk'), request.POST.getlist('jumlah')):
            # print(kodeproduk)
            newprodukobj = models.DetailSuratJalanPembelian(
                KodeProduk = models.Produk.objects.get(KodeProduk = kodeproduk),
                Jumlah = jumlah,
                KeteranganACC = 0,
                Harga = 0,
                NoSuratJalan = nosuratjalanobj
            )
            newprodukobj.save()
            
        
        return redirect("baranggudang")
    
def add_gudang2(request) :
    if request.method == "GET" :
        detailsjb = models.SuratJalanPembelian.objects.all()
        return render(request, 'gudang/addgudang2.html', {
            'detailsj' : detailsjb
        })
    if request.method == "POST" :
        no_surat = request.POST["no_surat"]
        tanggal = request.POST["Tanggal"]
        supplier = request.POST["supplier"]
        datasjb = models.SuratJalanPembelian(
            NoSuratJalan = no_surat,
            Tanggal = tanggal,
            supplier = supplier,
        ).save()
        return redirect("baranggudang")

def accgudang(request, id) :
    datagudang = models.TransaksiGudang.objects.get(IDDetailTransaksiGudang = id)
    datagudang.KeteranganACC = True
    datagudang.save()
    return redirect("viewgudang")

def update_gudang(request,id) :
    datasjp = models.DetailSuratJalanPembelian.objects.get(IDDetailSJPembelian = id)
    datasjp2 = models.DetailSuratJalanPembelian.objects.all()
    datasj = models.SuratJalanPembelian.objects.all()
    getproduk = models.Produk.objects.all()
    datasjp_getobj = models.SuratJalanPembelian.objects.get(NoSuratJalan = datasjp.NoSuratJalan.NoSuratJalan)
    detailsjp_filtered = models.DetailSuratJalanPembelian.objects.filter(NoSuratJalan =datasjp_getobj.NoSuratJalan)
    if request.method == "GET" :
        # tanggal = datetime.strftime(datasjp.NoSuratJalan.Tanggal, '%Y-%m-%d')  
        # jumlah = datasjp.Jumlah
        # kodeproduk = datasjp.KodeProduk
        # print(kodeproduk)
        # print(getproduk)
        # return render(request, 'gudang/updategudang.html', {
        #     'datasjp' : datasjp,
        #     'datasjp2' : datasjp2,
        #     'datasj' : datasj,
        #     'getproduk' : getproduk,
        #     'kodeproduk' : kodeproduk,
        #     'tanggal' : tanggal,
        #     'jumlah' : jumlah,
        # })
        
        return render(request, 'gudang/updategudang2.html', {
                'datasjp' :datasjp_getobj,
                'detailsjp' :detailsjp_filtered,
                'tanggal' :  datetime.strftime(datasjp_getobj.Tanggal, '%Y-%m-%d')
            })

    else :
        tanggal = request.POST['Tanggal']
        kode_produk = request.POST.get('kode_produk')
        kode_produkobj = models.Produk.objects.get(KodeProduk = kode_produk)
        jumlah = request.POST['jumlah']

        datasjp.KodeProduk = kode_produkobj
        datasjp.Jumlah = jumlah
        datasjp.KeteranganACC = datasjp.KeteranganACC
        datasjp.Harga = datasjp.Harga
        datasjp.NoSuratJalan = datasjp.NoSuratJalan
        datasjp.NoSuratJalan.Tanggal = tanggal
        datasjp.save()
        datasjp.NoSuratJalan.save()


        return redirect('baranggudang')
    

def delete_gudang(request, id) :
    datasbj = models.DetailSuratJalanPembelian.objects.get(IDDetailSJPembelian = id)
    datasbj.delete()
    return redirect("baranggudang")

def rekap_gudang(request) :
    datasjb = models.DetailSuratJalanPembelian.objects.values('KodeProduk','KodeProduk__NamaProduk','KodeProduk__unit','KodeProduk__keterangan').annotate(kuantitas=Sum('Jumlah')).order_by()
    if len(datasjb) == 0 :
        messages.error(request, "Tidak ada barang masuk ke gudang")

    datagudang = models.TransaksiGudang.objects.values('KodeProduk').annotate(kuantitas=Sum('jumlah')).order_by()

    for item in datasjb:
        kode_produk = item['KodeProduk']
        try:
            corresponding_gudang_item = datagudang.get(KodeProduk=kode_produk)
            item['kuantitas'] += corresponding_gudang_item['kuantitas']

            if item['kuantitas'] + corresponding_gudang_item['kuantitas'] < 0 :
                messages.info("Kuantitas gudang menjadi minus")

        except models.TransaksiGudang.DoesNotExist:
            pass
    
    return render(request,'gudang/rekapgudang.html',{
        'datasjb' : datasjb,
    })

    

def detail_barang(request) :
    datagudang = models.TransaksiGudang.objects.all()
    dataproduk = models.Produk.objects.all()
    if len(request.GET) == 0 :
        return render(request, 'gudang/detailbarang.html',{
            'datagudang' : datagudang,
            'dataproduk' : dataproduk,
        })
    
    else :
        dict_semua = []
        list_masuk = []
        list_keluar = []
        list_sisa = []
        input_kode = request.GET.get('input_kode')
        input_tahun = request.GET.get('input_tahun')
        datagudang2 = models.TransaksiGudang.objects.filter(KodeProduk = input_kode).filter(tanggal__year = input_tahun).order_by('tanggal')
        saldo_awal = models.SaldoAwalBahanBaku.objects.filter(IDBahanBaku = input_kode).filter(Tanggal__year = input_tahun).order_by('Tanggal')
        datasjp = models.DetailSuratJalanPembelian.objects.filter(KodeProduk = input_kode).filter(NoSuratJalan__Tanggal__year = input_tahun).order_by('NoSuratJalan__Tanggal')
        tanggalgudang = list(datagudang2.values_list('tanggal', flat = True).distinct())
        tanggalgudang2 = list(datasjp.values_list('NoSuratJalan__Tanggal', flat=True).distinct())
        tanggalgudang3 = list(saldo_awal.values_list('Tanggal', flat=True).distinct())
        
        
        tanggaltotal = tanggalgudang + tanggalgudang2
        tanggaltotal = sorted(list(set(tanggaltotal)))
        if len(tanggaltotal) == 0 :
            messages.error(request, "Tidak ada barang masuk ke gudang, keluar, dan retur")
        
        
        saldo_awal = 0
        data_saldoawal = models.SaldoAwalBahanBaku.objects.filter(IDBahanBaku = input_kode)
        for i in data_saldoawal :
            print(i.Jumlah)
            saldo_awal += i.Jumlah
        
        saldo_dummy = saldo_awal
        for i in tanggaltotal : 
            keluar = 0
            masuk = 0

            data_gudangobj = models.TransaksiGudang.objects.filter(tanggal = i).filter(KodeProduk = input_kode)
            data_sjp = models.DetailSuratJalanPembelian.objects.filter(NoSuratJalan__Tanggal = i).filter(KodeProduk = input_kode)
            data_saldoawal = models.SaldoAwalBahanBaku.objects.filter(Tanggal = i).filter(IDBahanBaku = input_kode)
            
            if len(data_gudangobj) > 0 :
                for j in data_gudangobj :
                    if j.jumlah > 0 :
                        keluar += j.jumlah
                    else :
                        masuk += j.jumlah*-1
            
            if len(data_sjp) > 0 :
                for j in data_sjp :
                    masuk += j.Jumlah
                    

            saldo_dummy += masuk - keluar

            if saldo_dummy + masuk - keluar < 0 :
                messages.warning(
                    request,
                    "Sisa stok menjadi negatif pada tanggal {}.\nCek kembali mutasi barang".format(
                        i
                    ),
                )

            list_keluar.append(keluar)
            list_masuk.append(masuk)
            list_sisa.append(saldo_dummy)


        for tanggal, masuk, keluar, sisa in zip(tanggaltotal, list_masuk, list_keluar, list_sisa) :
            dict_semua.append({'tanggaltotal' : tanggal, 'masuk' : masuk , 'keluar' : keluar, 'sisa' : sisa})
        
        
    
        return render(request, 'gudang/detailbarang.html',{
            'datagudang2' : datagudang2,
            'dataproduk' : dataproduk,
            'list_keluar' : list_keluar,
            'dict_semua' : dict_semua,
            'kodeproduk' : input_kode,
            'saldoawal' : saldo_awal,
            'input_tahun' : input_tahun
        })
    
def barang_keluar(request) :
    datalokasi = models.Lokasi.objects.all()
    datagudang = models.TransaksiGudang.objects.all()
    if len(request.GET) == 0 :
        return render(request, 'gudang/barangkeluar.html', {
            'datalokasi': datalokasi,
            'datagudang': datagudang,
        })
    else:
        date = request.GET.get('mulai')
        date2 = request.GET.get('akhir')
        lok = request.GET.get('lokasi')
        data = datagudang.filter(tanggal__range=(date,date2), Lokasi__NamaLokasi=lok, jumlah__gt=0)
        if len(data) == 0 :
            messages.error(request, "Tidak ada barang masuk ke gudang")
        
        return render(request, 'gudang/barangkeluar.html', {
            'datalokasi': datalokasi,
            'datagudang': datagudang,
            'data': data,
            'date': date,
            'date2':date2,
            'lok':lok
        })

def barang_retur(request) :
    datalokasi = models.Lokasi.objects.all()
    datagudang = models.TransaksiGudang.objects.all()

    if len(request.GET) == 0 :
        return render(request, 'gudang/barangretur.html', {
            'datalokasi': datalokasi,
            'datagudang': datagudang,
        })
    else:
        date = request.GET.get('mulai')
        date2 = request.GET.get('akhir')
        lok = request.GET.get('lokasi')
        data = datagudang.filter(tanggal__range=(date,date2), Lokasi__NamaLokasi=lok, jumlah__lt=0)
        if len(data) == 0 :
            messages.error(request, "Tidak ada barang masuk ke gudang")
        
        for i in data :
            i.jumlah = i.jumlah * -1
        return render(request, 'gudang/barangretur.html', {
            'datalokasi': datalokasi,
            'datagudang': datagudang,
            'data': data,
            'date': date,
            'date2':date2,
            'lok':lok
        })

def accgudang2(request,id,date,date2,lok) :
    datagudang = models.TransaksiGudang.objects.get(IDDetailTransaksiGudang = id)
    datagudang.KeteranganACC = True
    datagudang.save()

    return redirect(f'/gudang/barangretur/?mulai={date}&akhir={date2}&lokasi={lok}')

def accgudang3(request,id,date,date2,lok) :
    datagudang = models.TransaksiGudang.objects.get(IDDetailTransaksiGudang = id)
    datagudang.KeteranganACC = True
    datagudang.save()

    return redirect(f'/gudang/barangkeluar/?mulai={date}&akhir={date2}&lokasi={lok}')
   
# asdasd adasd

def cobaform(request):
    databahanbaku = models.Produk.objects.all()
    if request.method == 'POST':
        print(request.POST)
        nomor_nota = request.POST.get('nomor_nota')
        produk_list = request.POST.getlist('produk[]')
        print(len(produk_list))
        print(produk_list)
        
    return render(request,'gudang/cobaform.html',{'data':databahanbaku})
   