import json, re

with open(r'c:\Users\misha\Downloads\NAMAZ\prayer_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Build JS object literal for PRAYER_DB
db_lines = ['const PRAYER_DB = {']
for date, times in db.items():
    db_lines.append(f'    "{date}":{{Fajr:"{times["Fajr"]}",Dhuhr:"{times["Dhuhr"]}",Asr:"{times["Asr"]}",Maghrib:"{times["Maghrib"]}",Isha:"{times["Isha"]}"}},')
db_lines.append('};')
PRAYER_DB_JS = '\n'.join(db_lines)

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Namaz Tracker - Malappuram</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --primary: #16a34a;
            --primary-light: #22c55e;
            --primary-dark: #15803d;
            --secondary: #d97706;
            --accent: #f59e0b;
            --bg: #f0fdf4;
            --bg2: #dcfce7;
            --card: #ffffff;
            --text-dark: #14532d;
            --text-mid: #166534;
            --text-muted: #4b7a57;
            --text-gold: #b45309;
            --gold: #f59e0b;
            --glass: rgba(255,255,255,0.7);
            --shadow: 0 4px 24px rgba(22,163,74,0.10);
        }
        * { margin:0; padding:0; box-sizing:border-box; font-family:'Outfit',sans-serif; }

        /* ── SPLASH PAGE ── */
        .splash {
            min-height:100vh;
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 40%, #d1fae5 100%);
            display:flex; flex-direction:column; align-items:center; justify-content:center;
            text-align:center; padding:2rem; position:relative; overflow:hidden;
        }
        .splash::before {
            content:''; position:absolute; top:-80px; right:-80px;
            width:320px; height:320px; border-radius:50%;
            background:radial-gradient(circle, rgba(245,158,11,0.15), transparent 70%);
        }
        .splash::after {
            content:''; position:absolute; bottom:-60px; left:-60px;
            width:260px; height:260px; border-radius:50%;
            background:radial-gradient(circle, rgba(22,163,74,0.12), transparent 70%);
        }
        .splash-arabic {
            font-family:'Amiri',serif; font-size:2rem;
            color:var(--primary-dark); opacity:0.5; margin-bottom:1.5rem; letter-spacing:2px;
        }
        .splash-mosque {
            font-size:5rem; margin-bottom:1rem;
            animation: floatUp 3s ease-in-out infinite;
        }
        @keyframes floatUp {
            0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)}
        }
        .splash h1 {
            font-family:'Amiri',serif; font-size:3rem;
            color:var(--primary-dark); margin-bottom:0.5rem;
            text-shadow:0 2px 8px rgba(22,163,74,0.15);
        }
        .splash-sub {
            font-size:1rem; color:var(--text-muted); margin-bottom:0.5rem; letter-spacing:1px;
        }
        .splash-location {
            display:inline-flex; align-items:center; gap:0.4rem;
            background:rgba(22,163,74,0.1); color:var(--primary-dark);
            padding:0.3rem 0.9rem; border-radius:99px; font-size:0.85rem;
            margin-bottom:2.5rem; border:1px solid rgba(22,163,74,0.2);
        }
        .splash-enter-btn {
            background:linear-gradient(135deg, #16a34a, #15803d);
            color:white; border:none; padding:1rem 3rem;
            border-radius:99px; font-size:1.1rem; font-weight:700;
            cursor:pointer; box-shadow:0 8px 30px rgba(22,163,74,0.35);
            transition:all 0.3s ease; letter-spacing:0.5px;
            position:relative; z-index:1;
        }
        .splash-enter-btn:hover { transform:translateY(-3px) scale(1.03); box-shadow:0 12px 40px rgba(22,163,74,0.5); }
        .splash-enter-btn:active { transform:translateY(0); }
        .splash-dots {
            display:flex; gap:0.5rem; justify-content:center; margin-top:2rem;
        }
        .splash-dot {
            width:8px; height:8px; border-radius:50%; background:var(--gold); opacity:0.4;
        }
        .splash-dot:nth-child(2){opacity:0.7;} .splash-dot:nth-child(3){opacity:1;}

        /* ── MAIN APP ── */
        body {
            background: linear-gradient(160deg, #f0fdf4 0%, #dcfce7 100%);
            min-height:100vh; color:var(--text-dark); padding-bottom:5rem; overflow-x:hidden;
        }
        .container { max-width:500px; margin:0 auto; padding:1.5rem; }
        header { text-align:center; margin-bottom:2rem; padding-top:1rem; }
        h1 { font-family:'Amiri',serif; font-size:2.4rem; color:var(--primary-dark); margin-bottom:0.4rem; }
        .subtitle { font-size:0.8rem; color:var(--text-muted); letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem; }
        .date-badge {
            display:inline-block; padding:0.4rem 1.1rem;
            background:rgba(22,163,74,0.1); border:1px solid rgba(22,163,74,0.25);
            border-radius:99px; font-size:0.85rem; color:var(--text-mid); font-weight:500;
        }
        /* Floating buttons */
        .qibla-btn {
            position:fixed; top:1.2rem; right:1.2rem;
            width:48px; height:48px; background:linear-gradient(135deg,#f59e0b,#d97706);
            border:none; border-radius:50%; display:flex; align-items:center; justify-content:center;
            color:white; box-shadow:0 4px 16px rgba(245,158,11,0.4);
            cursor:pointer; transition:transform 0.3s ease; z-index:100;
        }
        .qibla-btn:hover { transform:scale(1.1) rotate(15deg); }
        .calendar-fab {
            position:fixed; bottom:2rem; right:2rem;
            width:58px; height:58px; background:linear-gradient(135deg,#16a34a,#15803d);
            border:none; border-radius:50%; color:white;
            display:flex; align-items:center; justify-content:center;
            box-shadow:0 8px 24px rgba(22,163,74,0.4); cursor:pointer; z-index:90;
            transition:transform 0.2s ease;
        }
        .calendar-fab:hover { transform:scale(1.1); }
        /* Cards */
        .card {
            background:var(--card); border-radius:24px;
            padding:1.5rem; margin-bottom:1.5rem;
            box-shadow:var(--shadow); border:1px solid rgba(22,163,74,0.1);
        }
        .section-title { font-size:1rem; font-weight:700; color:var(--primary-dark); margin-bottom:1rem; display:flex; align-items:center; gap:0.5rem; }
        /* Prayer time grid */
        .prayer-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:0.75rem; }
        .prayer-item-small {
            background:var(--bg2); padding:0.7rem 0.4rem;
            border-radius:14px; text-align:center; border:1px solid rgba(22,163,74,0.12);
        }
        .prayer-item-small span { display:block; font-size:0.68rem; color:var(--text-muted); margin-bottom:0.2rem; }
        .prayer-item-small strong { color:var(--text-gold); font-size:0.92rem; font-weight:700; }
        /* Progress pill */
        .progress-pill {
            display:flex; align-items:center; justify-content:center; gap:0.5rem;
            background:white; border:1px solid rgba(22,163,74,0.2);
            border-radius:99px; padding:0.4rem 1.2rem; font-size:0.85rem; margin-bottom:1.5rem;
            box-shadow:0 2px 8px rgba(22,163,74,0.08);
        }
        .progress-pill.full { background:#f0fdf4; border-color:rgba(22,163,74,0.4); }
        /* Namaz list */
        .namaz-list { display:flex; flex-direction:column; gap:0.75rem; }
        .namaz-row {
            display:flex; align-items:center; justify-content:space-between;
            padding:0.9rem 1rem; background:var(--bg);
            border-radius:16px; border:1.5px solid transparent; transition:all 0.3s ease;
        }
        .namaz-row.completed { background:#dcfce7; border-color:rgba(22,163,74,0.3); }
        .namaz-info h3 { font-size:1rem; color:var(--text-dark); margin-bottom:0.1rem; font-weight:600; }
        .namaz-info p { font-size:0.75rem; color:var(--text-muted); }
        .mark-btn {
            background:linear-gradient(135deg,#16a34a,#15803d); color:white; border:none;
            padding:0.5rem 0.9rem; border-radius:10px; font-weight:600; cursor:pointer;
            transition:all 0.2s ease; display:flex; align-items:center; gap:0.4rem; font-size:0.82rem;
        }
        .mark-btn:hover:not(:disabled) { transform:translateY(-2px); box-shadow:0 4px 12px rgba(22,163,74,0.3); }
        .mark-btn.checked { background:linear-gradient(135deg,#f59e0b,#d97706); cursor:default; }
        /* Modal */
        .modal {
            position:fixed; top:0; left:0; width:100%; height:100%;
            background:rgba(0,0,0,0.4); backdrop-filter:blur(6px);
            display:flex; align-items:center; justify-content:center; z-index:1000; padding:1rem;
        }
        .modal-content {
            background:white; border-radius:24px; width:100%; max-width:440px;
            padding:1.5rem; position:relative; max-height:90vh; overflow-y:auto;
            box-shadow:0 20px 60px rgba(0,0,0,0.15);
        }
        .close-modal {
            position:absolute; top:1rem; right:1rem;
            background:var(--bg2); border:none; color:var(--text-dark);
            cursor:pointer; width:30px; height:30px; border-radius:50%;
            display:flex; align-items:center; justify-content:center; font-weight:700;
        }
        /* Calendar */
        .cal-nav { display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; }
        .cal-nav h3 { color:var(--primary-dark); font-size:1.05rem; font-weight:700; }
        .cal-nav-btn {
            background:var(--bg2); border:none; color:var(--primary-dark);
            width:30px; height:30px; border-radius:50%; cursor:pointer;
            display:flex; align-items:center; justify-content:center; font-size:1rem;
            transition:background 0.2s;
        }
        .cal-nav-btn:hover { background:#bbf7d0; }
        .cal-weekdays { display:grid; grid-template-columns:repeat(7,1fr); gap:2px; margin-bottom:4px; }
        .cal-weekday { text-align:center; font-size:0.62rem; color:var(--text-muted); padding:0.2rem 0; font-weight:600; }
        .cal-days { display:grid; grid-template-columns:repeat(7,1fr); gap:4px; }
        .cal-day {
            aspect-ratio:1; display:flex; flex-direction:column;
            align-items:center; justify-content:center; border-radius:10px;
            font-size:0.78rem; cursor:pointer; transition:all 0.15s ease;
            border:1.5px solid transparent; color:var(--text-dark); font-weight:500;
            position:relative;
        }
        .cal-day:hover { background:var(--bg2); }
        .cal-day.empty { cursor:default; }
        .cal-day.today { background:#dcfce7; border-color:#16a34a; color:var(--primary-dark); font-weight:700; }
        .cal-day.has-data::after {
            content:''; display:block; width:4px; height:4px;
            background:var(--gold); border-radius:50%; margin-top:2px;
        }
        .cal-day.selected { background:linear-gradient(135deg,#f59e0b,#d97706); color:white; border-color:transparent; }
        .cal-day.selected::after { background:white; }
        /* Day detail */
        .day-detail { margin-top:1rem; border-top:1px solid var(--bg2); padding-top:1rem; }
        .day-detail h4 { color:var(--primary-dark); margin-bottom:0.75rem; font-size:0.9rem; font-weight:700; }
        .detail-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:0.5rem; }
        .detail-item { background:var(--bg2); border-radius:10px; padding:0.5rem; text-align:center; }
        .detail-item span { display:block; font-size:0.63rem; color:var(--text-muted); margin-bottom:0.1rem; }
        .detail-item strong { font-size:0.85rem; color:var(--text-gold); font-weight:700; }
        .no-data-msg { text-align:center; opacity:0.4; font-size:0.85rem; padding:1rem 0; }
        /* Spinner */
        .loading-spinner {
            width:36px; height:36px; border:4px solid var(--bg2);
            border-top:4px solid var(--primary); border-radius:50%;
            animation:spin 1s linear infinite; margin:1.5rem auto;
        }
        @keyframes spin { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
        /* Back button */
        .back-btn {
            position:fixed; top:1.2rem; left:1.2rem;
            background:white; border:1px solid rgba(22,163,74,0.2);
            border-radius:99px; padding:0.4rem 0.9rem; font-size:0.78rem;
            color:var(--primary-dark); cursor:pointer; z-index:100;
            display:flex; align-items:center; gap:0.3rem;
            box-shadow:0 2px 8px rgba(0,0,0,0.06);
        }
        @media(max-width:400px) { h1{font-size:2rem;} .card{padding:1rem;} }
    </style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect } = React;

__PRAYER_DB__

const MONTH_NAMES = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const NAMAZ = ['Fajr','Dhuhr','Asr','Maghrib','Isha'];

function FullCalendar({ onClose }) {
    const now = new Date();
    const todayStr = now.toLocaleDateString('en-CA');
    const [viewYear, setViewYear] = useState(now.getFullYear());
    const [viewMonth, setViewMonth] = useState(now.getMonth());
    const [selectedDate, setSelectedDate] = useState(null);
    const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();
    const firstDay = new Date(viewYear, viewMonth, 1).getDay();
    const pad = n => String(n).padStart(2,'0');
    const dateKey = day => `${viewYear}-${pad(viewMonth+1)}-${pad(day)}`;
    const prevMonth = () => { if(viewMonth===0){setViewMonth(11);setViewYear(y=>y-1);}else setViewMonth(m=>m-1); setSelectedDate(null); };
    const nextMonth = () => { if(viewMonth===11){setViewMonth(0);setViewYear(y=>y+1);}else setViewMonth(m=>m+1); setSelectedDate(null); };
    const cells = [];
    for(let i=0;i<firstDay;i++) cells.push(null);
    for(let d=1;d<=daysInMonth;d++) cells.push(d);
    const selData = selectedDate ? PRAYER_DB[selectedDate] : null;
    const selTracked = selectedDate ? (() => { const r=localStorage.getItem(`namaz_track_${selectedDate}`); return r?JSON.parse(r):null; })() : null;
    return (
        <div className="modal" onClick={onClose}>
            <div className="modal-content" onClick={e=>e.stopPropagation()}>
                <button className="close-modal" onClick={onClose}>✕</button>
                <div className="section-title">📅 Prayer Calendar</div>
                <div className="cal-nav">
                    <button className="cal-nav-btn" onClick={prevMonth}>‹</button>
                    <h3>{MONTH_NAMES[viewMonth]} {viewYear}</h3>
                    <button className="cal-nav-btn" onClick={nextMonth}>›</button>
                </div>
                <div className="cal-weekdays">
                    {['Su','Mo','Tu','We','Th','Fr','Sa'].map(d=><div key={d} className="cal-weekday">{d}</div>)}
                </div>
                <div className="cal-days">
                    {cells.map((day,idx) => {
                        if(!day) return <div key={`e${idx}`} className="cal-day empty"/>;
                        const key=dateKey(day), isToday=key===todayStr, hasData=!!PRAYER_DB[key], isSel=key===selectedDate;
                        return <div key={key} className={`cal-day ${isToday?'today':''} ${hasData?'has-data':''} ${isSel?'selected':''}`} onClick={()=>setSelectedDate(isSel?null:key)}>{day}</div>;
                    })}
                </div>
                <div style={{display:'flex',gap:'1rem',marginTop:'0.6rem',fontSize:'0.65rem',opacity:0.5,justifyContent:'center'}}>
                    <span>🟡 Dot = data</span><span>🟢 Green = today</span><span>🟠 Orange = selected</span>
                </div>
                {selectedDate && (
                    <div className="day-detail">
                        <h4>{new Date(selectedDate+'T12:00:00').toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric'})}</h4>
                        {selData ? (
                            <>
                                <div className="detail-grid" style={{marginBottom:'0.6rem'}}>
                                    {NAMAZ.map(n=><div key={n} className="detail-item"><span>{n}</span><strong>{selData[n]}</strong></div>)}
                                </div>
                                {selTracked && (
                                    <div>
                                        <div style={{fontSize:'0.72rem',color:'var(--text-muted)',marginBottom:'0.4rem'}}>✅ Your completion:</div>
                                        <div style={{display:'flex',flexWrap:'wrap',gap:'0.35rem'}}>
                                            {NAMAZ.map(n=>(
                                                <span key={n} style={{padding:'0.2rem 0.6rem',borderRadius:'99px',fontSize:'0.68rem',
                                                    background:selTracked[n]?'#dcfce7':'#f0fdf4',
                                                    border:`1px solid ${selTracked[n]?'#86efac':'#d1fae5'}`,
                                                    color:selTracked[n]?'#15803d':'#9ca3af'}}>
                                                    {n} {selTracked[n]?`✓ ${selTracked[n]}`:'—'}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </>
                        ) : <p className="no-data-msg">No prayer time data for this date</p>}
                    </div>
                )}
            </div>
        </div>
    );
}

function MainApp({ onBack }) {
    const [timings, setTimings] = useState(null);
    const [loading, setLoading] = useState(true);
    const [completed, setCompleted] = useState({});
    const [showCalendar, setShowCalendar] = useState(false);
    const today = new Date().toLocaleDateString('en-CA');
    useEffect(() => {
        if(PRAYER_DB[today]){ setTimings(PRAYER_DB[today]); setLoading(false); }
        else fetch(`https://api.aladhan.com/v1/timingsByCity?city=Malappuram&country=India&method=2`)
            .then(r=>r.json()).then(d=>{ if(d.code===200){const t=d.data.timings; setTimings({Fajr:t.Fajr,Dhuhr:t.Dhuhr,Asr:t.Asr,Maghrib:t.Maghrib,Isha:t.Isha});} })
            .catch(()=>{}).finally(()=>setLoading(false));
        const s=localStorage.getItem(`namaz_track_${today}`); setCompleted(s?JSON.parse(s):{});
        setTimeout(()=>window.lucide&&window.lucide.createIcons(),300);
    },[]);
    const markNamaz = name => {
        const u={...completed,[name]:new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})};
        setCompleted(u); localStorage.setItem(`namaz_track_${today}`,JSON.stringify(u));
        setTimeout(()=>window.lucide&&window.lucide.createIcons(),100);
    };
    const count=Object.values(completed).filter(Boolean).length;
    return (
        <div className="container">
            <button className="back-btn" onClick={onBack}>← Home</button>
            <button className="qibla-btn" onClick={()=>window.open('https://qiblafinder.withgoogle.com/','_blank')} title="Find Qibla">
                <i data-lucide="compass"></i>
            </button>
            <header>
                <div className="subtitle">بسم الله الرحمن الرحيم</div>
                <h1>Namaz Tracker</h1>
                <div className="date-badge">
                    {new Date().toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric'})}
                </div>
            </header>
            <div className={`progress-pill ${count===5?'full':''}`}>
                <span style={{color:'var(--primary-dark)',fontWeight:700}}>{count}/5</span>
                <span style={{color:'var(--text-muted)'}}>prayers completed today</span>
                {count===5 && <span>🌟</span>}
            </div>
            <div className="card">
                <div className="section-title"><i data-lucide="clock"></i> Today's Times — Malappuram</div>
                {loading ? <div className="loading-spinner"></div> : timings ? (
                    <div className="prayer-grid">
                        {NAMAZ.map(n=><div key={n} className="prayer-item-small"><span>{n}</span><strong>{timings[n]||'--:--'}</strong></div>)}
                    </div>
                ) : <p style={{textAlign:'center',opacity:0.4,fontSize:'0.85rem'}}>Could not load. Check connection.</p>}
            </div>
            <div className="card">
                <div className="section-title"><i data-lucide="check-circle"></i> Daily Progress</div>
                <div className="namaz-list">
                    {NAMAZ.map(n=>(
                        <div key={n} className={`namaz-row ${completed[n]?'completed':''}`}>
                            <div className="namaz-info">
                                <h3>{n}</h3>
                                <p>{completed[n]?`✓ Marked at ${completed[n]}`:timings?timings[n]:'Not marked yet'}</p>
                            </div>
                            <button className={`mark-btn ${completed[n]?'checked':''}`} onClick={()=>!completed[n]&&markNamaz(n)} disabled={!!completed[n]}>
                                {completed[n]?<><i data-lucide="check"></i>Done</>:'Mark Done'}
                            </button>
                        </div>
                    ))}
                </div>
            </div>
            <button className="calendar-fab" onClick={()=>setShowCalendar(true)} title="Prayer Calendar">
                <i data-lucide="calendar-days"></i>
            </button>
            {showCalendar && <FullCalendar onClose={()=>setShowCalendar(false)}/>}
            <footer style={{textAlign:'center',marginTop:'1rem',opacity:0.4,fontSize:'0.72rem'}}>Prayer times for Malappuram — Aladhan API</footer>
        </div>
    );
}

function SplashPage({ onEnter }) {
    return (
        <div className="splash">
            <div className="splash-arabic">بسم الله الرحمن الرحيم</div>
            <div className="splash-mosque">🕌</div>
            <h1>Namaz Tracker</h1>
            <p className="splash-sub">Daily Prayer Companion for Students</p>
            <div className="splash-location">📍 Malappuram, Kerala</div>
            <button className="splash-enter-btn" onClick={onEnter}>
                Enter App &nbsp;→
            </button>
            <div className="splash-dots">
                <div className="splash-dot"></div>
                <div className="splash-dot"></div>
                <div className="splash-dot"></div>
            </div>
        </div>
    );
}

function App() {
    const [page, setPage] = useState('splash');
    return page === 'splash'
        ? <SplashPage onEnter={() => { setPage('app'); setTimeout(()=>window.lucide&&window.lucide.createIcons(),300); }} />
        : <MainApp onBack={() => setPage('splash')} />;
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
setTimeout(()=>window.lucide&&window.lucide.createIcons(),600);
</script>
</body>
</html>'''

# Inject prayer DB
final_html = HTML.replace('__PRAYER_DB__', PRAYER_DB_JS)

with open(r'c:\Users\misha\Downloads\NAMAZ\index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f'Done! index.html generated with {len(db)} prayer entries.')
