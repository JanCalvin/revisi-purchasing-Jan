from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404,HttpResponse
from django.urls import reverse
from . import models
from django.db.models import Sum
from io import BytesIO
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from datetime import datetime
# Create your views here.

def laporanbarangjadi(request):
    if len(request.GET) == 0:
        return render(request, "ppic/views_laporanstokfg.html")
    else:
        # Rumus = Saldo awal periode sampai tanggal akhir - Keluar awal periode sampai tanggal akhir
        tanggal_mulai = request.GET["tanggalawal"]
        tanggal_akhir = request.GET["tanggalakhir"]
        data = models.Artikel.objects.all()
        grandtotal = 0
        for i in data:
            mutasifilterobj = models.TransaksiProduksi.objects.filter(
                KodeArtikel=i.id
                # Tanggal__range=(tanggal_mulai, tanggal_akhir),
            )
            print(mutasifilterobj)
            saldomutasimasuktanggalakhir = mutasifilterobj.filter(
                Lokasi=1, Tanggal__lte=(tanggal_akhir), Jenis = "Mutasi"
            )
            saldomutasikeluartanggalakhir = mutasifilterobj.filter(
                Lokasi=2, Tanggal__lte=(tanggal_akhir), Jenis = "Mutasi"
            )
            jumlahmasuk = 0
            # jUMLAH kELUAR BELUM SYNC DENGAN MUTASI SPPB
            jumlahkeluar = 0
            for j in saldomutasimasuktanggalakhir:
                jumlahmasuk += j.Jumlah
            for K in saldomutasikeluartanggalakhir:
                jumlahkeluar += K.Jumlah
            i.Jumlahakumulasi = jumlahmasuk - jumlahkeluar 
            print(jumlahmasuk)
            print(jumlahkeluar)
            # Nilai FG --> penyusun artikel * konversi * harga di akumulasikan semua penyusun
            penyusunfilterobj = models.Penyusun.objects.filter(KodeArtikel=i.id)

            nilaiFG = 0
            for penyusunobj in penyusunfilterobj:
                nilaiFG += gethargafg(penyusunobj)
            i.HargaFG = nilaiFG
            i.NilaiTotal = nilaiFG * i.Jumlahakumulasi
            grandtotal +=i.NilaiTotal

        return render(request, "ppic/views_laporanstokfg.html", {"data": data,'tanggalawal':tanggal_mulai,'tanggalakhir':tanggal_akhir,'grandtotal':grandtotal})

def excel_laporanbarangmasuk(request):
    if request.method == "POST" :
        tanggalawal = request.POST['tanggalawal']
        tanggalakhir = request.POST['tanggalakhir']
        dataspk = models.SuratJalanPembelian.objects.filter(
            Tanggal__range=(tanggalawal, tanggalakhir)
        ).order_by("Tanggal")
        # print(dataspk)
        listdetailsjp = []
        grandtotal = 0
        for i in dataspk:
            detailsjpembelianobj = models.DetailSuratJalanPembelian.objects.filter(
                NoSuratJalan=i.NoSuratJalan
            )
            for j in detailsjpembelianobj:
                j.supplier = i.supplier
                j.totalharga = j.Jumlah * j.Harga
                grandtotal += j.totalharga
                listdetailsjp.append(j)

        # print(listdetailsjp)
        listnomor = []
        listsjp =[]
        listsupplier =[]
        listkodeproduk = []
        listnamabarang = []
        listsatuan =[]
        listqty = []
        listhargasatuan = []
        listhargatotal = []
        for no,i in enumerate(listdetailsjp):
            listnomor.append(no)
            listsjp.append(i.NoSuratJalan.NoSuratJalan) 
            listsupplier.append(i.supplier) 
            listkodeproduk.append(i.KodeProduk.KodeProduk)
            listnamabarang.append(i.KodeProduk.NamaProduk)
            listsatuan.append(i.KodeProduk.unit) 
            listqty.append(i.Jumlah)
            listhargasatuan.append(i.Harga)
            listhargatotal.append(i.totalharga)
        tabel = {
            "No":listnomor,
            "SJ Pembelian" : listsjp,
            "Supplier" : listsupplier,
            "Kode Stok" : listkodeproduk,
            "Nama Barang" : listnamabarang,
            "Satuan" : listsatuan,
            'Kuantitas' : listqty,
            'Harga Satuan' : listhargasatuan,
            'Harga Total' : listhargatotal
        }
        df = pd.DataFrame(tabel)
        print(df)

        excel_file = BytesIO()
        # df.to_excel('export data.xlsx',index=False)
        wb = Workbook()
        ws = wb.active
        headers = list(df.columns)
        ws.append(headers)
        for r_idx, row in enumerate(df.itertuples(), start=1):
            for c_idx, value in enumerate(row[1:], start=1):
                ws.cell(row=r_idx+1, column=c_idx, value=value)
        
        start_row = len(df) + 1  # Ganti angka 2 dengan jumlah baris tambahan sebelum merge
        end_row = start_row   # Ganti angka 4 dengan jumlah baris yang ingin digabungkan
        totalhargacell = f'I{end_row}'
        labeltotalhargacell = f'H{end_row}'
        ws[totalhargacell] = grandtotal
        ws[labeltotalhargacell] = "Total Harga"
        excel_buffer = BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        file_name = f"Laporan_{tanggalawal}-{tanggalakhir}.xlsx"
        response = HttpResponse(
    excel_buffer,
    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        # with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        #     df.to_excel(writer, index=False)
        # excel_file.seek(0)
        # response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = f'attachment; filename="Laporan{tanggalawal}-{tanggalakhir}.xlsx"'
                
        return response


def laporanbarangmasuk(request):
    if len(request.GET) == 0:
        return render(request, "ppic/views_laporanbarangmasuk.html")
    else:
        tanggalawal = request.GET["tanggalawal"]
        tanggalakhir = request.GET["tanggalakhir"]

        dataspk = models.SuratJalanPembelian.objects.filter(
            Tanggal__range=(tanggalawal, tanggalakhir)
        ).order_by("Tanggal")
        print(dataspk)
        listdetailsjp = []
        grandtotal = 0
        for i in dataspk:
            detailsjpembelianobj = models.DetailSuratJalanPembelian.objects.filter(
                NoSuratJalan=i.NoSuratJalan
            )
            for j in detailsjpembelianobj:
                j.supplier = i.supplier
                j.totalharga = j.Jumlah * j.Harga
                grandtotal += j.totalharga
                listdetailsjp.append(j)

        print(listdetailsjp)
        return render(
            request,
            "ppic/views_laporanbarangmasuk.html",
            {
                "data": listdetailsjp,
                "tanggalawal": tanggalawal,
                "tanggalakhir": tanggalakhir,
                'grandtotal':grandtotal
            },
        )


def gethargafg(penyusunobj):
    konversiobj = models.KonversiMaster.objects.get(
        KodePenyusun=penyusunobj.IDKodePenyusun
    )
    konversialowance = konversiobj.Kuantitas + (konversiobj.Kuantitas * 0.025)
    detailsjpembelian = models.DetailSuratJalanPembelian.objects.filter(
        KodeProduk=penyusunobj.KodeProduk
    )
    # print("ini detailsjpembelian", detailsjpembelian)
    hargatotalkodeproduk = 0
    jumlahtotalkodeproduk = 0
    for m in detailsjpembelian:
        hargatotalkodeproduk += m.Harga * m.Jumlah
        jumlahtotalkodeproduk += m.Jumlah
    # print("ini jumlah harga total ", hargatotalkodeproduk)
    rataratahargakodeproduk = hargatotalkodeproduk / jumlahtotalkodeproduk
    # print("selesai")
    # print(rataratahargakodeproduk)
    nilaifgperkodeproduk = rataratahargakodeproduk * konversialowance
    # print("Harga Konversi : ", nilaifgperkodeproduk)
    return nilaifgperkodeproduk


def laporanbarangkeluar(request):
    if len(request.GET) == 0:
        return render(request, "ppic/views_laporanbarangkeluar.html")
    else:
        tanggalawal = request.GET["tanggalawal"]
        tanggalakhir = request.GET["tanggalakhir"]
        data = models.SPPB.objects.filter(
            Tanggal__range=(tanggalawal, tanggalakhir)
        ).order_by("Tanggal")
        print('ini data',data)
        listharga = []
        listdata = []
        listkodeartikel = []
        listjumlah = []
        listhargafg = []
        listnilaitotal =[]
        datakirim = []
        if not data.exists():
            messages.warning(request,'Data SPPB tidak ditemukan pada rentang tanggal tersebut')
            return redirect('laporanbarangkeluar')
        for i in data:
            detailsppb = models.DetailSPPB.objects.filter(NoSPPB=i.id)
            a = detailsppb.values("DetailSPK__KodeArtikel").annotate(
                total_jumlah=Sum("Jumlah")
            )
            print("nilai A", a)
            for j in a:
                print(j['DetailSPK__KodeArtikel'])
                kodeartikel = j['DetailSPK__KodeArtikel']
                penyusunfilterobj = models.Penyusun.objects.filter(
                    KodeArtikel=kodeartikel
                )
                if kodeartikel in listkodeartikel:
                    index = listkodeartikel.index(kodeartikel)
                    jumlah = listjumlah[index] + j['total_jumlah']
                    listjumlah[index] = jumlah
                    listnilaitotal[index] = jumlah * listhargafg[index]
                else:
                    listkodeartikel.append(kodeartikel)
                    jumlah = j['total_jumlah']
                    listjumlah.append(jumlah)

                    nilaiFG = 0
                    for penyusunobj in penyusunfilterobj:

                        nilaiFG += gethargafg(penyusunobj)
                    listhargafg.append(nilaiFG)
                    listnilaitotal.append(nilaiFG*jumlah)
            
                        

            listdata.append(a)
        # print(listdata)
        grandtotal = sum(listnilaitotal)
        print('listkodeartikel',listkodeartikel)
        print('listjumlah',listjumlah)
        print('listnilaitotal',listnilaitotal)
        print('listhargafg',listhargafg)

        for kode_artikel, jumlah, nilai_total, harga_fg in zip(listkodeartikel, listjumlah, listnilaitotal, listhargafg):
            artikel = models.Artikel.objects.get(id = kode_artikel)
            datakirim.append({
        'kode_artikel': artikel,
        'jumlah': jumlah,
        'nilai_total': nilai_total,
        'harga_fg': harga_fg
    })

        return render(
            request,
            "ppic/views_laporanbarangkeluar.html",
            {
                "tanggalawal": tanggalawal,
                "tanggalakhir": tanggalakhir,
                "data": datakirim,
                "grandtotal": grandtotal,
                
            },
        )


def laporanpersediaanbarang(request):
    if len(request.GET) == 0:
        return render(request, "ppic/views_laporanpersediaan.html")
    else:
        tanggal_mulai = request.GET["tanggalawal"]
        tanggal_akhir = request.GET["tanggalakhir"]
        tanggal_obj = datetime.strptime(tanggal_akhir, '%Y-%m-%d').date()

        # Ambil total harga barang keluar dulu
        data = models.SPPB.objects.filter(Tanggal__range=(tanggal_mulai,tanggal_akhir)).order_by('Tanggal')
        if  not data.exists():
            messages.warning(request,"Data SPPB Tidak ditemukan pada rentang tanggal tersebut")
            return redirect('laporanpersediaanbarang')
        listharga = []
        for i in data:
            detailsppb = models.DetailSPPB.objects.filter(NoSPPB =i.id)
            a = detailsppb.values('DetailSPK__KodeArtikel').annotate(total_jumlah=Sum("Jumlah"))
            for j in a:
                penyusunfilterobj = models.Penyusun.objects.filter(KodeArtikel = j['DetailSPK__KodeArtikel'])
                nilaiFG = 0
                for penyusunobj in penyusunfilterobj:
                    nilaiFG += gethargafg(penyusunobj)
                j.update({"HargaFG": nilaiFG})
                j.update({"TotalNilai": nilaiFG * j["total_jumlah"]})
                j["DetailSPK__KodeArtikel"] = penyusunobj.KodeArtikel.KodeArtikel
                listharga.append(j["TotalNilai"])
        totalhargabarangkeluar = sum(listharga)

        # Ambil data Bahan masuk
        dataspk = models.SuratJalanPembelian.objects.filter(Tanggal__range=(tanggal_mulai,tanggal_akhir)).order_by("Tanggal")
        listdetailsjp =[]
        totalhargabarangmasuk = 0
        for i in dataspk : 
            detailsjpembelianobj = models.DetailSuratJalanPembelian.objects.filter(NoSuratJalan=i.NoSuratJalan)
            for j in detailsjpembelianobj:
                j.supplier = i.supplier
                j.totalharga = j.Jumlah*j.Harga
                totalhargabarangmasuk += j.totalharga
                listdetailsjp.append(j)

        #Total Harga Stok Gudang
        dataartikel = models.Artikel.objects.all()
        totalhargabarangjadi = 0
        for i in dataartikel:
            mutasifilterobj = models.TransaksiProduksi.objects.filter(KodeArtikel = i.id)
            saldomutasimasuktanggalakhir = mutasifilterobj.filter(Lokasi=1, Tanggal__lte = (tanggal_akhir))
            saldomutasikeluartanggalakhir = mutasifilterobj.filter(Lokasi=2,Tanggal__lte =(tanggal_akhir))
            print(mutasifilterobj)
            jumlahmasuk = 0
            jumlahkeluar = 0
            for j in saldomutasimasuktanggalakhir:
                jumlahmasuk +=j.Jumlah
            for k in saldomutasikeluartanggalakhir:
                jumlahkeluar += k.Jumlah
            
            i.Jumlahakumulasi = jumlahmasuk - jumlahkeluar
            penyusunfilterobj = models.Penyusun.objects.filter(KodeArtikel = i.id)

            nilaiFG = 0
            for penyusunobj in penyusunfilterobj:
                nilaiFG +=gethargafg(penyusunobj)
            i.Harga = nilaiFG
            i.NilaiTotal = nilaiFG * i.Jumlahakumulasi
            totalhargabarangjadi += i.NilaiTotal
        
        # Saldo awal Belum dibuat
        Saldoawal = 0
        # Anggap dari 
        # Ambil data semua bahan baku di wip
        databahanproduksi = models.Produk.objects.filter(KodeProduk__startswith = 'A')
        print(databahanproduksi)
        for i in databahanproduksi:
            print('ini i',i)
            datasaldoawaltahun = models.SaldoAwalBahanBaku.objects.filter(Tanggal__lte = tanggal_akhir,IDBahanBaku = i.KodeProduk).order_by('-Tanggal').first()
            if not datasaldoawaltahun or datasaldoawaltahun.Tanggal.year != tanggal_obj.year:
                print('data tidak ada')
                hargasaldoawalbahanbaku = 0
            else:
                print(datasaldoawaltahun)
                print('data ada')
                hargasaldoawalbahanbaku = datasaldoawaltahun.Harga * datasaldoawaltahun.Jumlah
            
            Saldoawal+=hargasaldoawalbahanbaku

        


        # 
        saldototal = Saldoawal + totalhargabarangmasuk - totalhargabarangkeluar
        saldowip = saldototal -totalhargabarangjadi

        return render(request, "ppic/views_laporanpersediaan.html",{
            "tanggalawal": tanggal_mulai,
            'tanggalakhir':tanggal_akhir,
            'data':a,
            'barangkeluar':round(totalhargabarangkeluar,2),
            'barangmasuk':round(totalhargabarangmasuk,2),
            'barangfg':round(totalhargabarangjadi,2),
            "saldoawal":round(Saldoawal,2),
            "saldototal":round(saldototal,2),
            "saldowip" : round(saldowip,2)})
    
