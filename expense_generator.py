# expense_generator.py
# Modul/Kelas untuk logika generasi data inti

import pandas as pd
import numpy as np
import datetime
import random
import calendar
import logging

# 1. Definisi Data Master untuk Perilaku Natural
#    Struktur ini adalah kunci untuk menghasilkan keterangan yang realistis ("keranjang belanja").
ITEM_MASTER = {
    'BAHAN_BAKU': {
        'susu': {'harga_rata2': 22000, 'std_dev': 7000},
        'gula': {'harga_rata2': 16000, 'std_dev': 4000},
        'kopi': {'harga_rata2': 25000, 'std_dev': 10000},
        'telur': {'harga_rata2': 28000, 'std_dev': 9000},
        'indomie': {'harga_rata2': 3500, 'std_dev': 500},
        'pasar': {'harga_rata2': 175000, 'std_dev': 75000},
        'toko ibu': {'harga_rata2': 150000, 'std_dev': 60000},
        'dampit': {'harga_rata2': 40000, 'std_dev': 15000},
        'roti': {'harga_rata2': 18000, 'std_dev': 5000},
        'es batu': {'harga_rata2': 10000, 'std_dev': 2000},
        'air galon': {'harga_rata2': 7000, 'std_dev': 1000},
    },
    'OPERASIONAL_PENDUKUNG': {
        'lpg': {'harga_rata2': 23000, 'std_dev': 1000},
        'sabun': {'harga_rata2': 15000, 'std_dev': 5000},
        'minyak': {'harga_rata2': 28000, 'std_dev': 8000},
        'tisue': {'harga_rata2': 12000, 'std_dev': 4000},
        'bensin': {'harga_rata2': 15000, 'std_dev': 5000},
    },
    'MAINTENANCE_HABIS_PAKAI': {
        'baterai': {'harga_rata2': 15000, 'std_dev': 5000},
        'pengharum ruangan': {'harga_rata2': 30000, 'std_dev': 10000},
        'pupuk tanaman': {'harga_rata2': 50000, 'std_dev': 15000},  # 1 bulan sekali
        'makanan kucing': {'harga_rata2': 25000, 'std_dev': 5000},  # 1 minggu sekali
        'alat kebersihan': {'harga_rata2': 20000, 'std_dev': 8000},
        'sponge cuci piring': {'harga_rata2': 5000, 'std_dev': 2000},
        'sabun cuci piring': {'harga_rata2': 15000, 'std_dev': 5000},
        'tissue toilet': {'harga_rata2': 20000, 'std_dev': 8000},
        'perbaikan meja / kursi': {'harga_rata2': 40000, 'std_dev': 10000},  # 1 bulan sekali
        'pengadaan gelas pecah': {'harga_rata2': 30000, 'std_dev': 20000},  # setiap bulan, range 10k-50k
    },
    'MAINTENANCE_ALAT': {
        'ember': {'harga_rata2': 35000, 'std_dev': 10000},
        'gagang pel': {'harga_rata2': 40000, 'std_dev': 15000},
        'sapu': {'harga_rata2': 25000, 'std_dev': 8000},
        'perbaikan elektrikal': {'harga_rata2': 65000, 'std_dev': 15000},  # 1 bulan sekali, range 50k-80k
        'perbaikan kecil ruang': {'harga_rata2': 80000, 'std_dev': 30000},  # 1-2 kali bulan
    },
    'LAIN_LAIN': {
        'ATK': {'harga_rata2': 25000, 'std_dev': 10000},
        'fotokopi': {'harga_rata2': 15000, 'std_dev': 5000},
        'biaya tak terduga': {'harga_rata2': 50000, 'std_dev': 25000},
        'bayar pengamen': {'harga_rata2': 1500, 'std_dev': 500},  # nominal kecil 1000-2000
        'sumbangan kecil': {'harga_rata2': 10000, 'std_dev': 5000},
        'pembelian impulsif': {'harga_rata2': 20000, 'std_dev': 10000},
    }
}


class SmartExpenseGenerator:
    """
    Kelas utama yang mengatur seluruh logika generasi data transaksi hibrida.
    """
    def __init__(self):
        self.transactions = []
        self.SENSITIVITY = 0.2  # Konstanta untuk mengontrol agresivitas penyesuaian
        self.transaction_id_counter = 1
        self.logger = logging.getLogger(__name__)
        # Set seed untuk reproducibility
        random.seed(42)
        np.random.seed(42)

    def _get_payment_date(self, year, month, day):
        """Helper untuk menentukan tanggal pembayaran gaji yang jatuh di hari kerja."""
        try:
            dt = datetime.date(year, month, day)
            # Jika Minggu (6), mundur ke Jumat.
            if dt.weekday() == 6:
                return dt - datetime.timedelta(days=2)
            # Jika Sabtu (5), maju ke Senin.
            elif dt.weekday() == 5:
                return dt + datetime.timedelta(days=2)
            return dt
        except ValueError: # Menangani tanggal tidak valid seperti 31 April
            # Jika tanggal tidak valid, gunakan hari kerja terakhir bulan itu
            _, last_day = calendar.monthrange(year, month)
            last_date = datetime.date(year, month, last_day)
            if last_date.weekday() >= 5: # Jika Sabtu atau Minggu
                return last_date - datetime.timedelta(days=(last_date.weekday() - 4))
            return last_date
            
    def _add_transaction(self, date, category, sub_category, nominal, keterangan):
        """Helper untuk menambahkan transaksi ke daftar dan memastikan format konsisten."""
        self.transactions.append({
            'ID_Transaksi': f"TXN{self.transaction_id_counter:04d}",
            'Tanggal_Transaksi': pd.to_datetime(date),
            'Bulan': date.month,
            'PIC': 'SYSTEM',
            'Kategori_Utama': category,
            'Sub_Kategori': sub_category,
            'Keterangan': keterangan,
            'Nominal': float(nominal)
        })
        self.transaction_id_counter += 1

    def _generate_fixed_transactions(self, monthly_target, start_date, end_date):
        """
        Membuat semua transaksi yang jadwal dan aturannya tetap (LOCK ON).
        Mengembalikan dictionary sisa target untuk kategori fleksibel.
        """
        year, month = start_date.year, start_date.month
        
        # Gaji Pegawai
        payment_date = self._get_payment_date(year, month, 10)
        self._add_transaction(payment_date, 'Operasional', 'Operasional|Gaji Pegawai', monthly_target['Operasional|Gaji Pegawai'], f"Gaji Pegawai {start_date.strftime('%B')}")

        # Marketing & Promosi
        promo_date = datetime.date(year, month, random.randint(1, 5))
        self._add_transaction(promo_date, 'Operasional', 'Operasional|Marketing & Promosi', monthly_target['Operasional|Marketing & Promosi'], "Budget Promosi & Pemasaran")
        
        # Sewa Tempat (Cadangan)
        sewa_date = datetime.date(year, month, 1)
        self._add_transaction(sewa_date, 'Operasional', 'Operasional|Sewa Tempat (Cadangan)', monthly_target['Operasional|Sewa Tempat (Cadangan)'], "Alokasi Dana Cadangan Sewa")
        
        # Beban Penyusutan
        depr_date = datetime.date(year, month, random.randint(1, 5))
        self._add_transaction(depr_date, 'Operasional', 'Operasional|Beban Penyusutan (Depresiasi)', monthly_target['Operasional|Beban Penyusutan (Depresiasi)'], "Pencatatan Beban Penyusutan")
        
        # Iuran Lingkungan
        iuran_warga_date = datetime.date(year, month, random.randint(1, 5))
        self._add_transaction(iuran_warga_date, 'Operasional', 'Operasional|Iuran Lingkungan', 80000, "Pembayaran Iuran Warga Bulanan")
        
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == 5: # Sabtu
                self._add_transaction(current_date, 'Operasional', 'Operasional|Iuran Lingkungan', 20000, "Pembayaran Uang Sampah Mingguan")
            current_date += datetime.timedelta(days=1)
            
        # Utilitas (Bagian Tetap)
        wifi_nominal = 425000
        pdam_nominal = random.uniform(500000, 620000)
        
        wifi_date = datetime.date(year, month, random.randint(15, 20))
        pdam_date = datetime.date(year, month, random.randint(15, 20))
        
        self._add_transaction(wifi_date, 'Operasional', 'Operasional|Utilitas', wifi_nominal, "Pembayaran Tagihan WIFI Bulanan")
        self._add_transaction(pdam_date, 'Operasional', 'Operasional|Utilitas', pdam_nominal, "Pembayaran Tagihan Air PDAM")
        
        # Hitung sisa target untuk Listrik
        total_utilitas_target = monthly_target.get('Operasional|Utilitas', 0)
        listrik_target = total_utilitas_target - wifi_nominal - pdam_nominal
        
        # Pastikan tidak negatif
        listrik_target = max(0, listrik_target)

        return {'Utilitas|Listrik': listrik_target}

    def _create_transaction_from_basket(self, item_category_map, base_num_items, adjustment_factor):
        """
        Membuat 'keranjang belanja' dengan jumlah item dan nominal yang dipengaruhi
        oleh adjustment_factor.
        """
        num_items = max(1, round(base_num_items * adjustment_factor))
        
        items_in_basket = []
        total_nominal = 0
        
        for _ in range(num_items):
            # Tentukan kategori item (misal: 85% Bahan Baku, 15% Pendukung)
            chosen_category_type = random.choices(list(item_category_map.keys()), weights=list(item_category_map.values()))[0]
            
            # Pilih item dari kategori tersebut
            item_name = random.choice(list(ITEM_MASTER[chosen_category_type].keys()))
            item_props = ITEM_MASTER[chosen_category_type][item_name]
            
            # Hasilkan harga acak untuk item ini
            item_price = np.random.normal(item_props['harga_rata2'], item_props['std_dev'])
            item_price = max(0, item_price) # Pastikan tidak negatif
            
            items_in_basket.append(item_name)
            total_nominal += item_price

        return "/".join(items_in_basket), round(total_nominal / 100) * 100 # Pembulatan ke 100 terdekat

    def _generate_daily_flexible_transactions(self, flexible_targets, start_date, end_date):
        """
        Loop harian yang membuat transaksi fleksibel dengan panduan mekanisme kontrol.
        """
        actual_spending = {cat: 0.0 for cat in flexible_targets.keys()}
        num_days_in_month = (end_date - start_date).days + 1
        
        current_date = start_date
        while current_date <= end_date:
            day_number = current_date.day
            
            # Hitung adjustment factor untuk setiap kategori
            adjustment_factors = {}
            for category, target in flexible_targets.items():
                target_pro_rata = (target / num_days_in_month) * day_number
                current_actual = actual_spending[category]
                discrepancy = target_pro_rata - current_actual
                adjustment_factors[category] = 1.0 + (discrepancy / (target_pro_rata + 1e-6)) * self.SENSITIVITY
                adjustment_factors[category] = max(0.1, min(2.0, adjustment_factors[category])) # Batasi faktor

            # Generate Transaksi COGS (probabilitas tinggi setiap hari)
            if random.random() < 0.95: # 95% probabilitas ada belanja
                keterangan, nominal = self._create_transaction_from_basket(
                    {'BAHAN_BAKU': 0.85, 'OPERASIONAL_PENDUKUNG': 0.15},
                    base_num_items=random.randint(4, 8),
                    adjustment_factor=adjustment_factors['Belanja Bahan Baku (COGS)']
                )
                if nominal > 0:
                    self._add_transaction(current_date, 'Bahan Baku', 'Belanja Bahan Baku (COGS)', nominal, keterangan)
                    actual_spending['Belanja Bahan Baku (COGS)'] += nominal

            # Generate Transaksi Maintenance (probabilitas 1-2 kali seminggu)
            if random.random() < (2/7):
                keterangan, nominal = self._create_transaction_from_basket(
                    {'MAINTENANCE_HABIS_PAKAI': 0.9, 'MAINTENANCE_ALAT': 0.1},
                    base_num_items=random.randint(1, 2),
                    adjustment_factor=adjustment_factors['Operasional|Maintenance & Perlengkapan']
                )
                if nominal > 0:
                    self._add_transaction(current_date, 'Operasional', 'Operasional|Maintenance & Perlengkapan', nominal, keterangan)
                    actual_spending['Operasional|Maintenance & Perlengkapan'] += nominal

            # Generate Transaksi Listrik (probabilitas 1-2 kali seminggu)
            if random.random() < (2/7):
                base_token_price = random.uniform(50000, 150000)
                nominal = base_token_price * adjustment_factors['Utilitas|Listrik']
                nominal = round(nominal / 1000) * 1000 # Pembulatan ke 1000 terdekat
                if nominal > 0:
                    self._add_transaction(current_date, 'Operasional', 'Operasional|Utilitas', nominal, "Pembelian Token Listrik")
                    actual_spending['Utilitas|Listrik'] += nominal
            
            # Generate Transaksi Lain-lain (probabilitas kecil)
            if random.random() < 0.1:
                 keterangan, nominal = self._create_transaction_from_basket(
                    {'LAIN_LAIN': 1.0},
                    base_num_items=1,
                    adjustment_factor=adjustment_factors['Operasional|Lain-lain']
                )
                 if nominal > 0:
                    self._add_transaction(current_date, 'Operasional', 'Operasional|Lain-lain', nominal, keterangan)
                    actual_spending['Operasional|Lain-lain'] += nominal

            current_date += datetime.timedelta(days=1)

    def _run_final_calibration(self, df, final_targets):
        """Menjalankan kalibrasi akhir untuk memastikan akurasi 100%."""

        for category, target_amount in final_targets.items():
            if category == 'Operasional|Akumulasi Beban Penyusutan' or category.startswith('Tanggal'):
                continue

            actual_amount = df.loc[df['Sub_Kategori'] == category, 'Nominal'].sum()
            discrepancy = target_amount - actual_amount

            if abs(discrepancy) > 1: # Toleransi 1 Rupiah
                category_indices = df.index[df['Sub_Kategori'] == category].tolist()

                if not category_indices:
                    continue

                # Strategi: Tambahkan ke transaksi terbesar
                max_transaction_index = df.loc[category_indices, 'Nominal'].idxmax()
                df.loc[max_transaction_index, 'Nominal'] += discrepancy
                df.loc[max_transaction_index, 'Nominal'] = max(0, df.loc[max_transaction_index, 'Nominal']) # Pastikan tidak negatif

        return df

    def generate(self, monthly_target, start_date, end_date):
        """
        Metode entry point utama untuk memulai proses generasi data.
        """
        try:
            self.logger.info(f"Memulai generasi data untuk periode {start_date} hingga {end_date}")
            # 1. Reset state
            self.transactions = []
            self.transaction_id_counter = 1

            # 2. Proses transaksi tetap dan dapatkan sisa target Utilitas
            sisa_target_utilitas = self._generate_fixed_transactions(monthly_target, start_date, end_date)
            self.logger.info(f"Sisa target utilitas: {sisa_target_utilitas}")

            # 3. Definisikan target untuk kategori fleksibel
            flexible_targets = {
                'Belanja Bahan Baku (COGS)': monthly_target.get('Belanja Bahan Baku (COGS)', 0),
                'Operasional|Maintenance & Perlengkapan': monthly_target.get('Operasional|Maintenance & Perlengkapan', 0),
                'Operasional|Lain-lain': monthly_target.get('Operasional|Lain-lain', 0),
                'Utilitas|Listrik': sisa_target_utilitas['Utilitas|Listrik']
            }
            self.logger.info(f"Target fleksibel: {flexible_targets}")

            # 4. Loop harian untuk generasi transaksi fleksibel
            self._generate_daily_flexible_transactions(flexible_targets, start_date, end_date)

            # 5. Buat DataFrame dari semua transaksi
            if not self.transactions:
                self.logger.warning("Tidak ada transaksi yang dihasilkan")
                return pd.DataFrame() # Kembalikan DF kosong jika tidak ada transaksi

            df_final = pd.DataFrame(self.transactions)
            self.logger.info(f"Jumlah transaksi awal: {len(df_final)}")

            # 6. Jalankan Kalibrasi Final
            #    Kita perlu menggabungkan target Utilitas yang sudah terpecah untuk kalibrasi
            full_target_for_calibration = monthly_target.copy()
            df_calibrated = self._run_final_calibration(df_final, full_target_for_calibration)
            self.logger.info("Kalibrasi final selesai")

            # 7. Bersihkan dan kembalikan DataFrame
            df_calibrated = df_calibrated.sort_values(by='Tanggal_Transaksi').reset_index(drop=True)
            self.logger.info(f"Generasi selesai, total transaksi: {len(df_calibrated)}")
            return df_calibrated
        except Exception as e:
            self.logger.error(f"Error dalam generasi data: {str(e)}")
            raise