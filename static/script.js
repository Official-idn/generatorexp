// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    // --- Referensi Elemen DOM ---
    const yearSelect = document.getElementById('yearSelect');
    const monthSelect = document.getElementById('monthSelect');
    const getTargetBtn = document.getElementById('getTargetBtn');
    const generateBtn = document.getElementById('generateBtn');
    const loader = document.getElementById('loader');
    const errorContainer = document.getElementById('errorContainer');
    const targetContainer = document.getElementById('targetContainer');
    const transactionsContainer = document.getElementById('transactionsContainer');
    const summaryContainer = document.getElementById('summaryContainer');
    const csvButtons = document.getElementById('csvButtons');
    const copyCsvBtn = document.getElementById('copyCsvBtn');
    const downloadCsvBtn = document.getElementById('downloadCsvBtn');
    const notification = document.getElementById('notification');

    // --- State Aplikasi ---
    let currentTargetData = null;
    let currentTransactionsData = null;

    // --- Fungsi Helper ---
    const showLoader = (show) => {
        loader.classList.toggle('hidden', !show);
    };

    const showError = (message) => {
        errorContainer.textContent = message;
        errorContainer.classList.remove('hidden');
    };

    const hideError = () => {
        errorContainer.classList.add('hidden');
    };

    const formatCurrency = (number) => {
        return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(number);
    };

    const convertToCSV = (data) => {
        if (!data || data.length === 0) return '';
        const headers = Object.keys(data[0]);
        const csvRows = [];
        csvRows.push(headers.join(','));
        data.forEach(row => {
            const values = headers.map(header => {
                let value = row[header];
                if (typeof value === 'string' && value.includes(',')) {
                    value = `"${value}"`;
                }
                return value;
            });
            csvRows.push(values.join(','));
        });
        return csvRows.join('\n');
    };

    const copyToClipboard = async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            console.error('Failed to copy: ', err);
            return false;
        }
    };

    const downloadCSV = (csvContent, filename) => {
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const showNotification = (message) => {
        notification.textContent = message;
        notification.classList.remove('hidden');
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 3000);
    };
    
    // Fungsi utama untuk merender tabel dari data JSON
    const renderTable = (container, data, title, isTargetTable = false) => {
        container.innerHTML = `<h2>${title}</h2>`;
        if (!data || data.length === 0) {
            container.innerHTML += '<p>Tidak ada data untuk ditampilkan.</p>';
            return;
        }

        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        const headerRow = document.createElement('tr');

        // Dapatkan header dari objek pertama
        const headers = Object.keys(data[0]);
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText.replace(/_/g, ' ').replace(/\|/g, ' - ');
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);

        // Isi baris data
        data.forEach(rowData => {
            const row = document.createElement('tr');
            headers.forEach(header => {
                const cell = document.createElement('td');
                let cellValue = rowData[header];
                if (typeof cellValue === 'number' && header.toLowerCase() !== 'bulan' && header.toLowerCase() !== 'tahun') {
                    cell.textContent = formatCurrency(cellValue);
                } else {
                    cell.textContent = cellValue;
                }
                row.appendChild(cell);
            });
            tbody.appendChild(row);
        });

        table.appendChild(thead);
        table.appendChild(tbody);
        container.appendChild(table);
    };

    // Fungsi untuk merender tabel target (format khusus)
    const renderTargetTable = (container, data) => {
        container.innerHTML = '<h2>Ringkasan Target</h2>';
        const tableData = Object.entries(data)
            .filter(([key, _]) => key !== 'Bulan' && key !== 'Tahun' && key !== 'Tanggal Laporan' && key !== 'Operasional|Akumulasi Beban Penyusutan')
            .map(([key, value]) => ({ Kategori: key.replace(/\|/g, ' - '), Nominal: value }));
        
        const total = tableData.reduce((sum, item) => sum + item.Nominal, 0);
        tableData.push({ Kategori: '<strong>TOTAL TARGET</strong>', Nominal: `<strong>${formatCurrency(total)}</strong>` });

        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr><th>Kategori</th><th>Nominal</th></tr>
            </thead>
            <tbody>
                ${tableData.map(item => `<tr><td>${item.Kategori}</td><td>${typeof item.Nominal === 'number' ? formatCurrency(item.Nominal) : item.Nominal}</td></tr>`).join('')}
            </tbody>
        `;
        container.appendChild(table);
    };

    const renderSummaryTable = (target, actual) => {
        summaryContainer.innerHTML = '<h2>Verifikasi: Target vs. Aktual</h2>';
        const summaryData = [];
        let totalTarget = 0;
        let totalActual = 0;

        for (const key in target) {
            if (key !== 'Bulan' && key !== 'Tahun' && key !== 'Tanggal Laporan' && key !== 'Operasional|Akumulasi Beban Penyusutan') {
                const targetAmount = target[key];
                const actualAmount = actual.filter(item => item.Sub_Kategori === key).reduce((sum, item) => sum + item.Nominal, 0);
                const deviation = actualAmount - targetAmount;

                summaryData.push({
                    Kategori: key.replace(/\|/g, ' - '),
                    Target: formatCurrency(targetAmount),
                    Aktual: formatCurrency(actualAmount),
                    Deviasi: formatCurrency(deviation)
                });
                totalTarget += targetAmount;
                totalActual += actualAmount;
            }
        }

        // Baris Total
        summaryData.push({
            Kategori: '<strong>TOTAL</strong>',
            Target: `<strong>${formatCurrency(totalTarget)}</strong>`,
            Aktual: `<strong>${formatCurrency(totalActual)}</strong>`,
            Deviasi: `<strong>${formatCurrency(totalActual - totalTarget)}</strong>`
        });

        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr><th>Kategori</th><th>Target</th><th>Aktual</th><th>Deviasi</th></tr>
            </thead>
            <tbody>
                ${summaryData.map(item => `
                    <tr>
                        <td>${item.Kategori}</td>
                        <td>${item.Target}</td>
                        <td>${item.Aktual}</td>
                        <td style="color: ${Math.abs(parseFloat(item.Deviasi.replace(/[^0-9-]/g, ''))) < 1 ? 'green' : 'red'};">${item.Deviasi}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        summaryContainer.appendChild(table);
    };

    // --- Event Listeners ---
    getTargetBtn.addEventListener('click', async () => {
        hideError();
        showLoader(true);
        generateBtn.disabled = true;
        targetContainer.innerHTML = '';
        transactionsContainer.innerHTML = '';
        summaryContainer.innerHTML = '';

        try {
            const response = await fetch('/get-target', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    year: parseInt(yearSelect.value),
                    month: parseInt(monthSelect.value)
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Gagal mengambil data target.');
            }

            const data = await response.json();
            currentTargetData = data;
            renderTargetTable(targetContainer, currentTargetData);
            generateBtn.disabled = false;

        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                showError('Tidak dapat terhubung ke server. Pastikan server berjalan.');
            } else {
                showError(error.message);
            }
        } finally {
            showLoader(false);
        }
    });

    generateBtn.addEventListener('click', async () => {
        if (!currentTargetData) {
            showError("Silakan tampilkan target terlebih dahulu.");
            return;
        }
        hideError();
        showLoader(true);
        transactionsContainer.innerHTML = '';
        summaryContainer.innerHTML = '';

        try {
            const response = await fetch('/generate-data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentTargetData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Gagal menghasilkan data transaksi.');
            }

            const data = await response.json();
            currentTransactionsData = data;
            renderSummaryTable(currentTargetData, data);
            renderTable(transactionsContainer, data, "Detail Transaksi Harian");
            csvButtons.classList.remove('hidden');

        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                showError('Tidak dapat terhubung ke server. Pastikan server berjalan.');
            } else {
                showError(error.message);
            }
        } finally {
            showLoader(false);
        }
    });

    copyCsvBtn.addEventListener('click', async () => {
        if (!currentTransactionsData) return;
        const csvContent = convertToCSV(currentTransactionsData);
        const success = await copyToClipboard(csvContent);
        if (success) {
            showNotification(`${currentTransactionsData.length} rows have been copied to clipboard`);
        } else {
            showError('Failed to copy to clipboard');
        }
    });

    downloadCsvBtn.addEventListener('click', () => {
        if (!currentTransactionsData) return;
        const csvContent = convertToCSV(currentTransactionsData);
        const filename = `expense_data_${yearSelect.value}_${monthSelect.value}.csv`;
        downloadCSV(csvContent, filename);
    });
});