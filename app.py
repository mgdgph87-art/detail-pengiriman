from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_paket_kamu'

# List di dalam memori untuk menyimpan data pengiriman
daftar_tamu = []

# Halaman 1: Detail Pengirim
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['pengirim'] = {
            'nama': request.form.get('nama'),
            'nohp': request.form.get('instansi'),
            'alamat': request.form.get('keperluan')
        }
        return redirect(url_for('tujuan'))
    return render_template('index.html')

# Halaman 2: Detail Tujuan Paket
@app.route('/tujuan', methods=['GET', 'POST'])
def tujuan():
    if 'pengirim' not in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        pengirim = session['pengirim']
        data_lengkap = {
            'nama_pengirim': pengirim['nama'],
            'nohp_pengirim': pengirim['nohp'],
            'alamat_pengirim': pengirim['alamat'],
            'nama_penerima': request.form.get('nama_penerima'),
            'nohp_penerima': request.form.get('nohp_penerima'),
            'alamat_tujuan': request.form.get('alamat_tujuan')
        }
        daftar_tamu.append(data_lengkap)
        session.pop('pengirim', None)
        return redirect(url_for('sukses'))
        
    return render_template('tujuan.html')

@app.route('/sukses')
def sukses():
    return "<h1 style='text-align:center; margin-top:50px; font-family:sans-serif;'>Terima kasih! Detail Pengiriman Paket Berhasil Tersimpan.</h1>"

# Rute Rahasia Admin (Daftar Customer)
@app.route('/admin')
def admin():
    if request.remote_addr not in ['127.0.0.1', 'localhost']:
        abort(403)
    return render_template('admin.html', tamu=daftar_tamu)

# FITUR BARU: Hapus Data Berdasarkan Indeks
@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_tamu(id):
    if request.remote_addr not in ['127.0.0.1', 'localhost']:
        abort(403)
    if 0 <= id < len(daftar_tamu):
        daftar_tamu.pop(id) # Menghapus data dari list
    return redirect(url_for('admin'))

# FITUR BARU: Edit Data Berdasarkan Indeks
@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_tamu(id):
    if request.remote_addr not in ['127.0.0.1', 'localhost']:
        abort(403)
        
    if id < 0 or id >= len(daftar_tamu):
        return "Data tidak ditemukan", 404
        
    if request.method == 'POST':
        # Update data lama dengan data baru dari form edit
        daftar_tamu[id] = {
            'nama_pengirim': request.form.get('nama_pengirim'),
            'nohp_pengirim': request.form.get('nohp_pengirim'),
            'alamat_pengirim': request.form.get('alamat_pengirim'),
            'nama_penerima': request.form.get('nama_penerima'),
            'nohp_penerima': request.form.get('nohp_penerima'),
            'alamat_tujuan': request.form.get('alamat_tujuan')
        }
        return redirect(url_for('admin'))
        
    # Ambil data spesifik yang ingin diedit untuk ditampilkan di form
    data_tamu = daftar_tamu[id]
    return render_template('edit.html', t=data_tamu, id=id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)