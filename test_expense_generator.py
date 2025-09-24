import unittest
import pandas as pd
from datetime import datetime
from expense_generator import SmartExpenseGenerator

class TestSmartExpenseGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = SmartExpenseGenerator()
        self.sample_target = {
            'Belanja Bahan Baku (COGS)': 1000000,
            'Operasional|Gaji Pegawai': 500000,
            'Operasional|Marketing & Promosi': 100000,
            'Operasional|Sewa Tempat (Cadangan)': 200000,
            'Operasional|Maintenance & Perlengkapan': 100000,
            'Operasional|Utilitas': 200000,
            'Operasional|Iuran Lingkungan': 10000,
            'Operasional|Lain-lain': 50000,
            'Operasional|Beban Penyusutan (Depresiasi)': 50000,
            'Tanggal Laporan': '2024-09-30'
        }
        self.start_date = datetime(2024, 9, 1)
        self.end_date = datetime(2024, 9, 30)

    def test_generate_returns_dataframe(self):
        df = self.generator.generate(self.sample_target, self.start_date, self.end_date)
        self.assertIsInstance(df, pd.DataFrame)

    def test_generate_has_required_columns(self):
        df = self.generator.generate(self.sample_target, self.start_date, self.end_date)
        required_columns = ['ID_Transaksi', 'Tanggal_Transaksi', 'Bulan', 'PIC', 'Kategori_Utama', 'Sub_Kategori', 'Keterangan', 'Nominal']
        for col in required_columns:
            self.assertIn(col, df.columns)

    def test_generate_total_matches_target(self):
        df = self.generator.generate(self.sample_target, self.start_date, self.end_date)
        # Check total for COGS (with larger delta due to adjustment)
        cogs_total = df[df['Sub_Kategori'] == 'Belanja Bahan Baku (COGS)']['Nominal'].sum()
        self.assertAlmostEqual(cogs_total, self.sample_target['Belanja Bahan Baku (COGS)'], delta=10000)

    def test_fixed_transactions_generated(self):
        df = self.generator.generate(self.sample_target, self.start_date, self.end_date)
        # Check if gaji is present
        gaji = df[df['Sub_Kategori'] == 'Operasional|Gaji Pegawai']
        self.assertEqual(len(gaji), 1)

if __name__ == '__main__':
    unittest.main()