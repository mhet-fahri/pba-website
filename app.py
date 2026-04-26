import os
import json
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'pba-uin-jakarta-secret-key-2026' # Should be changed in production

# Admin Credentials (Simple system)
ADMIN_PASSWORD = 'pba_admin_2026'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_lang():
    # Only Indonesian is supported now
    ui = {
        'beranda': 'Beranda',
        'profil': 'Profil',
        'kurikulum': 'Kurikulum',
        'dosen': 'Dosen',
        'riset': 'Research & Publication',
        'mahasiswa': 'Mahasiswa',
        'alumni': 'Alumni',
        'berita': 'Berita',
        'selengkapnya': 'Baca Selengkapnya',
        'kontak': 'Kontak Kami',
        'search': 'Cari...'
    }
    return dict(current_lang='id', ui=ui)

# Utility for JSON writing
def save_json(data, filename):
    json_path = os.path.join(app.root_path, f'static/data/{filename}.json')
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def load_mata_kuliah():
    json_path = os.path.join(app.root_path, 'static/data/mata_kuliah.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_research():
    json_path = os.path.join(app.root_path, 'static/data/research.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_dosen():
    json_path = os.path.join(app.root_path, 'static/data/dosen.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_mahasiswa_data():
    json_path = os.path.join(app.root_path, 'static/data/mahasiswa_data.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"stats": [], "enrollment_chart": [], "distribution": []}

def load_prestasi():
    json_path = os.path.join(app.root_path, 'static/data/prestasi.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_alumni_data():
    json_path = os.path.join(app.root_path, 'static/data/alumni_data.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"summary": [], "employment_sectors": [], "work_locations": []}

def load_alumni_testimonials():
    json_path = os.path.join(app.root_path, 'static/data/alumni_testimonials.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_events():
    json_path = os.path.join(app.root_path, 'static/data/events.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_news():
    json_path = os.path.join(app.root_path, 'static/data/news.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.route('/')
def home():
    news_data = load_news()
    testimonials = load_alumni_testimonials()
    events = load_events()
    # Get latest 3 news
    latest_news = sorted(news_data, key=lambda x: x.get('date', ''), reverse=True)[:3]
    return render_template('index.html', news=latest_news, testimonials=testimonials, events=events)

@app.route('/sejarah')
def sejarah():
    return render_template('sejarah.html')

@app.route('/visi')
def visi():
    return render_template('visi.html')

@app.route('/tujuan')
def tujuan():
    return render_template('tujuan.html')

@app.route('/lulusan')
def lulusan():
    return render_template('profil_lulusan.html')

@app.route('/cpl')
def cpl():
    return render_template('cpl.html')

@app.route('/mata-kuliah')
def mata_kuliah():
    data = load_mata_kuliah()
    mandatory = [mk for mk in data if mk.get('Jenis MK') != 'Pilihan']
    optional = [mk for mk in data if mk.get('Jenis MK') == 'Pilihan']
    return render_template('mata_kuliah.html', mandatory=mandatory, optional=optional)

@app.route('/dosen')
def dosen():
    data = load_dosen()
    return render_template('dosen.html', dosen=data)

@app.route('/mahasiswa/data')
def mahasiswa_data():
    data = load_mahasiswa_data()
    return render_template('data_mahasiswa.html', data=data)

@app.route('/mahasiswa/prestasi')
def prestasi():
    data = load_prestasi()
    return render_template('prestasi.html', prestasi=data)

@app.route('/alumni/data')
def alumni_data():
    data = load_alumni_data()
    return render_template('data_alumni.html', data=data)

@app.route('/research')
def research():
    data = load_research()
    # Sort by year descending
    data = sorted(data, key=lambda x: x.get('year', 0), reverse=True)
    return render_template('research.html', publications=data)

@app.route('/berita')
def berita():
    news_data = load_news()
    # Sort by date descending
    news_data = sorted(news_data, key=lambda x: x.get('date', ''), reverse=True)
    return render_template('berita.html', news=news_data)

@app.route('/berita/<int:news_id>')
def berita_detail(news_id):
    news_data = load_news()
    article = next((item for item in news_data if item['id'] == news_id), None)
    if article:
        return render_template('berita_detail.html', article=article)
    return "Berita tidak ditemukan", 404


# --- Admin Area Routes ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Login berhasil!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Password salah!', 'danger')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Load basic stats for dashboard overview
    news_count = len(load_news())
    events_count = len(load_events())
    alumni_count = len(load_alumni_testimonials())
    publications_count = len(load_research())
    return render_template('admin/dashboard.html', 
                         news_count=news_count, 
                         events_count=events_count, 
                         alumni_count=alumni_count,
                         publications_count=publications_count)

# --- Manage News ---
@app.route('/admin/news', methods=['GET', 'POST'])
@login_required
def manage_news():
    news_data = load_news()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            new_item = {
                "id": max([n['id'] for n in news_data] + [0]) + 1,
                "title": request.form.get('title'),
                "category": request.form.get('category'),
                "date": request.form.get('date'),
                "excerpt": request.form.get('excerpt'),
                "content": request.form.get('content'),
                "image_url": request.form.get('image_url')
            }
            news_data.append(new_item)
            save_json(news_data, 'news')
            flash('Berita berhasil ditambahkan!', 'success')
            return redirect(url_for('manage_news'))
        elif action == 'delete':
            news_id = int(request.form.get('id'))
            news_data = [n for n in news_data if n['id'] != news_id]
            save_json(news_data, 'news')
            flash('Berita berhasil dihapus!', 'warning')
            return redirect(url_for('manage_news'))
    
    return render_template('admin/manage_news.html', news=news_data)

@app.route('/admin/news/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news_data = load_news()
    article = next((n for n in news_data if n['id'] == news_id), None)
    if not article:
        flash('Berita tidak ditemukan!', 'danger')
        return redirect(url_for('manage_news'))
    
    if request.method == 'POST':
        article.update({
            "title": request.form.get('title'),
            "category": request.form.get('category'),
            "date": request.form.get('date'),
            "excerpt": request.form.get('excerpt'),
            "content": request.form.get('content'),
            "image_url": request.form.get('image_url')
        })
        save_json(news_data, 'news')
        flash('Berita diperbarui!', 'success')
        return redirect(url_for('manage_news'))
    
    return render_template('admin/edit_news.html', item=article)

# --- Manage Events ---
@app.route('/admin/events', methods=['GET', 'POST'])
@login_required
def manage_events():
    events = load_events()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            new_event = {
                "id": max([e['id'] for e in events] + [0]) + 1,
                "title": request.form.get('title'),
                "day": request.form.get('day'),
                "month": request.form.get('month'),
                "time": request.form.get('time'),
                "location": request.form.get('location'),
                "image": request.form.get('image'),
                "type": request.form.get('type')
            }
            events.append(new_event)
            save_json(events, 'events')
            flash('Kegiatan ditambahkan!', 'success')
        elif action == 'delete':
            event_id = int(request.form.get('id'))
            events = [e for e in events if e['id'] != event_id]
            save_json(events, 'events')
            flash('Kegiatan dihapus!', 'warning')
        return redirect(url_for('manage_events'))
    
    return render_template('admin/manage_events.html', events=events)

@app.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    events = load_events()
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        flash('Kegiatan tidak ditemukan!', 'danger')
        return redirect(url_for('manage_events'))
    
    if request.method == 'POST':
        event.update({
            "title": request.form.get('title'),
            "day": request.form.get('day'),
            "month": request.form.get('month'),
            "time": request.form.get('time'),
            "location": request.form.get('location'),
            "image": request.form.get('image'),
            "type": request.form.get('type')
        })
        save_json(events, 'events')
        flash('Kegiatan diperbarui!', 'success')
        return redirect(url_for('manage_events'))
    
    return render_template('admin/edit_event.html', item=event)

# --- Manage Alumni ---
@app.route('/admin/alumni', methods=['GET', 'POST'])
@login_required
def manage_alumni():
    testimonials = load_alumni_testimonials()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            new_alumni = {
                "id": max([t['id'] for t in testimonials] + [0]) + 1,
                "name": request.form.get('name'),
                "year": request.form.get('year'),
                "position": request.form.get('position'),
                "quote": request.form.get('quote'),
                "image": request.form.get('image'),
                "instagram": request.form.get('instagram')
            }
            testimonials.append(new_alumni)
            save_json(testimonials, 'alumni_testimonials')
            flash('Testimoni alumni ditambahkan!', 'success')
        elif action == 'delete':
            alumni_id = int(request.form.get('id'))
            testimonials = [t for t in testimonials if t['id'] != alumni_id]
            save_json(testimonials, 'alumni_testimonials')
            flash('Testimoni dihapus!', 'warning')
        return redirect(url_for('manage_alumni'))
    
    return render_template('admin/manage_alumni.html', testimonials=testimonials)

@app.route('/admin/alumni/edit/<int:alumni_id>', methods=['GET', 'POST'])
@login_required
def edit_alumni(alumni_id):
    testimonials = load_alumni_testimonials()
    alumni = next((t for t in testimonials if t['id'] == alumni_id), None)
    if not alumni:
        flash('Data alumni tidak ditemukan!', 'danger')
        return redirect(url_for('manage_alumni'))
    
    if request.method == 'POST':
        alumni.update({
            "name": request.form.get('name'),
            "year": request.form.get('year'),
            "position": request.form.get('position'),
            "quote": request.form.get('quote'),
            "image": request.form.get('image'),
            "instagram": request.form.get('instagram')
        })
        save_json(testimonials, 'alumni_testimonials')
        flash('Data alumni diperbarui!', 'success')
        return redirect(url_for('manage_alumni'))
    
    return render_template('admin/edit_alumni.html', item=alumni)

# --- Manage Publications ---
@app.route('/admin/publications', methods=['GET', 'POST'])
@login_required
def manage_publications():
    publications = load_research()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            new_pub = {
                "id": max([p['id'] for p in publications] + [0]) + 1,
                "title": request.form.get('title'),
                "authors": request.form.get('authors'),
                "year": int(request.form.get('year')),
                "type": request.form.get('type'),
                "publisher": request.form.get('publisher'),
                "link": request.form.get('link'),
                "category": request.form.get('category')
            }
            publications.append(new_pub)
            save_json(publications, 'research')
            flash('Publikasi berhasil ditambahkan!', 'success')
        elif action == 'delete':
            pub_id = int(request.form.get('id'))
            publications = [p for p in publications if p['id'] != pub_id]
            save_json(publications, 'research')
            flash('Publikasi berhasil dihapus!', 'warning')
        return redirect(url_for('manage_publications'))
    
    return render_template('admin/manage_publications.html', publications=publications)

@app.route('/admin/publications/edit/<int:pub_id>', methods=['GET', 'POST'])
@login_required
def edit_publication(pub_id):
    publications = load_research()
    pub = next((p for p in publications if p['id'] == pub_id), None)
    if not pub:
        flash('Publikasi tidak ditemukan!', 'danger')
        return redirect(url_for('manage_publications'))
    
    if request.method == 'POST':
        pub.update({
            "title": request.form.get('title'),
            "authors": request.form.get('authors'),
            "year": int(request.form.get('year')),
            "type": request.form.get('type'),
            "publisher": request.form.get('publisher'),
            "link": request.form.get('link'),
            "category": request.form.get('category')
        })
        save_json(publications, 'research')
        flash('Publikasi diperbarui!', 'success')
        return redirect(url_for('manage_publications'))
    
    return render_template('admin/edit_publication.html', item=pub)

# --- Manage Student Data ---
@app.route('/admin/mahasiswa', methods=['GET', 'POST'])
@login_required
def manage_mahasiswa():
    data = load_mahasiswa_data()
    if request.method == 'POST':
        # Simple update for stats
        data['stats'] = [
            {"label": "Mahasiswa Aktif", "value": request.form.get('aktif'), "icon": "users"},
            {"label": "Tingkat Kelulusan", "value": request.form.get('lulus'), "icon": "award"},
            {"label": "Rasio Dosen:Mhs", "value": request.form.get('rasio'), "icon": "percentage"}
        ]
        save_json(data, 'mahasiswa_data')
        flash('Data statistik mahasiswa diperbarui!', 'success')
        return redirect(url_for('manage_mahasiswa'))
    
    return render_template('admin/manage_mahasiswa.html', data=data)

if __name__ == '__main__':
    import sys
    port = 5001 # Changed from 5000 to avoid macOS AirPlay conflict
    if '--port' in sys.argv:
        try:
            port_idx = sys.argv.index('--port') + 1
            port = int(sys.argv[port_idx])
        except (IndexError, ValueError):
            pass
            
    print(f"Website PBA UIN Jakarta berjalan di http://127.0.0.1:{port}")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
