def render_dashboard_header(title: str, logo_width: int = 110):
    logo_path = _active_logo_path()

    # Fix typo and parse title parts gracefully
    clean_title = title.replace("Dashbard", "Dashboard")
    parts = [p.strip() for p in clean_title.split("|")]
    
    main_title = parts[0] if len(parts) > 0 else clean_title
    sub_title = parts[1] if len(parts) > 1 else ""
    date_badge = parts[2] if len(parts) > 2 else ""

    is_dark = _is_dark_theme()
    title_gradient = "linear-gradient(135deg, #f8fafc, #cbd5e1)" if is_dark else "linear-gradient(135deg, #0f172a, #4f46e5)"
    sub_color = "#94a3b8" if is_dark else "#64748b"
    badge_bg = "rgba(129, 140, 248, 0.15)" if is_dark else "rgba(99, 102, 241, 0.08)"
    badge_border = "1px solid rgba(129, 140, 248, 0.3)" if is_dark else "1px solid rgba(99, 102, 241, 0.2)"
    badge_color = "#818cf8" if is_dark else "#4f46e5"

    # --- حل المشكلة هنا: تجهيز الأكواد الفرعية في متغيرات منفصلة بدون علامات مائلة عكسية ---
    badge_html = ""
    if date_badge:
        badge_html = f'<span style="background: {badge_bg}; border: {badge_border}; color: {badge_color}; padding: 4px 14px; border-radius: 20px; font-family: \'Outfit\', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">{date_badge}</span>'

    sub_title_html = ""
    if sub_title:
        sub_title_html = f'<div style="font-family: \'Outfit\', \'Cairo\', sans-serif; font-size: 15px; font-weight: 600; color: {sub_color}; letter-spacing: 0.2px; display: flex; align-items: center; gap: 6px; margin-top: 6px;"><span class="material-symbols-rounded" style="font-size: 18px; color: {badge_color};">insights</span> {sub_title}</div>'
    # ----------------------------------------------------------------------------------

    html_content = f"""
    <div style="display: flex; flex-direction: column; justify-content: center; padding: 4px 0;">
        <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
            <h1 style="font-family: 'Outfit', 'Cairo', sans-serif; font-size: 34px; font-weight: 800; margin: 0; padding: 0; background: {title_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; letter-spacing: -0.5px;">
                {main_title}
            </h1>
            {badge_html}
        </div>
        {sub_title_html}
    </div>
    """

    if logo_path:
        col_logo, col_title = st.columns([0.4, 7], vertical_alignment="center", gap="small")
        with col_logo:
            st.image(str(logo_path), width=logo_width)
        with col_title:
            st.markdown(html_content, unsafe_allow_html=True)
    else:
        st.markdown(html_content, unsafe_allow_html=True)


def section_header(icon_name, title):
    """Render a styled section header with a material icon."""
    st.markdown(f'''
    <div class="section-header">
        <span class="material-symbols-rounded">{icon_name}</span>
        {title}
    </div>
    ''', unsafe_allow_html=True)


def sidebar_header(icon_name, title):
    """Render a styled sidebar header with a material icon."""
    st.sidebar.markdown(f'''
    <div class="sidebar-header">
        <span class="material-symbols-rounded">{icon_name}</span>
        {title}
    </div>
    ''', unsafe_allow_html=True)


from auth import (
    authenticate, load_users, add_user, update_user, delete_user, save_users,
    get_user_permission_type, is_super_admin, can_access_all_branches, get_all_users
)
from data_manager import load_sales_data, load_target_data, compute_kpis, compute_mtd_target

# إعدادات الصفحة
st.set_page_config(page_title="NSTextile Dashboard", layout="wide", initial_sidebar_state="expanded")

# إعدادات وتنسيق الصفحة الاحترافي
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Cairo:wght@300;400;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* الخطوط العامة وتجانس الألوان */
    html, body, [class*="css"], .stMarkdown, .stText, p, span, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Outfit', 'Cairo', sans-serif !important;
    }

    /* Material Symbols Rounded base icon styling */
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded' !important;
        font-variation-settings: 'FILL' 1, 'wght' 500, 'GRAD' 0, 'opsz' 24;
        vertical-align: middle;
        display: inline-block;
        line-height: 1;
    }
    
    body {
        background-color: #f8fafc !important;
        color: #1e293b !important;
    }

    /* حاوية الصفحة وتقليل الهوامش الزائدة */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 95% !important;
    }

/* ---------------------------------------------
   تنسيقات احترافية ومستقرة للشريط الجانبي (Sidebar)
--------------------------------------------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e2a3a 0%, #1a2435 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    box-shadow: 4px 0 25px rgba(0,0,0,0.12) !important;
}

/* ======= حل جذري لزر فتح/قفل القائمة الجانبية ======= */
/* إخفاء كل المحتوى داخل الزر (نصوص + SVG + أيقونات مسربة) */
[data-testid="stSidebar"] button[kind="header"],
[data-testid="collapsedControl"] button,
[data-testid="stSidebarCollapseButton"],
[data-testid="baseButton-header"] {
    font-size: 0 !important;
    color: transparent !important;
    text-indent: -9999px !important;
    overflow: hidden !important;
    background: rgba(99, 102, 241, 0.12) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 10px !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    min-height: 36px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    padding: 0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    position: relative !important;
}

/* Hover effect */
[data-testid="stSidebar"] button[kind="header"]:hover,
[data-testid="collapsedControl"] button:hover,
[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="baseButton-header"]:hover {
    background: rgba(99, 102, 241, 0.25) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    transform: scale(1.05) !important;
}

/* إخفاء كل العناصر الداخلية بلا استثناء */
[data-testid="stSidebar"] button[kind="header"] > *,
[data-testid="collapsedControl"] button > *,
[data-testid="stSidebarCollapseButton"] > *,
[data-testid="baseButton-header"] > * {
    display: none !important;
    visibility: hidden !important;
    font-size: 0 !important;
    position: absolute !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* أيقونة مخصصة لزر إغلاق القائمة (داخل الشريط الجانبي) — سهم يسار */
[data-testid="stSidebar"] button[kind="header"]::after,
[data-testid="stSidebarCollapseButton"]::after {
    content: "✕" !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 16px !important;
    color: #a78bfa !important;
    text-indent: 0 !important;
    position: absolute !important;
    inset: 0 !important;
    visibility: visible !important;
    font-weight: 700 !important;
}

/* أيقونة مخصصة لزر فتح القائمة (خارج الشريط الجانبي) — قائمة ☰ */
[data-testid="collapsedControl"] button::after,
[data-testid="baseButton-header"]::after {
    content: "☰" !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 18px !important;
    color: #a78bfa !important;
    text-indent: 0 !important;
    position: absolute !important;
    inset: 0 !important;
    visibility: visible !important;
    font-weight: 400 !important;
}

/* تنظيف الحاوية الخارجية للزر المطوي */
[data-testid="collapsedControl"] {
    background-color: transparent !important;
    border: none !important;
    padding: 8px !important;
}

/* تحسين وضوح عناوين الشريط الجانبي */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] div[data-testid="stSubheader"] h3,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #818cf8 !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding-bottom: 8px !important;
    margin-bottom: 14px !important;
    margin-top: 18px !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}

/* تنسيق حاويات عناصر التحكم بالشريط الجانبي */
[data-testid="stSidebar"] .stSelectbox, 
[data-testid="stSidebar"] .stRadio, 
[data-testid="stSidebar"] .stNumberInput {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 12px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1) !important;
}

/* تخصيص الـ Selectbox داخل القائمة */
[data-testid="stSidebar"] div[data-baseweb="select"] {
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background-color: rgba(255, 255, 255, 0.03) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"]:hover {
    border-color: rgba(255, 255, 255, 0.2) !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: transparent !important;
    color: #f1f5f9 !important;
}

/* تخصيص الـ Radio وتحويلها إلى أزرار مقسمة أنيقة وعصرية */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 8px !important;
    display: flex !important;
    flex-direction: column !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 8px !important;
    padding: 10px 12px !important;
    margin-bottom: 0px !important;
    color: #cbd5e1 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: rgba(255, 255, 255, 0.06) !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
    color: white !important;
}

/* إخفاء دائرة الراديو الافتراضية بالكامل */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* محاذاة النص بالمنتصف بعد الحذف */
[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
    margin-left: 0 !important;
    padding: 0 !important;
    text-align: center !important;
    width: 100% !important;
}

/* 🔥 إصلاح تمييز الخيار النشط (الزر المحدد حالياً) في الراديو */
[data-testid="stSidebar"] div[role="radiogroup"] [data-checked="true"],
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked),
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input[aria-checked="true"]),
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] {
    background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
    border-color: #4f46e5 !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
}

/* ضمان لون النص أبيض داخل الخيار النشط */
[data-testid="stSidebar"] div[role="radiogroup"] [data-checked="true"] p,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input[aria-checked="true"]) p,
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p {
    color: white !important;
}

/* تخصيص زر تسجيل الخروج / الأزرار في الشريط الجانبي */
[data-testid="stSidebar"]  .stButton button {
    background-color: rgba(239, 68, 68, 0.1) !important;
    color: #f87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    padding: 8px 16px !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    border-color: #ef4444 !important;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
    color: white !important;
}

    /* ---------------------------------------------
       تنسيقات الجداول والعناصر في القسم الرئيسي
    --------------------------------------------- */
    .stDataFrame, .stDataFrame table {
        font-size: 12px !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* تخصيص شريط التمرير (Scrollbars) لمظهر متناسق */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* ============================= */
    /* ANIMATION KEYFRAMES & MOTION  */
    /* ============================= */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes shimmer {
        0% { transform: translateX(-200%); }
        100% { transform: translateX(200%); }
    }

    @keyframes pulseGlow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Section header styling */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Outfit', 'Cairo', sans-serif !important;
        font-weight: 700;
        font-size: 1.35rem;
        padding: 0.6rem 0;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }

    .section-header .material-symbols-rounded {
        font-size: 28px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Sidebar header with icon */
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 700;
        color: #a5b4fc !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 8px;
        margin-bottom: 14px;
        margin-top: 18px;
        animation: slideInLeft 0.4s ease-out;
    }

    .sidebar-header .material-symbols-rounded {
        font-size: 20px;
        color: #a5b4fc;
    }

    /* Chart & table entrance animations */
    @keyframes slideUpReveal {
        from { opacity: 0; transform: translateY(50px) scale(0.96); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes slideInFromLeft {
        from { opacity: 0; transform: translateX(-25px); }
        to { opacity: 1; transform: translateX(0); }
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stDataFrame"] {
        animation: slideUpReveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    .section-header {
        animation: slideInFromLeft 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    /* Scroll-driven animations for supported browsers (Chrome/Edge 115+) */
    @supports (animation-timeline: view()) {
        [data-testid="stPlotlyChart"],
        [data-testid="stDataFrame"] {
            animation: slideUpReveal 1s cubic-bezier(0.16, 1, 0.3, 1) both;
            animation-timeline: view();
            animation-range: entry 0% entry 35%;
        }

        .section-header {
            animation: slideInFromLeft 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
            animation-timeline: view();
            animation-range: entry 0% entry 30%;
        }
    }

    /* Smooth page transition */
    .main .block-container {
        animation: fadeIn 0.3s ease-out;
    }

    /* KPI icon inside cards */
    .kpi-icon {
        font-size: 20px !important;
        color: rgba(255,255,255,0.9) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.9) !important;
        background: none !important;
    }

    /* Trend icon in KPI sub-text */
    .trend-icon {
        font-size: 16px !important;
        vertical-align: middle;
        line-height: 1;
    }

    /* Profile card float animation */
    .profile-card {
        animation: fadeIn 0.5s ease-out;
    }

    /* ============================= */
    /* ENHANCED SIDEBAR REDESIGN     */
    /* ============================= */

    /* Enhanced Profile Card */
    .sidebar-profile-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(168, 85, 247, 0.12) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 24px 16px 18px;
        margin-bottom: 16px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        animation: fadeIn 0.5s ease-out;
    }

    .profile-avatar-lg {
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        border-radius: 50%;
        margin: 0 auto 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 24px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        animation: float 3s ease-in-out infinite;
        line-height: 1;
    }

    .profile-name-lg {
        font-weight: 700;
        font-size: 15px;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .profile-email-lg {
        font-size: 10px;
        color: #94a3b8;
        margin-bottom: 10px;
        font-family: 'Outfit', monospace;
        word-break: break-all;
        direction: ltr;
    }

    .profile-role-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }

    .profile-role-info {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin-top: 6px;
    }

    .role-info-item {
        display: flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 8px 10px;
        flex: 1;
    }

    .role-info-item .ri-label {
        font-size: 9px;
        color: #64748b;
        line-height: 1.3;
    }

    .role-info-item .ri-value {
        font-size: 11px;
        font-weight: 700;
        line-height: 1.3;
    }

    /* Sidebar Section Cards */
    .sidebar-section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 12px;
        justify-content: center;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    .sidebar-section-title .material-symbols-rounded {
        font-size: 22px;
        color: #a78bfa;
    }

    /* Filter label with icon */
    .filter-label {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 4px;
        margin-top: 10px;
    }

    .filter-label .material-symbols-rounded {
        font-size: 18px;
        color: #818cf8;
    }

    /* MTD Info Cards */
    .mtd-info-grid {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 10px;
    }

    .mtd-info-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 10px 14px;
        transition: all 0.2s ease;
    }

    .mtd-info-item:hover {
        background: rgba(255,255,255,0.05);
        border-color: rgba(255,255,255,0.1);
    }

    .mtd-info-label {
        font-size: 11px;
        color: #94a3b8;
        font-weight: 500;
    }

    .mtd-info-value {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 13px;
        font-weight: 700;
        color: #818cf8;
    }

    .mtd-info-value .material-symbols-rounded {
        font-size: 16px;
    }

    .mtd-status-active {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(52, 211, 153, 0.15);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }

    /* Sidebar footer */
    .sidebar-footer {
        text-align: center;
        padding: 14px 8px 8px;
        margin-top: 16px;
        border-top: 1px solid rgba(255,255,255,0.06);
    }

    .sidebar-footer p {
        font-size: 10px !important;
        color: #64748b !important;
        margin-bottom: 2px !important;
    }

    .sidebar-footer .heart {
        color: #818cf8;
    }
</style>

""", unsafe_allow_html=True)



# جلسة المستخدم
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_branches" not in st.session_state:
    st.session_state.user_branches = []
if "user_permission_type" not in st.session_state:
    st.session_state.user_permission_type = None
if "user_branch_filter_type" not in st.session_state:
    st.session_state.user_branch_filter_type = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "mtd_mode" not in st.session_state:
    st.session_state.mtd_mode = "Last sales date"
if "mtd_month_length" not in st.session_state:
    st.session_state.mtd_month_length = 25

# تعديل الدالة لتقرأ الملفات المرفوعة مؤقتاً تلقائياً في حال وجودها
@st.cache_resource
def load_all_data():
    # التحقق من ملف المبيعات
    if os.path.exists("temp_sales.xlsx"):
        sales_path = "temp_sales.xlsx"
    else:
        sales_path = "Sales (Naguib Selim) This Month.xlsx"
        
    # التحقق من ملف الأهداف
    if os.path.exists("temp_target.xlsx"):
        target_path = "temp_target.xlsx"
    else:
        target_path = "Target This Month.xlsx"
        
    sales_df = load_sales_data(sales_path)
    branch_target, rep_target = load_target_data(target_path)
    return sales_df, branch_target, rep_target

def get_sales_date_range(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = None
        for candidate in ["Sales Final", "Sales"]:
            if candidate in xls.sheet_names:
                sheet_name = candidate
                break
        if sheet_name is None:
            sheet_name = xls.sheet_names[0]
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = df.columns.astype(str).str.strip()
        date_cols = [c for c in df.columns if c.strip().lower() == "date" or "date" in c.lower() or "تاريخ" in c]
        if not date_cols:
            return None, None
        dates = pd.to_datetime(df[date_cols[0]], errors="coerce").dropna()
        if dates.empty:
            return None, None
        return dates.min().date(), dates.max().date()
    except Exception:
        return None, None


def get_mtd_factor(mode, sales_df, month_length=0):
    today = datetime.today()
    def days_in_month(date):
        next_month = (date.replace(day=28) + timedelta(days=4)).replace(day=1)
        return (next_month - timedelta(days=1)).day

    if mode == "Last sales date":
        if "Date" in sales_df.columns and not sales_df["Date"].dropna().empty:
            last_date = sales_df["Date"].dropna().max()
            if pd.isna(last_date):
                last_date = today
            actual_days = days_in_month(last_date)
            month_days = int(month_length) if month_length and month_length > 0 else actual_days
            month_days = max(1, month_days)
            return min(int(last_date.day), month_days) / month_days
        return 1.0
    month_days = int(month_length) if month_length and month_length > 0 else days_in_month(today)
    month_days = max(1, month_days)
    return min(today.day, month_days) / month_days

# واجهة تسجيل الدخول
def login_page():
    st.markdown("""
    <style>
        /* Main background for Login */
        .stApp {
            background: radial-gradient(circle at top right, #1e1b4b, #0f172a, #020617) !important;
        }
        
        /* Hide sidebar and top header to create a focused login screen */
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        header { display: none !important; }

        /* Align columns vertically */
        .stVerticalBlock {
            justify-content: center !important;
        }

        /* The Glass Card Form */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border-radius: 12px !important; /* Square-like corners */
            padding: 25px 30px !important;
            max-width: 400px !important;
            min-height: 400px !important; /* Force a square aspect ratio */
            margin: 0 auto !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            box-shadow: 0 40px 80px -20px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
            animation: slideUpFade 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
            position: relative;
            z-index: 10;
        }

        /* Typography */
        .login-logo {
            font-size: 52px;
            margin-bottom: 6px;
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            animation: float 4s ease-in-out infinite;
        }
        
        .login-title {
            color: #ffffff !important;
            font-family: 'Outfit', 'Cairo', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.8rem !important;
            margin-bottom: 0.2rem !important;
            letter-spacing: -0.5px;
        }
        
        .login-subtitle {
            color: #94a3b8 !important;
            font-family: 'Outfit', 'Cairo', sans-serif !important;
            font-size: 0.85rem !important;
            margin-bottom: 1.2rem !important;
        }

        /* Inputs */
        /* Hide 'Press Enter to apply' / 'Press Enter to submit' text */
        [data-testid="InputInstructions"], 
        [data-testid="stTextInput"] small,
        .st-emotion-cache-1n76uvr {
            display: none !important;
        }

        [data-testid="stTextInput"] label p {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            text-align: right !important;
            width: 100%;
            margin-bottom: 4px !important;
        }

        [data-testid="stTextInput"] input {
            background: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #0f172a !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            text-align: right !important;
            font-family: 'Outfit', 'Cairo', sans-serif !important;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: #a78bfa !important;
            box-shadow: 0 0 0 4px rgba(167, 139, 250, 0.25) !important;
            background: #ffffff !important;
        }
        
        [data-testid="stTextInput"] input::placeholder {
            color: #94a3b8 !important;
            font-weight: 400 !important;
            font-family: 'Outfit', 'Cairo', sans-serif !important;
        }

        /* Submit Button */
        [data-testid="stFormSubmitButton"] {
            width: 100% !important;
            display: flex !important;
            margin-top: 5px !important;
        }
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
            color: white !important;
            border: none !important;
            padding: 14px !important;
            border-radius: 12px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 8px 20px -5px rgba(99, 102, 241, 0.5) !important;
            width: 100% !important;
            margin-top: 0px !important;
        }

        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 0 15px 25px -5px rgba(168, 85, 247, 0.6) !important;
            background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important;
        }
        
        [data-testid="stFormSubmitButton"] button p {
            font-family: 'Outfit', 'Cairo', sans-serif !important;
            font-weight: 700 !important;
            font-size: 18px !important;
            color: white !important;
        }

        /* Error Messages */
        [data-testid="stNotification"] {
            border-radius: 16px !important;
            background: rgba(239, 68, 68, 0.15) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        [data-testid="stNotification"] p {
            color: #fca5a5 !important;
            font-weight: 600 !important;
            font-family: 'Outfit', 'Cairo', sans-serif !important;
        }

        /* Animations */
        @keyframes slideUpFade {
            from { opacity: 0; transform: translateY(50px) scale(0.95); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-12px); }
        }
        
        /* Background Animated Orbs */
        .orb-container {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            overflow: hidden;
            z-index: 0;
            pointer-events: none;
        }
        .orb-1, .orb-2 {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.45;
            animation: floatOrb 12s ease-in-out infinite alternate;
        }
        .orb-1 {
            width: 600px;
            height: 600px;
            background: #4f46e5;
            top: -200px;
            left: -150px;
        }
        .orb-2 {
            width: 500px;
            height: 500px;
            background: #a855f7;
            bottom: -150px;
            right: -100px;
            animation-delay: -6s;
        }

        @keyframes floatOrb {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(100px, 80px) scale(1.15); }
        }
    </style>
    
    <div class="orb-container">
        <div class="orb-1"></div>
        <div class="orb-2"></div>
    </div>
    """, unsafe_allow_html=True)

    # Add vertical spacing
    st.write("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("""
            <div style="text-align: center;">
                <div class="login-logo"><span class="material-symbols-rounded" style="font-size: 68px;">admin_panel_settings</span></div>
                <h1 class="login-title">تسجيل الدخول</h1>
                <p class="login-subtitle">مرحبا بك ف يي نظام متابعة مبيعات الفروع و البياعين</p>
            </div>
            """, unsafe_allow_html=True)
            
            email = st.text_input("البريد الإلكتروني", placeholder="example@nstextile-eg.com")
            password = st.text_input("كلمة المرور", type="password", placeholder="••••••••")
            
            submitted = st.form_submit_button("دخول")
            
        if submitted:
            user = authenticate(email.strip(), password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_email = email.strip()
                st.session_state.user_branches = user.get("branches", [])
                st.session_state.user_permission_type = user.get("permission_type", "specific_branches")
                st.session_state.user_branch_filter_type = user.get("branch_filter_type")
                st.session_state.is_admin = user.get("is_admin", False)
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة، يرجى المحاولة مرة أخرى.")

# صفحة الإعدادات (للمدير فقط)
# صفحة الإعدادات
def settings_page():
    from auth import is_super_admin, get_all_users, PERMISSION_TYPES
    
    st.title("⚙️ الإعدادات")
    
    # =============================================
    # قسم تغيير كلمة المرور (يظهر للجميع)
    # =============================================
    with st.expander("🔑 تغيير كلمة المرور", expanded=True):
        
        # التحقق إذا كان المستخدم مدير عام أم لا
        is_admin = is_super_admin(st.session_state.user_email)
        
        if is_admin:
            # المدير العام: يمكنه تغيير كلمة المرور لأي مستخدم
            st.markdown("**🔐 تغيير كلمة المرور لأي مستخدم (صلاحية المدير العام)**")
            users = get_all_users()
            
            if users:
                # اختيار المستخدم من القائمة
                selected_user_email = st.selectbox(
                    "اختر المستخدم", 
                    list(users.keys()), 
                    key="admin_pass_change_select"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    new_password = st.text_input("كلمة المرور الجديدة", type="password", key="admin_new_pass")
                with col2:
                    confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="admin_confirm_pass")
                
                if st.button("تحديث كلمة المرور", key="admin_update_pass"):
                    if new_password and new_password == confirm_password:
                        update_user(
                            selected_user_email,
                            password=new_password,
                            permission_type=None,
                            branch_filter_type=None,
                            branches=None
                        )
                        st.success(f"✅ تم تحديث كلمة المرور للمستخدم {selected_user_email} بنجاح")
                        st.rerun()
                    elif not new_password:
                        st.error("❌ يرجى إدخال كلمة المرور الجديدة")
                    else:
                        st.error("❌ كلمات المرور غير متطابقة")
            else:
                st.info("لا يوجد مستخدمون")
        
        else:
            # المستخدم العادي: يغير كلمة المرور الخاصة به فقط
            st.markdown(f"**🔐 تغيير كلمة المرور الخاصة بحسابك: {st.session_state.user_email}**")
            
            col1, col2 = st.columns(2)
            with col1:
                new_password = st.text_input("كلمة المرور الجديدة", type="password", key="user_new_pass")
            with col2:
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="user_confirm_pass")
            
            if st.button("تحديث كلمة المرور", key="user_update_pass"):
                if new_password and new_password == confirm_password:
                    update_user(
                        st.session_state.user_email,
                        password=new_password,
                        permission_type=None,
                        branch_filter_type=None,
                        branches=None
                    )
                    st.success("✅ تم تحديث كلمة المرور بنجاح")
                    st.info("🔐 سيتم تطبيق التغيير عند تسجيل الدخول下一次")
                    st.rerun()
                elif not new_password:
                    st.error("❌ يرجى إدخال كلمة المرور الجديدة")
                else:
                    st.error("❌ كلمات المرور غير متطابقة")
    
    st.markdown("---")
    
    # =============================================
    # باقي الإعدادات (تظهر فقط للمدير العام)
    # =============================================
    if not is_super_admin(st.session_state.user_email):
        st.warning("⚠️ الإعدادات المتقدمة متاحة للمديرين العامين فقط.")
        return
    
    # تبويبات الإعدادات للمدير
    settings_tabs = st.tabs(["📂 البيانات", "👥 المستخدمون", "📆 إعدادات أخرى"])
    
    # تبويب 1: تحميل البيانات
   # تبويب 1: تحميل البيانات
    with settings_tabs[0]:
        st.header("📂 تحديث ملفات البيانات")
        sales_file = st.file_uploader("رفع ملف المبيعات (Sales This Month.xlsx)", type=["xlsx"])
        target_file = st.file_uploader("رفع ملف الأهداف (Target This Month.xlsx)", type=["xlsx"])
        
        if st.button("تحميل ومعالجة"):
            if sales_file and target_file:
                try:
                    # تعديل مسارات الحفظ المؤقت لتفادي مشاكل الصلاحيات على سيرفر Hugging Face
                    with open("temp_sales.xlsx", "wb") as f:
                        f.write(sales_file.getbuffer()) # استخدام getbuffer() بدلاً من read() لضمان معالجة بايتات الملف الكبيرة بشكل آمن
                    with open("temp_target.xlsx", "wb") as f:
                        f.write(target_file.getbuffer())
                    
                    st.cache_resource.clear()
                    st.success("تم رفع الملفات وتحديث البيانات بنجاح!")
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ أثناء حفظ الملفات: {e}")
            else:
                st.error("يرجى رفع كلا الملفين")
        
        st.subheader("📌 معلومات الملفات المرفوعة")
        sales_path = "temp_sales.xlsx" if os.path.exists("temp_sales.xlsx") else "Sales (Naguib Selim) This Month.xlsx"
        target_path = "temp_target.xlsx" if os.path.exists("temp_target.xlsx") else "Target This Month.xlsx"
        st.write("**Sales data file:**", sales_path)
        st.write("**Target data file:**", target_path)
        min_date, max_date = get_sales_date_range(sales_path)
        if min_date and max_date:
            st.write(f"**Sales data range:** {min_date} to {max_date}")
    
    # تبويب 2: إدارة المستخدمين
    with settings_tabs[1]:
        st.header("👥 إدارة المستخدمين")
        users = get_all_users()
        
        # عرض جدول المستخدمين
        users_display = []
        for email, user_data in users.items():
            users_display.append({
                "البريد الإلكتروني": email,
                "نوع الصلاحية": PERMISSION_TYPES.get(user_data.get("permission_type"), "غير محدد"),
                "مصدر الفروع": "مبيعات الفرع (System)" if user_data.get("branch_filter_type") == "branch" else ("مندوب المبيعات" if user_data.get("branch_filter_type") == "sales_rep" else "-"),
                "الفروع": ", ".join(user_data.get("branches", [])) if user_data.get("branches") else "—"
            })
        st.dataframe(pd.DataFrame(users_display), use_container_width=True)
        
        # إضافة مستخدم جديد
        with st.expander("➕ إضافة مستخدم جديد"):
            col1, col2 = st.columns(2)
            with col1:
                new_email = st.text_input("البريد الإلكتروني", key="add_email")
                new_password = st.text_input("كلمة المرور", type="password", key="add_password")
            with col2:
                permission_type = st.selectbox(
                    "نوع الصلاحية", 
                    ["all_branches", "specific_branches"],
                    format_func=lambda x: PERMISSION_TYPES.get(x, x),
                    key="add_permission"
                )
            
            branch_filter_type = None
            branches = []
            
            if permission_type == "specific_branches":
                col1, col2 = st.columns(2)
                with col1:
                    branch_filter_type = st.radio(
                        "تصفية الفروع حسب:",
                        ["branch", "sales_rep"],
                        format_func=lambda x: "مبيعات الفرع (System)" if x == "branch" else "مندوب المبيعات",
                        key="add_filter_type"
                    )
                with col2:
                    branches_input = st.text_area("الفروع المسموحة (كل فرع في سطر)", key="add_branches")
                    branches = [b.strip() for b in branches_input.split("\n") if b.strip()]
            
            if st.button("إضافة المستخدم", key="btn_add_user"):
                if new_email and new_password:
                    add_user(new_email, new_password, permission_type, branch_filter_type, branches)
                    st.success("✅ تمت الإضافة بنجاح")
                    st.rerun()
                else:
                    st.error("❌ يرجى ملء جميع الحقول المطلوبة")
        
        # تعديل صلاحيات مستخدم
        with st.expander("⚙️ تعديل صلاحيات مستخدم"):
            if users:
                edit_email = st.selectbox("اختر المستخدم", list(users.keys()), key="edit_email")
                user_data = users[edit_email]
                
                st.subheader("الصلاحيات")
                current_perm_type = user_data.get("permission_type", "specific_branches")
                new_perm_type = st.selectbox(
                    "نوع الصلاحية",
                    ["all_branches", "specific_branches"],
                    index=["all_branches", "specific_branches"].index(current_perm_type),
                    format_func=lambda x: PERMISSION_TYPES.get(x, x),
                    key="edit_permission"
                )
                
                edit_branches = []
                edit_filter_type = None
                
                if new_perm_type == "specific_branches":
                    current_filter_type = user_data.get("branch_filter_type", "branch")
                    edit_filter_type = st.radio(
                        "تصفية الفروع حسب:",
                        ["branch", "sales_rep"],
                        index=["branch", "sales_rep"].index(current_filter_type),
                        format_func=lambda x: "مبيعات الفرع (System)" if x == "branch" else "مندوب المبيعات",
                        key="edit_filter_type",
                        horizontal=True
                    )
                    
                    current_branches = user_data.get("branches", [])
                    branches_input = st.text_area(
                        "الفروع المسموحة (كل فرع في سطر)",
                        value="\n".join(current_branches),
                        key="edit_branches"
                    )
                    edit_branches = [b.strip() for b in branches_input.split("\n") if b.strip()]
                
                if st.button("حفظ التعديلات", key="btn_update_user"):
                    update_user(
                        edit_email,
                        password=None,
                        permission_type=new_perm_type,
                        branch_filter_type=edit_filter_type,
                        branches=edit_branches if edit_branches else None
                    )
                    st.success("✅ تم تحديث الصلاحيات بنجاح")
                    st.rerun()
        
        # حذف مستخدم
        with st.expander("🗑️ حذف مستخدم"):
            if users:
                del_email = st.selectbox("اختر مستخدم للحذف", list(users.keys()), key="del_email")
                if st.button("حذف المستخدم", key="btn_delete_user"):
                    if del_email != "mahmoud.bayoumi@nstextile-eg.com":
                        delete_user(del_email)
                        st.success("✅ تم الحذف بنجاح")
                        st.rerun()
                    else:
                        st.error("❌ لا يمكن حذف حساب المدير الرئيسي")
    
    # تبويب 3: إعدادات أخرى
    with settings_tabs[2]:
        st.header("📆 إعدادات MTD")
        mtd_mode = st.radio(
            "أساس حساب MTD",
            ["Last sales date", "Today"],
            index=["Last sales date", "Today"].index(st.session_state.mtd_mode) if st.session_state.mtd_mode in ["Last sales date", "Today"] else 0,
        )
        st.session_state.mtd_mode = mtd_mode
        
        if mtd_mode == "Last sales date":
            default_month = st.session_state.mtd_month_length if st.session_state.mtd_month_length > 0 else 25
            month_length = st.number_input(
                "طول الشهر المستخدم للحساب",
                min_value=1,
                max_value=31,
                value=default_month,
                step=1,
                help="حدد عدد أيام الشهر الفعلي عند وجود عطل في الأيام الأخيرة."
            )
            st.session_state.mtd_month_length = month_length
        
        st.write("**نمط MTD الحالي:**", mtd_mode)
        if mtd_mode == "Last sales date":
            st.write(f"**طول الشهر المعين:** {st.session_state.mtd_month_length} يوم")

# واجهة Dashbard | Daily Sales | May 2026
def resolve_allowed_branches(sales_df, branch_column, user_branches, user_branch_filter_type):
    if not user_branches:
        return sorted(sales_df[branch_column].dropna().unique())
    # بما أن أسماء الفروع مطابقة تماماً في كلا العمودين (مبيعات الفرع (System) ومبيعات الفرع حسب البياع)، فإن قائمة الفروع المسموحة هي نفس قائمة فروع حساب المستخدم مباشرة دون الحاجة لأي ربط
    return sorted(user_branches)

# واجهة Dashbard | Daily Sales | May 2026
def dashboard_page():
    render_dashboard_header("Dashbard | Daily Sales | May 2026")
    
    try:
        sales_df, branch_target, rep_target = load_all_data()
    except Exception as e:
        st.error("لم يتم العثور على ملفات البيانات في المجلد، أو أن هناك مشكلة توافق في الملفات المرفوعة. يرجى رفع الملفات الصحيحة من صفحة الإعدادات.")
        return
    
    # --- 1. فلاتر تصفية البيانات في الشريط الجانبي ---
    st.sidebar.markdown("""
    <div class="sidebar-section-title" style="margin-top:8px;">
        <span class="material-symbols-rounded">store</span>
        فروع منشأتك
    </div>
    """, unsafe_allow_html=True)

    # اختيار مصدر الفرع: مبيعات الفرع (System) أم الفرع حسب مندوب المبيعات
    st.sidebar.markdown('<div class="filter-label"><span class="material-symbols-rounded">swap_horiz</span>مصدر الفرع</div>', unsafe_allow_html=True)
    branch_source = st.sidebar.radio(
        "مصدر المبيعات",
        ["مبيعات الفرع حسب البياع", "مبيعات الفرع (system)"],
        label_visibility="collapsed",
    )
    if branch_source == "مبيعات الفرع (system)":
        branch_column = "Branch"
        brand_column = "Brand"
    else:
        branch_column = "Branch based on sales reps"
        brand_column = "Brand based on sales reps"

    # فلتر الفروع حسب صلاحية المستخدم
    user_permission_type = get_user_permission_type(st.session_state.user_email)
    
    if user_permission_type in ["super_admin", "all_branches"] or not st.session_state.user_branches:
        allowed_branches = sorted(sales_df[branch_column].dropna().unique())
    else:
        allowed_branches = resolve_allowed_branches(
            sales_df,
            branch_column,
            st.session_state.user_branches,
            st.session_state.user_branch_filter_type,
        )
    # التحقق من ما إذا كان يجب إظهار فلتر البراند
    # إخفاء فلتر البراند للمستخدمين ذوي صلاحيات على فروع معينة
    show_brand_filter = user_permission_type in ["super_admin", "all_branches"]

    # فلتر البراند ونوع العميل في القائمة الجانبية
    if show_brand_filter:
        st.sidebar.markdown('<div class="filter-label"><span class="material-symbols-rounded">category</span>(Branch / Other Channel) قنوات البيع</div>', unsafe_allow_html=True)
        channel_category = st.sidebar.selectbox(
            "نوع القناة (Branch / Other Channel)",
            ["الكل", "Branches", "Other Channel"],
            key="channel_category_filter",
            label_visibility="collapsed"
        )
        
        # الحصول على الماركات المتاحة من البيانات
        all_brands_in_df = sorted(sales_df[brand_column].dropna().unique())
        if channel_category == "Branches":
            available_brands = [b for b in all_brands_in_df if b in ["EXP", "NS", "ED", "Domyat"]]
        elif channel_category == "Other Channel":
            available_brands = [b for b in all_brands_in_df if b in ["Shop IN Shop", "Other Channel"]]
        else:
            available_brands = all_brands_in_df
            
        brand_options = ["الكل"] + available_brands
        st.sidebar.markdown('<div class="filter-label"><span class="material-symbols-rounded">shopping_bag</span>البراند</div>', unsafe_allow_html=True)
        brand_filter = st.sidebar.selectbox("البراند", brand_options, label_visibility="collapsed")
        
        # حصر خيارات الفروع حسب البراند المختارة ومع مراعاة صلاحيات المستخدم
        if brand_filter == "الكل":
            if channel_category == "Branches":
                branches_for_brand = list(sales_df[sales_df[brand_column].isin(["EXP", "NS", "ED", "Domyat"])][branch_column].dropna().unique())
            elif channel_category == "Other Channel":
                branches_for_brand = list(sales_df[sales_df[brand_column].isin(["Shop IN Shop", "Other Channel"])][branch_column].dropna().unique())
            else:
                branches_for_brand = list(sales_df[branch_column].dropna().unique())
        else:
            branches_for_brand = list(sales_df[sales_df[brand_column] == brand_filter][branch_column].dropna().unique())
        
        # تصفية الفروع من allowed_branches المحسوبة بناءً على صلاحيات المستخدم
        if user_permission_type in ["super_admin", "all_branches"] or not st.session_state.user_branches:
            branch_options = sorted(branches_for_brand)
        else:
            # استخدام allowed_branches فقط - التي تم حسابها مع مراعاة صلاحيات المستخدم وتحويل الأعمدة
            branch_options = sorted([b for b in allowed_branches if b in branches_for_brand])
            
        branch_choice_options = ["الكل"] + branch_options
        st.sidebar.markdown('<div class="filter-label"><span class="material-symbols-rounded">location_on</span>القطاع</div>', unsafe_allow_html=True)
        branch_choice = st.sidebar.selectbox("الفرع", branch_choice_options, label_visibility="collapsed")
    else:
        # اختيار تلقائي "الكل" للعلامة التجارية عند إخفائها للمستخدمين ذوي صلاحيات محدودة
        channel_category = "الكل"
        brand_filter = "الكل"
        # حصر خيارات الفروع حسب الفروع المسموحة فقط
        branches_for_brand = list(sales_df[branch_column].dropna().unique())
        # استخدام allowed_branches فقط (التي تم حسابها بناءً على صلاحيات المستخدم)
        branch_options = sorted([b for b in allowed_branches if b in branches_for_brand])
        
        branch_choice_options = ["الكل"] + branch_options
        st.sidebar.markdown('<div class="filter-label"><span class="material-symbols-rounded">location_on</span>القطاع</div>', unsafe_allow_html=True)
        branch_choice = st.sidebar.selectbox("الفرع", branch_choice_options, label_visibility="collapsed")
        
    st.sidebar.markdown('<div class="filter-label"><span class="material-symbols-rounded">group</span>نوع التسجيل</div>', unsafe_allow_html=True)
    cust_filter = st.sidebar.selectbox("نوع العميل", ["الكل", "B2B", "B2C"], label_visibility="collapsed")

    # --- 2. بيانات المبيعات MTD ---
    st.sidebar.markdown("""
    <div class="sidebar-section-title" style="margin-top:16px;">
        <span class="material-symbols-rounded">bar_chart</span>
        بيانات المبيعات (MTD)
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="filter-label"><span class="material-symbols-rounded">date_range</span>طول الفترة المستخدم</div>', unsafe_allow_html=True)
    month_length_choice = st.sidebar.radio(
        "طول الشهر المستخدم للحساب",
        ["25 يوم", "عدد أيام الشهر الفعلية"],
        index=0 if st.session_state.mtd_month_length == 25 else 1,
        label_visibility="collapsed",
    )
    
    if month_length_choice == "25 يوم":
        st.session_state.mtd_month_length = 25
    else:
        st.session_state.mtd_month_length = 0
    
    # MTD Info Cards
    import calendar as _cal_mod
    _today = datetime.today()
    _month_total_days = _cal_mod.monthrange(_today.year, _today.month)[1]
    _used_length = st.session_state.mtd_month_length if st.session_state.mtd_month_length > 0 else _month_total_days
    _elapsed = min(_today.day, _used_length)
    _remaining = max(0, _used_length - _elapsed)
    
    st.sidebar.markdown(f"""
    <div class="mtd-info-grid">
        <div class="mtd-info-item">
            <div class="mtd-info-label">طول الفترة المستخدم</div>
            <div class="mtd-info-value">
                <span class="material-symbols-rounded">schedule</span>
                {_elapsed} يوم {_used_length}
            </div>
        </div>
        <div class="mtd-info-item">
            <div class="mtd-info-label">عدد أيام الفترة المتبقية</div>
            <div class="mtd-info-value" style="color:#f59e0b;">
                <span class="material-symbols-rounded">hourglass_top</span>
                {_remaining} يوم {_remaining}
            </div>
        </div>
        <div class="mtd-info-item">
            <div class="mtd-info-label">حالة الفترة الحالية</div>
            <div class="mtd-status-active">
                <span class="material-symbols-rounded" style="font-size:14px;">bolt</span>
                نشطة
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Footer
    st.sidebar.markdown("""
    <div class="sidebar-footer">
        <p>المشروع تم بواسطة</p>
        <p><span class="heart">💙</span>Mahmoud Bayoumi</p>
    </div>
    """, unsafe_allow_html=True)

    # تحويل اختيار الفرع إلى قائمة فروع مستخدمة (مطلوب من compute_kpis)
    if branch_choice == "الكل":
        selected_branches = branch_options
    else:
        selected_branches = [branch_choice]

    # إنشاء نسخة مفلترة من بيانات المبيعات تتفاعل مع كل الفلاتر
    filtered_sales = sales_df.copy()
    if selected_branches:
        filtered_sales = filtered_sales[filtered_sales[branch_column].isin(selected_branches)]
    if cust_filter and cust_filter != "الكل":
        filtered_sales = filtered_sales[filtered_sales["Customer Type"] == cust_filter]
    
    if brand_filter and brand_filter != "الكل":
        filtered_sales = filtered_sales[filtered_sales[brand_column] == brand_filter]
    elif channel_category == "Branch":
        filtered_sales = filtered_sales[filtered_sales[brand_column].isin(["EXP", "NS", "ED", "Domyat"])]
    elif channel_category == "Other Channel":
        filtered_sales = filtered_sales[filtered_sales[brand_column].isin(["Shop IN Shop", "Other Channel"])]

    # تحديد فلتر البراند الممرر لـ compute_kpis
    kpis_brand_arg = None
    if brand_filter and brand_filter != "الكل":
        kpis_brand_arg = brand_filter
    elif channel_category == "Branch":
        kpis_brand_arg = ["EXP", "NS", "ED", "Domyat"]
    elif channel_category == "Other Channel":
        kpis_brand_arg = ["Shop IN Shop", "Other Channel"]

    # حساب المؤشرات الرئيسية باستخدام الفروع المختارة والفلترة حسب البراند
    factor = get_mtd_factor(st.session_state.mtd_mode, sales_df, st.session_state.mtd_month_length)
    kpis = compute_kpis(
        sales_df,
        branch_target,
        selected_branches,
        None if cust_filter=="الكل" else cust_filter,
        kpis_brand_arg,
        factor,
        branch_col=branch_column,
        brand_col=brand_column,
    )
    
    # =============================================
    # تصميم احترافي لبطاقات KPI - احدث الداشبورد
    # =============================================

    # استخدام html و css لتنسيق حديث
    st.markdown("""
    <style>
    /* تنسيقات البطاقات الحديثة */
    .kpi-card {
        border-radius: 20px;
        padding: 1.1rem 1.3rem;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px -5px rgba(0,0,0,0.12), 0 8px 10px -6px rgba(0,0,0,0.04);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        border: 1px solid rgba(255,255,255,0.15);
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
        position: relative;
        overflow: hidden;
    }

    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
        animation: shimmer 5s ease-in-out infinite;
        pointer-events: none;
    }

    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 32px -8px rgba(0,0,0,0.22);
        border-color: rgba(255,255,255,0.25);
    }

    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        color: rgba(255,255,255,0.7);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        line-height: 1.2;
        margin-bottom: 0.25rem;
    }

    .kpi-sub {
        font-size: 0.82rem;
        color: rgba(255,255,255,0.7);
        display: flex;
        align-items: center;
        gap: 5px;
        font-weight: 600;
    }

    .kpi-trend-up {
        color: #4ade80;
        font-weight: 800;
        font-size: 0.92rem;
    }

    .kpi-trend-down {
        color: #f87171;
        font-weight: 800;
        font-size: 0.92rem;
    }

    /* ألوان مختلفة لكل بطاقة */
    .card-sales { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
    .card-quantity { background: linear-gradient(135deg, #134e5e 0%, #71b280 100%); }
    .card-invoices { background: linear-gradient(135deg, #c31432 0%, #240b36 100%); }
    .card-atv { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); }
    .card-return { background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%); }
    .card-customers { background: linear-gradient(135deg, #aa4b6b 0%, #6b6b83 100%); }
    .card-discount { background: linear-gradient(135deg, #3a1c71 0%, #d76d77 100%); }

    /* Responsive KPI grid — auto-fit ensures cards never get too narrow */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .kpi-row .kpi-card {
        margin: 0;
    }

    .kpi-row .kpi-value {
        font-size: clamp(1.15rem, 1.6vw, 1.6rem);
    }

    .kpi-row .kpi-title {
        font-size: clamp(0.62rem, 0.85vw, 0.8rem);
    }

    .kpi-row .kpi-sub {
        font-size: clamp(0.6rem, 0.75vw, 0.72rem);
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== Build all KPI card data =====
    sales_ach = kpis.get('Sales Ach%', 0)
    qty_ach = kpis.get('Qty Ach%', 0)
    inv_ach = kpis.get('Invoices Ach%', 0)
    atv_ach = kpis.get('ATV Ach%', 0)
    return_val = kpis.get('Return', 0)
    return_ratio = kpis.get('Return Ratio', 0)
    customers = kpis.get('Customers', 0)
    discount = kpis.get('Discount', 0)
    discount_ratio = kpis.get('Discount Ratio', 0)

    def _trend(val, threshold=70):
        up = val >= threshold
        icon = 'trending_up' if up else 'trending_down'
        css = 'kpi-trend-up' if up else 'kpi-trend-down'
        return f'<span class="{css}"><span class="material-symbols-rounded trend-icon">{icon}</span> {val:.1f}%</span>'

    def _warn(ratio):
        if ratio > 0.05:
            return '<span class="material-symbols-rounded trend-icon" style="color:#fbbf24;">warning</span>'
        return '<span class="material-symbols-rounded trend-icon" style="color:#4ade80;">check_circle</span>'

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card card-sales" style="animation-delay:0.05s">
            <div class="kpi-title"><span class="material-symbols-rounded kpi-icon">payments</span> Sales Amount</div>
            <div class="kpi-value">{kpis['Sales Amount']:,.0f} <span style="font-size:0.7em">جنيه</span></div>
            <div class="kpi-sub">الهدف: {kpis['Target Sales']:,.0f} {_trend(sales_ach)}</div>
        </div>
        <div class="kpi-card card-quantity" style="animation-delay:0.1s">
            <div class="kpi-title"><span class="material-symbols-rounded kpi-icon">inventory_2</span> Quantity</div>
            <div class="kpi-value">{kpis['Quantity']:,.0f}</div>
            <div class="kpi-sub">الهدف: {kpis['Target Quantity']:,.0f} {_trend(qty_ach)}</div>
        </div>
        <div class="kpi-card card-invoices" style="animation-delay:0.15s">
            <div class="kpi-title"><span class="material-symbols-rounded kpi-icon">receipt_long</span> Invoices</div>
            <div class="kpi-value">{kpis['Invoices']:,.0f}</div>
            <div class="kpi-sub">الهدف: {kpis['Target Invoices']:,.0f} {_trend(inv_ach)}</div>
        </div>
        <div class="kpi-card card-atv" style="animation-delay:0.2s">
            <div class="kpi-title"><span class="material-symbols-rounded kpi-icon">point_of_sale</span> ATV</div>
            <div class="kpi-value">{kpis['ATV']:,.0f} <span style="font-size:0.7em">جنيه</span></div>
            <div class="kpi-sub">الهدف: {kpis['Target ATV']:,.0f} {_trend(atv_ach, 100)}</div>
        </div>
        <div class="kpi-card card-return" style="animation-delay:0.25s">
            <div class="kpi-title"><span class="material-symbols-rounded kpi-icon">assignment_return</span> Returns</div>
            <div class="kpi-value" style="color:{'#f87171' if return_val < 0 else 'white'}">{return_val:,.0f} <span style="font-size:0.7em">جنيه</span></div>
            <div class="kpi-sub">نسبة: {return_ratio:.1%} {_warn(return_ratio)}</div>
        </div>
        <div class="kpi-card card-customers" style="animation-delay:0.3s">
            <div class="kpi-title"><span class="material-symbols-rounded kpi-icon">groups</span> Customer</div>
            <div class="kpi-value">{customers:,.0f}</div>
            <div class="kpi-sub">العملاء النشطين هذا الشهر</div>
        </div>
        <div class="kpi-card card-discount" style="animation-delay:0.35s">
            <div class="kpi-title"><span class="material-symbols-rounded kpi-icon">sell</span> Discount</div>
            <div class="kpi-value">{discount:,.0f} <span style="font-size:0.7em">جنيه</span></div>
            <div class="kpi-sub">نسبة الخصم: {discount_ratio:.1%}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Daily sales chart with achievement percentage (صافي = مبيعات - مرتجعات)
    section_header("bar_chart", "Daily Sales & Achievement Ratio")
    
    # 1. تحديد الشهر والسنة بناءً على البيانات أو التاريخ الحالي
    import calendar
    today = datetime.today()
    if not sales_df.empty and "Date" in sales_df.columns:
        max_date = sales_df["Date"].dropna().max()
        if pd.notna(max_date):
            year, month = max_date.year, max_date.month
        else:
            year, month = today.year, today.month
    else:
        year, month = today.year, today.month

    # 2. إنشاء جميع أيام الشهر بالكامل
    last_day = calendar.monthrange(year, month)[1]
    all_dates = pd.date_range(start=f"{year}-{month:02d}-01", end=f"{year}-{month:02d}-{last_day}")
    full_month_df = pd.DataFrame({"Date": all_dates})
    full_month_df["Date"] = full_month_df["Date"].dt.normalize()
    
    # 3. تجميع المبيعات بعد تسوية التاريخ
    sales_for_chart = filtered_sales[filtered_sales["Sales Type"].isin(["Sales", "Return"])].copy()
    if not sales_for_chart.empty:
        sales_for_chart["Date_Normalized"] = pd.to_datetime(sales_for_chart["Date"]).dt.normalize()
        daily_sales_grouped = sales_for_chart.groupby("Date_Normalized")["Total After Disc"].sum().reset_index()
        daily_sales_grouped.rename(columns={"Date_Normalized": "Date"}, inplace=True)
    else:
        daily_sales_grouped = pd.DataFrame(columns=["Date", "Total After Disc"])
        
    # 4. دمج البيانات لضمان وجود كل أيام الشهر
    daily_sales = pd.merge(full_month_df, daily_sales_grouped, on="Date", how="left")
    daily_sales["Total After Disc"] = daily_sales["Total After Disc"].fillna(0)
    
    # 5. حساب الهدف اليومي ونسبة الإنجاز
    current_day = datetime.today().day
    target_daily = kpis["Target Sales"] / current_day if current_day > 0 else 0
    daily_sales["Target daily"] = target_daily
    daily_sales["Achievement %"] = daily_sales.apply(
        lambda row: (row["Total After Disc"] / row["Target daily"] * 100) if row["Target daily"] else 0,
        axis=1,
    )
    daily_sales["Date Label"] = daily_sales["Date"].dt.strftime("%d %b<br>%a")

    # Prepare data for animated chart
    labels_list = daily_sales["Date Label"].tolist()
    sales_list = [round(v, 0) for v in daily_sales["Total After Disc"].tolist()]
    ach_list = [round(v, 1) for v in daily_sales["Achievement %"].tolist()]
    y1_max = max(sales_list) * 1.15 if sales_list else 100
    y2_max = max(max(ach_list) * 1.2, 100) if ach_list else 100

    animated_chart_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Outfit', sans-serif; background: transparent; overflow: hidden; }
        #chart-wrapper {
            opacity: 0;
            transform: translateY(40px);
            transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                        transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }
        #chart-wrapper.revealed {
            opacity: 1;
            transform: translateY(0);
        }
        /* Lock bar hover styles with high-performance CSS transition instead of JS redraw */
        #daily-chart .point path {
            transition: fill 0.15s ease, stroke 0.15s ease !important;
        }
        #daily-chart .point path:hover {
            fill: #818cf8 !important;
            stroke: #818cf8 !important;
        }
    </style>
</head>
<body>
    <div id="chart-wrapper">
        <div id="daily-chart"></div>
    </div>
    <script>
        const labels = __LABELS__;
        const salesValues = __SALES__;
        const achievementValues = __ACH__;
        const y1Max = __Y1MAX__;
        const y2Max = __Y2MAX__;
        const N = labels.length;

        // Bar trace with actual values (stationary)
        const barTrace = {
            x: labels,
            y: salesValues,
            text: salesValues.map(v => v > 0 ? v.toLocaleString('en', {maximumFractionDigits:0}) : ''),
            textposition: 'outside',
            textfont: { size: 10, color: '#475569', family: 'Outfit, Cairo, sans-serif' },
            type: 'bar',
            marker: {
                color: salesValues.map(() => '#6366f1'),
                line: { width: 0 }
            },
            name: 'Sales',
            hovertemplate: '%{y:,.0f}<extra></extra>'
        };

        const lineTrace = {
            x: labels,
            y: Array(N).fill(null),
            mode: 'lines+markers',
            line: { color: '#f59e0b', width: 3, shape: 'spline' },
            marker: { color: '#d97706', size: 0, line: { color: 'white', width: 1.5 } },
            name: 'Achievement %',
            yaxis: 'y2',
            hovertemplate: '%{y:.1f}%<extra></extra>'
        };

        const layout = {
            title: { text: 'Daily Sales and Achievement Trend', font: { size: 15, color: '#334155' } },
            font: { family: 'Outfit, Cairo, sans-serif' },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            xaxis: {
                type: 'category',
                range: [-0.7, N - 0.3],
                tickangle: -45,
                fixedrange: true,
                linecolor: 'rgba(148,163,184,0.2)',
                tickfont: { size: 10, color: '#64748b' }
            },
            yaxis: {
                title: { text: 'Sales Amount', font: { size: 11, color: '#94a3b8' } },
                range: [0, y1Max],
                fixedrange: true,
                linecolor: 'rgba(148,163,184,0.2)',
                gridcolor: 'rgba(148,163,184,0.1)',
                gridwidth: 1,
                griddash: 'dash',
                tickfont: { size: 10, color: '#64748b' }
            },
            yaxis2: {
                title: { text: 'Achievement %', font: { size: 11, color: '#94a3b8' } },
                overlaying: 'y',
                side: 'right',
                tickformat: '.0f',
                ticksuffix: '%',
                range: [0, y2Max],
                fixedrange: true,
                showgrid: false,
                tickfont: { size: 10, color: '#64748b' }
            },
            height: 500,
            margin: { l: 55, r: 65, t: 55, b: 90 },
            bargap: 0.22,
            legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1, font: { size: 11 } },
            hovermode: 'x unified'
        };

        Plotly.newPlot('daily-chart', [barTrace, lineTrace], layout, {
            displayModeBar: false,
            responsive: true
        });

        // Premium line-drawing animation (bars are stationary)
        async function runAnimation() {
            // Line draws progressively with growing markers
            const lineStagger = Math.max(30, Math.min(60, 600 / N));
            for (let i = 0; i < N; i++) {
                const yCurrent = achievementValues.map((v, j) => j <= i ? v : null);
                await Plotly.animate('daily-chart', {
                    data: [{}, {
                        x: labels,
                        y: yCurrent,
                        marker: { size: 8, color: '#d97706', line: { color: 'white', width: 1.5 } }
                    }]
                }, {
                    transition: { duration: lineStagger, easing: 'cubic-in-out' },
                    frame: { duration: lineStagger, redraw: true }
                });
            }
        }

        // Entrance: container slide up, then chart animates
        setTimeout(() => {
            document.getElementById('chart-wrapper').classList.add('revealed');
        }, 100);
        setTimeout(runAnimation, 700);
    </script>
</body>
</html>
    """.replace('__LABELS__', json.dumps(labels_list)) \
       .replace('__SALES__', json.dumps(sales_list)) \
       .replace('__ACH__', json.dumps(ach_list)) \
       .replace('__Y1MAX__', str(y1_max)) \
       .replace('__Y2MAX__', str(y2_max))

    components.html(animated_chart_html, height=540)

    # المبيعات حسب البراند, Customer Type, and Top/Bottom Branches — 3 columns
    st.markdown("""
    <style>
    /* Chart card styling for the 3-column row */
    .chart-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px 16px 12px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 6px 16px rgba(0,0,0,0.04);
        border: 1px solid rgba(148,163,184,0.12);
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    .chart-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 12px 28px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .chart-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        border-radius: 16px 16px 0 0;
    }
    .card-brand::before { background: linear-gradient(90deg, #f59e0b, #f97316); }
    .card-cust::before { background: linear-gradient(90deg, #6366f1, #8b5cf6); }
    .card-branch::before { background: linear-gradient(90deg, #10b981, #34d399); }

    .chart-card-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Outfit', 'Cairo', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
        padding-top: 4px;
    }
    .chart-card-title .material-symbols-rounded {
        font-size: 22px;
        font-variation-settings: 'FILL' 1, 'wght' 600, 'GRAD' 0, 'opsz' 24;
    }
    .card-brand .chart-card-title .material-symbols-rounded { color: #f59e0b; }
    .card-cust .chart-card-title .material-symbols-rounded { color: #6366f1; }
    .card-branch .chart-card-title .material-symbols-rounded { color: #10b981; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown('<div class="chart-card card-brand"><div class="chart-card-title"><span class="material-symbols-rounded">shopping_bag</span> المبيعات حسب البراند</div>', unsafe_allow_html=True)
        brand_sales_df = sales_df.copy()
        if channel_category == "Branch":
            brand_sales_df = brand_sales_df[brand_sales_df[brand_column].isin(["EXP", "NS", "ED", "Domyat"])]
        elif channel_category == "Other Channel":
            brand_sales_df = brand_sales_df[brand_sales_df[brand_column].isin(["Shop IN Shop", "Other Channel"])]
        
        brand_sales = brand_sales_df[brand_sales_df["Sales Type"].isin(["Sales", "Return"])].groupby(brand_column)["Total After Disc"].sum()
        
        brand_labels = brand_sales.index.tolist()
        brand_values = [round(v, 0) for v in brand_sales.values.tolist()]
        brand_colors = ["#6366f1", "#10b981", "#ec4899", "#f59e0b", "#8b5cf6", "#ef4444"]

        brand_html = """
<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Outfit',sans-serif;background:transparent;overflow:hidden}
#wrap{opacity:0;transition:opacity 0.7s cubic-bezier(0.16,1,0.3,1)}
#wrap.show{opacity:1}
</style></head><body>
<div id="wrap"><div id="chart"></div></div>
<script>
const labels=__B_LABELS__,values=__B_VALUES__,
colors=__B_COLORS__.slice(0,labels.length);
Plotly.newPlot('chart',[{
    values:values,labels:labels,type:'pie',hole:0.55,
    textinfo:'percent+label',textposition:'outside',
    marker:{colors:colors,line:{color:'#fff',width:2}},
    hoverinfo:'label+value+percent',
    rotation:-90,
    pull:Array(labels.length).fill(0),
    domain:{x:[0.3,1],y:[0.05,0.95]},
    textfont:{size:10}
}],{
    height:400,margin:{l:10,r:10,t:15,b:15},
    font:{family:'Outfit, Cairo, sans-serif'},
    plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)',
    legend:{orientation:'v',yanchor:'middle',y:0.5,xanchor:'left',x:-0.02,font:{size:10},tracegroupgap:2},
    showlegend:true
},{displayModeBar:false,responsive:true});

// Animate: rotate from -180 to 0
setTimeout(()=>{document.getElementById('wrap').classList.add('show')},100);
setTimeout(async()=>{
    for(let r=-180;r<=0;r+=12){
        await Plotly.animate('chart',{data:[{rotation:r}]},{
            transition:{duration:25,easing:'cubic-in-out'},
            frame:{duration:25,redraw:true}
        });
    }
},500);
</script></body></html>
        """.replace('__B_LABELS__', json.dumps(brand_labels)) \
           .replace('__B_VALUES__', json.dumps(brand_values)) \
           .replace('__B_COLORS__', json.dumps(brand_colors))
        components.html(brand_html, height=400)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card card-cust"><div class="chart-card-title"><span class="material-symbols-rounded">groups</span> المبيعات حسب نوع العميل</div>', unsafe_allow_html=True)
        cust_sales = filtered_sales[filtered_sales["Sales Type"].isin(["Sales", "Return"])].groupby("Customer Type")["Total After Disc"].sum()
        total_cust = cust_sales.sum()
        cust_percent = (cust_sales / total_cust * 100).round(1)

        cust_labels = cust_sales.index.tolist()
        cust_values = [round(v, 0) for v in cust_sales.values.tolist()]
        cust_pcts = [f"{p:.1f}%" for p in cust_percent]
        cust_color_map = {"B2B": "#6366f1", "B2C": "#10b981"}
        cust_colors_list = [cust_color_map.get(l, "#6366f1") for l in cust_labels]

        cust_html = """
<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Outfit',sans-serif;background:transparent;overflow:hidden}
#wrap{opacity:0;transition:opacity 0.7s cubic-bezier(0.16,1,0.3,1)}
#wrap.show{opacity:1}
</style></head><body>
<div id="wrap"><div id="chart"></div></div>
<script>
const labels=__C_LABELS__,values=__C_VALUES__,pcts=__C_PCTS__,colors=__C_COLORS__;
const N=labels.length;
const yMax=__C_YMAX__;

Plotly.newPlot('chart',[{
    x:labels,y:Array(N).fill(0),type:'bar',
    text:Array(N).fill(''),textposition:'outside',
    textfont:{size:12,color:'#1e293b',family:'Outfit, Cairo, sans-serif'},
    marker:{color:colors,line:{width:0}},
    hovertemplate:'%{y:,.0f}<extra></extra>'
}],{
    height:400,margin:{l:50,r:30,t:20,b:60},
    font:{family:'Outfit, Cairo, sans-serif'},
    plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)',
    showlegend:false,
    xaxis:{fixedrange:true,linecolor:'rgba(148,163,184,0.2)',tickfont:{size:11,color:'#64748b'},title:{text:'نوع العميل',font:{size:11,color:'#94a3b8'}}},
    yaxis:{fixedrange:true,range:[0,yMax*1.15],linecolor:'rgba(148,163,184,0.2)',gridcolor:'rgba(148,163,184,0.1)',gridwidth:1,griddash:'dash',tickfont:{size:10,color:'#64748b'},title:{text:'صافي المبيعات',font:{size:11,color:'#94a3b8'}}},
    bargap:0.35
},{displayModeBar:false,responsive:true});

setTimeout(()=>{document.getElementById('wrap').classList.add('show')},100);

// Bars grow up one by one
setTimeout(async()=>{
    const step=Math.max(900,750/N);
    for(let i=0;i<N;i++){
        const y=values.map((v,j)=>j<=i?v:0);
        const t=pcts.map((p,j)=>j<=i?p:'');
        await Plotly.animate('chart',{data:[{y:y,text:t}]},{
            transition:{duration:step,easing:'cubic-in-out'},
            frame:{duration:step,redraw:true}
        });
    }
    // Hover effect
    const el=document.getElementById('chart');
    el.on('plotly_hover',d=>{
        const idx=d.points[0].pointIndex;
        const c=colors.map((_,j)=>j===idx?colors[j]+'cc':colors[j]);
        Plotly.restyle('chart',{'marker.color':[c]},[0]);
    });
    el.on('plotly_unhover',()=>{
        Plotly.restyle('chart',{'marker.color':[colors]},[0]);
    });
},500);
</script></body></html>
        """.replace('__C_LABELS__', json.dumps(cust_labels)) \
           .replace('__C_VALUES__', json.dumps(cust_values)) \
           .replace('__C_PCTS__', json.dumps(cust_pcts)) \
           .replace('__C_COLORS__', json.dumps(cust_colors_list)) \
           .replace('__C_YMAX__', str(max(cust_values) if cust_values else 1))
        components.html(cust_html, height=400)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="chart-card card-branch"><div class="chart-card-title"><span class="material-symbols-rounded">leaderboard</span> أكثر وأقل الفروع مبيعات</div>', unsafe_allow_html=True)

        # 1. تصفية أولية بناءً على نوع الحركة (بيع أو مرتجع)
        branch_brand_sales = filtered_sales[filtered_sales["Sales Type"].isin(["Sales", "Return"])].copy()

        # 2. تطبيق شروط القنوات والبراندات بشكل ذكي
        is_other_channel = (channel_category == "Other Channel") or (brand_filter in ["Shop IN Shop", "Other Channel"])
        
        if is_other_channel:
            branch_brand_sales = branch_brand_sales[branch_brand_sales[brand_column].isin(["Shop IN Shop", "Other Channel"])]
        else:
            branch_brand_sales = branch_brand_sales[branch_brand_sales[brand_column].isin(["EXP", "NS", "ED", "Domyat"])]

        # 3. حساب المبيعات لكل فرع بعد التصفية
        branch_sales = branch_brand_sales.groupby(branch_column)["Total After Disc"].sum().reset_index()
        branch_sales.columns = ["Branch", "Sales"]
        branch_sales = branch_sales.sort_values("Sales", ascending=False)

        # بقية كود الرسم البياني (Top5 و Bottom5) تستمر كما هي بدون تغيير...
        top5 = branch_sales.head(5)
        bottom5 = branch_sales.tail(5).sort_values("Sales", ascending=True)

        top5_labels = top5["Branch"].tolist()
        top5_values = [round(v, 0) for v in top5["Sales"].tolist()]
        bottom5_labels = bottom5["Branch"].tolist()
        bottom5_values = [round(v, 0) for v in bottom5["Sales"].tolist()]
        global_max = float(branch_sales["Sales"].max()) if len(branch_sales) > 0 else 1

        branch_rank_html = """
<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Outfit','Cairo',sans-serif;background:transparent;overflow:hidden}
#wrap{opacity:0;transition:opacity 0.7s cubic-bezier(0.16,1,0.3,1)}
#wrap.show{opacity:1}
.btn-row{display:flex;gap:6px;margin-bottom:10px;padding:0 4px}
.toggle-btn{
    display:inline-flex;align-items:center;gap:5px;
    padding:6px 14px;border-radius:8px;border:1.5px solid #e2e8f0;
    background:#fff;color:#64748b;font-family:'Outfit','Cairo',sans-serif;
    font-size:12px;font-weight:600;cursor:pointer;
    transition:all 0.3s cubic-bezier(0.16,1,0.3,1);
}
.toggle-btn:hover{border-color:#6366f1;color:#6366f1;transform:translateY(-1px)}
.toggle-btn.active{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border-color:transparent;box-shadow:0 4px 15px rgba(99,102,241,0.3)}
.toggle-btn .material-symbols-rounded{font-size:16px;font-family:'Material Symbols Rounded'!important;font-variation-settings:'FILL' 1,'wght' 500,'GRAD' 0,'opsz' 24}
</style></head><body>
<div id="wrap">
    <div class="btn-row">
        <button class="toggle-btn active" id="btn-top" onclick="showTop()">
            <span class="material-symbols-rounded">trending_up</span> Top
        </button>
        <button class="toggle-btn" id="btn-bottom" onclick="showBottom()">
            <span class="material-symbols-rounded">trending_down</span> Bottom
        </button>
    </div>
    <div id="chart"></div>
</div>
<script>
const topLabels=__TOP_LABELS__,topValues=__TOP_VALUES__;
const bottomLabels=__BOT_LABELS__,bottomValues=__BOT_VALUES__;
const globalMax=__GLOBAL_MAX__;
let currentView='top';

const topColors=topValues.map((_,i)=>{
    const colors=['#10b981','#34d399','#6ee7b7','#6ee7b7','#6ee7b7'];
    return colors[i]||colors[4];
});
const bottomColors=bottomValues.map((_,i)=>{
    const colors=['#ef4444','#ef4444','#f87171','#fca5a5','#fca5a5'];
    return colors[i]||colors[4];
});

function makeTrace(labels,values,colors){
    return {
        y:labels,x:values,type:'bar',orientation:'h',
        text:values.map(v=>v.toLocaleString('en',{maximumFractionDigits:0})),
        textposition:'inside',
        insidetextanchor:'end',
        textfont:{size:14,color:'#fff',family:'Outfit, Cairo, sans-serif',weight:'bold'},
        marker:{color:colors,line:{width:0},cornerradius:4},
        hovertemplate:'%{y}: %{x:,.0f}<extra></extra>'
    };
}

const layout={
    height:350,margin:{l:140,r:15,t:10,b:30},
    font:{family:'Outfit, Cairo, sans-serif'},
    plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)',
    xaxis:{fixedrange:true,range:[0,globalMax*1.15],visible:false},
    yaxis:{fixedrange:true,autorange:'reversed',tickfont:{size:13,color:'#334155',weight:'bold'},linecolor:'rgba(0,0,0,0)'},
    showlegend:false,bargap:0.25
};

Plotly.newPlot('chart',[makeTrace(topLabels,Array(5).fill(0),topColors)],layout,{displayModeBar:false,responsive:true});

async function animateBars(labels,values,colors){
    const N=labels.length;
    Plotly.react('chart',[makeTrace(labels,Array(N).fill(0),colors)],layout,{displayModeBar:false,responsive:true});
    const step=120;
    for(let i=0;i<N;i++){
        const x=values.map((v,j)=>j<=i?v:0);
        const t=values.map((v,j)=>j<=i?v.toLocaleString('en',{maximumFractionDigits:0}):'');
        await Plotly.animate('chart',{data:[{x:x,text:t}]},{
            transition:{duration:step,easing:'cubic-in-out'},
            frame:{duration:step,redraw:true}
        });
    }
}

function showTop(){
    if(currentView==='top')return;
    currentView='top';
    document.getElementById('btn-top').classList.add('active');
    document.getElementById('btn-bottom').classList.remove('active');
    layout.xaxis.range=[0,globalMax*1.15];
    animateBars(topLabels,topValues,topColors);
}
function showBottom(){
    if(currentView==='bottom')return;
    currentView='bottom';
    document.getElementById('btn-bottom').classList.add('active');
    document.getElementById('btn-top').classList.remove('active');
    layout.xaxis.range=[0,Math.max(...bottomValues)*1.5||globalMax*0.5];
    animateBars(bottomLabels,bottomValues,bottomColors);
}

// Initial animation
setTimeout(()=>{document.getElementById('wrap').classList.add('show')},100);
setTimeout(()=>animateBars(topLabels,topValues,topColors),500);
</script></body></html>
        """.replace('__TOP_LABELS__', json.dumps(top5_labels)) \
           .replace('__TOP_VALUES__', json.dumps(top5_values)) \
           .replace('__BOT_LABELS__', json.dumps(bottom5_labels)) \
           .replace('__BOT_VALUES__', json.dumps(bottom5_values)) \
           .replace('__GLOBAL_MAX__', str(global_max))
        components.html(branch_rank_html, height=400)
        st.markdown('</div>', unsafe_allow_html=True)


    def pct_cell_style(val):
        import math
        try:
            v = float(val)
            if math.isnan(v):
                return ""
        except Exception:
            return ""
        if v < 70:
            return "color:white; background-color:#d9534f"
        elif v < 90:
            return "color:black; background-color:#f0ad4e"
        else:
            return "color:black; background-color:#5cb85c"

    def fmt_pct(val):
        import math
        try:
            v = float(val)
            if math.isnan(v):
                return ""
        except Exception:
            return ""
        return f"{v:.1f}%"

    section_header("account_tree", "Branch Performance")

    if "bp_view_mode" not in st.session_state:
        st.session_state.bp_view_mode = "sales"

    # Define active toggle button styles dynamically based on the active mode
    if st.session_state.bp_view_mode == "sales":
        btn_bg = "linear-gradient(135deg, #4f46e5, #6366f1)"
        btn_shadow = "0 4px 12px rgba(99, 102, 241, 0.4)"
        container_bg = "#0f172a"
        container_border = "1px solid rgba(99, 102, 241, 0.3)"
    else:
        btn_bg = "linear-gradient(135deg, #0d9488, #14b8a6)"
        btn_shadow = "0 4px 12px rgba(20, 184, 166, 0.4)"
        container_bg = "#0f172a"
        container_border = "1px solid rgba(20, 184, 166, 0.3)"

    sel = 'div[data-testid="stVerticalBlock"] > div:has(.bp-toggle-container-marker) + div div[data-testid="stHorizontalBlock"]'

    toggle_css = f"""<style>
    /* Container style for the toggle group */
    {sel} {{
        background: {container_bg} !important;
        border: {container_border} !important;
        padding: 6px !important;
        border-radius: 12px !important;
        display: inline-flex !important;
        gap: 8px !important;
        width: auto !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    }}
    
    /* Ensure columns do not stretch and stay inline */
    {sel} div[data-testid="stColumn"] {{
        width: auto !important;
        flex: none !important;
    }}
    
    /* Standardize button dimensions and typography */
    {sel} button {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        height: 40px !important;
        padding: 0 24px !important;
        font-family: 'Outfit', 'Cairo', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: none !important;
    }}
    
    /* Primary / Active toggle button */
    {sel} button[kind="primary"] {{
        background: {btn_bg} !important;
        color: #ffffff !important;
        box-shadow: {btn_shadow} !important;
    }}
    
    /* Secondary / Inactive toggle button */
    {sel} button[kind="secondary"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }}
    
    {sel} button[kind="secondary"]:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: #f1f5f9 !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }}
    
    /* Modern vector SVG icon for Sales (Dollar Symbol / Finance) */
    {sel} div[data-testid="stColumn"]:first-child button::before {{
        content: "";
        display: inline-block;
        width: 16px;
        height: 16px;
        background-color: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='12' y1='1' x2='12' y2='23'%3E%3C/line%3E%3Cpath d='M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'%3E%3C/path%3E%3C/svg%3E") no-repeat center;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='12' y1='1' x2='12' y2='23'%3E%3C/line%3E%3Cpath d='M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'%3E%3C/path%3E%3C/svg%3E") no-repeat center;
        -webkit-mask-size: contain;
        mask-size: contain;
    }}
    
    /* Modern vector SVG icon for Quantity (Package Box) */
    {sel} div[data-testid="stColumn"]:nth-child(2) button::before {{
        content: "";
        display: inline-block;
        width: 16px;
        height: 16px;
        background-color: currentColor;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'%3E%3C/path%3E%3Cpolyline points='3.27 6.96 12 12.01 20.73 6.96'%3E%3C/polyline%3E%3Cline x1='12' y1='22.08' x2='12' y2='12'%3E%3C/line%3E%3C/svg%3E") no-repeat center;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'%3E%3C/path%3E%3Cpolyline points='3.27 6.96 12 12.01 20.73 6.96'%3E%3C/polyline%3E%3Cline x1='12' y1='22.08' x2='12' y2='12'%3E%3C/line%3E%3C/svg%3E") no-repeat center;
        -webkit-mask-size: contain;
        mask-size: contain;
    }}
    </style>
<div class="bp-toggle-container-marker"></div>
    """

    st.markdown(toggle_css, unsafe_allow_html=True)

    bp_tog_col1, bp_tog_col2, _ = st.columns([0.8, 0.9, 8])
    with bp_tog_col1:
        if st.button("Sales", key="bp_sales_btn", use_container_width=True,
                     type="primary" if st.session_state.bp_view_mode == "sales" else "secondary"):
            st.session_state.bp_view_mode = "sales"
            st.rerun()
    with bp_tog_col2:
        if st.button("Quantity", key="bp_qty_btn", use_container_width=True,
                     type="primary" if st.session_state.bp_view_mode == "quantity" else "secondary"):
            st.session_state.bp_view_mode = "quantity"
            st.rerun()

    branch_perf = []
    branch_perf_qty = []
    def find_target_column(df, candidates):
        for c in candidates:
            if c in df.columns:
                return c
        return None

    # Sales target columns
    col_s_b2b = find_target_column(branch_target, ["Sales Target | B2B", "Sales Target B2B", "B2B MTD Target"])
    col_s_b2c = find_target_column(branch_target, ["Sales Target | B2C", "Sales Target B2C", "B2C MTD Target"])
    col_s_total = find_target_column(branch_target, ["Sales Target | TOTAL", "Sales Target TOTAL", "Total Target"])

    # Quantity target columns
    col_q_b2b = find_target_column(branch_target, ["Quantity Target | B2B", "Quantity Target B2B"])
    col_q_b2c = find_target_column(branch_target, ["Quantity Target | B2C", "Quantity Target B2C"])
    col_q_total = find_target_column(branch_target, ["Quantity Target | TOTAL", "Quantity Target TOTAL"])

    for branch in selected_branches:
        target_row = branch_target[branch_target["Branch"] == branch]
        if target_row.empty:
            continue

        target_b2b = float(target_row[col_s_b2b].values[0]) * factor if col_s_b2b else 0
        target_b2c = float(target_row[col_s_b2c].values[0]) * factor if col_s_b2c else 0
        target_total = float(target_row[col_s_total].values[0]) * factor if col_s_total else 0

        qt_b2b = float(target_row[col_q_b2b].values[0]) * factor if col_q_b2b else 0
        qt_b2c = float(target_row[col_q_b2c].values[0]) * factor if col_q_b2c else 0
        qt_total = float(target_row[col_q_total].values[0]) * factor if col_q_total else 0

        if target_total == 0 and target_b2b == 0 and target_b2c == 0 and qt_total == 0 and qt_b2b == 0 and qt_b2c == 0:
            continue

        branch_data = filtered_sales[(filtered_sales[branch_column] == branch) & (filtered_sales["Sales Type"].isin(["Sales","Return"]))]
        sales_b2b = branch_data[branch_data["Customer Type"] == "B2B"]["Total After Disc"].sum()
        sales_b2c = branch_data[branch_data["Customer Type"] == "B2C"]["Total After Disc"].sum()
        sales_total = sales_b2b + sales_b2c

        branch_qty_data = filtered_sales[(filtered_sales[branch_column] == branch) & (filtered_sales["Sales Type"] == "Sales")]
        qty_b2b = branch_qty_data[branch_qty_data["Customer Type"] == "B2B"]["Qty"].sum() if "Qty" in filtered_sales.columns else 0
        qty_b2c = branch_qty_data[branch_qty_data["Customer Type"] == "B2C"]["Qty"].sum() if "Qty" in filtered_sales.columns else 0
        qty_total = qty_b2b + qty_b2c

        branch_perf.append({
            "Branch": branch,
            "B2B MTD Target": target_b2b, "Sales B2B": sales_b2b,
            "B2B %": (sales_b2b / target_b2b * 100) if target_b2b else None,
            "B2C MTD Target": target_b2c, "Sales B2C": sales_b2c,
            "B2C %": (sales_b2c / target_b2c * 100) if target_b2c else None,
            "Total Target": target_total, "Total Sales": sales_total,
            "Sales %": (sales_total / target_total * 100) if target_total else None,
        })
        branch_perf_qty.append({
            "Branch": branch,
            "B2B Qty Target": qt_b2b, "Qty B2B": qty_b2b,
            "B2B %": (qty_b2b / qt_b2b * 100) if qt_b2b else None,
            "B2C Qty Target": qt_b2c, "Qty B2C": qty_b2c,
            "B2C %": (qty_b2c / qt_b2c * 100) if qt_b2c else None,
            "Total Qty Target": qt_total, "Total Qty": qty_total,
            "Qty %": (qty_total / qt_total * 100) if qt_total else None,
        })

    # --- Sort branches by brand priority ---
    brand_priority = {
        "EXP": 0, "NS": 1, "ED": 2, "DOMYAT": 3, "DOMYAT/EXP": 3, 
        "SHOP IN SHOP": 4, "OTHER CHANNEL": 5, "AND OTHER": 6, "OTHER": 7
    }
    def _get_branch_brand(branch_name):
        """Get the brand for a branch from branch_target or sales data."""
        if "Brand" in branch_target.columns:
            row = branch_target[branch_target["Branch"] == branch_name]
            if not row.empty and pd.notna(row["Brand"].values[0]):
                return str(row["Brand"].values[0]).strip()
        # Fallback: check sales data
        br_data = filtered_sales[filtered_sales[branch_column] == branch_name]
        if not br_data.empty and brand_column in br_data.columns:
            return str(br_data[brand_column].mode().iloc[0]) if not br_data[brand_column].mode().empty else "ZZZ"
        return "ZZZ"

    def _brand_sort_key(item):
        brand = _get_branch_brand(item["Branch"])
        brand_upper = str(brand).upper().strip()
        # Find the priority by searching for substring or exact match
        for key, val in brand_priority.items():
            if key in brand_upper:
                return val
        return 99 # Default for any other brands

    branch_perf.sort(key=_brand_sort_key)
    branch_perf_qty.sort(key=_brand_sort_key)

    def _pct_badge(val):
        import math
        try:
            v = float(val)
            if math.isnan(v):
                return '<span class="bp-badge bp-na">-</span>'
        except Exception:
            return '<span class="bp-badge bp-na">-</span>'
        if v < 70:
            return f'<span class="bp-badge bp-red">{v:.1f}%</span>'
        elif v < 90:
            return f'<span class="bp-badge bp-amber">{v:.1f}%</span>'
        else:
            return f'<span class="bp-badge bp-green">{v:.1f}%</span>'

    def _fmt_num(val):
        import math
        try:
            v = float(val)
            if math.isnan(v):
                return "-"
        except Exception:
            return "-"
        return f"{v:,.0f}"

    def _raw_val(val):
        import math
        try:
            v = float(val)
            if math.isnan(v):
                return 0
            return v
        except Exception:
            return 0

    _BP_CSS_JS = """<style>
:root {
  --bp-primary: #6366f1;
  --bp-primary-rgb: 99, 102, 241;
  --bp-accent: #818cf8;
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Outfit','Cairo',sans-serif;background:transparent;margin:0;padding:0;}
.bp-scroll{width:100%;overflow-x:auto;overflow-y:auto;scrollbar-width:thin;scrollbar-color:var(--bp-primary) rgba(255,255,255,0.05)}
.bp-scroll::-webkit-scrollbar{width:8px;height:8px}
.bp-scroll::-webkit-scrollbar-track{background:rgba(255,255,255,0.03);border-radius:4px}
.bp-scroll::-webkit-scrollbar-thumb{background:rgba(var(--bp-primary-rgb),0.5);border-radius:4px;border:2px solid #0f172a}
.bp-scroll::-webkit-scrollbar-thumb:hover{background:rgba(var(--bp-primary-rgb),0.8)}
.bp-table{width:100%;border-collapse:separate;border-spacing:0;font-size:13px;border-radius:14px;border:1px solid rgba(var(--bp-primary-rgb),0.18);background:#0f172a}
.bp-group-row th{padding:0 8px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;border-bottom:none;position:sticky;top:0;z-index:4;background:#0f172a;height:35px;line-height:35px}
.bp-group-row th:first-child{border-top-left-radius:14px}
.bp-group-row th:last-child{border-top-right-radius:14px}
.bp-group-empty{background:#0f172a}
.bp-group-label{background:linear-gradient(135deg,rgba(var(--bp-primary-rgb),0.15),rgba(139,92,246,0.1));color:var(--bp-accent);text-align:center;border-left:1px solid rgba(var(--bp-primary-rgb),0.25);border-right:1px solid rgba(var(--bp-primary-rgb),0.25)}
.bp-header-row th{padding:0 10px;font-size:10.5px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(var(--bp-primary-rgb),0.2);position:sticky;top:35px;z-index:3;background:#0f172a;height:35px;line-height:35px}
.bp-sortable{cursor:pointer;user-select:none;transition:color 0.2s}
.bp-sortable:hover{color:var(--bp-accent) !important}
.bp-si{font-size:12px;opacity:0.35;transition:opacity 0.2s}
.bp-sortable.asc .bp-si,.bp-sortable.desc .bp-si{opacity:1;color:var(--bp-accent)}
.bp-col-branch{text-align:right;min-width:100px;white-space:nowrap}
.bp-col-num{text-align:center}
.bp-col-pct{text-align:center;min-width:72px}
.bp-table tbody tr{height:38px;transition:background 0.15s;border-bottom:1px solid rgba(148,163,184,0.06)}
.bp-table tbody td{border-bottom:1px solid rgba(148,163,184,0.06)}
.bp-table tbody tr:hover{background:rgba(var(--bp-primary-rgb),0.08)}
.bp-cell-branch{padding:0 12px;font-weight:600;color:#e2e8f0;text-align:right;white-space:nowrap;font-size:12px;height:38px;line-height:38px}
.bp-cell-num{padding:0 8px;text-align:center;color:#cbd5e1;font-variant-numeric:tabular-nums;font-weight:500;font-size:12px;height:38px;line-height:38px}
.bp-cell-pct{padding:0 4px;text-align:center;height:38px}
.bp-badge{display:inline-block;padding:3px 10px;border-radius:6px;font-weight:700;font-size:11px;min-width:52px;text-align:center}
.bp-na{color:#475569}
.bp-red{background:rgba(220,38,38,0.15);color:#fca5a5;border:1px solid rgba(220,38,38,0.25)}
.bp-amber{background:rgba(217,119,6,0.15);color:#fcd34d;border:1px solid rgba(217,119,6,0.25)}
.bp-green{background:rgba(22,163,74,0.15);color:#86efac;border:1px solid rgba(22,163,74,0.25)}
.bp-table tfoot td{position:sticky;bottom:0;z-index:4;background:#1e293b !important;border-top:2px solid rgba(var(--bp-primary-rgb),0.3) !important;height:40px;line-height:40px}
.bp-table tfoot td:first-child{border-bottom-left-radius:14px}
.bp-table tfoot td:last-child{border-bottom-right-radius:14px}
.bp-table tfoot .bp-cell-branch{font-weight:800;color:var(--bp-accent);font-size:12.5px}
.bp-table tfoot .bp-cell-num{font-weight:700;color:#e2e8f0}
</style>
<script>
function bpSort(tid,ci){
  var t=document.getElementById(tid);if(!t)return;
  var tb=t.querySelector('tbody');
  var rs=Array.from(tb.querySelectorAll('tr'));
  var ths=t.querySelectorAll('.bp-header-row th');
  var th=ths[ci];
  ths.forEach(function(h){h.classList.remove('asc','desc')});
  var d=th.dataset.sort==='asc'?'desc':'asc';
  th.dataset.sort=d;th.classList.add(d);
  rs.sort(function(a,b){
    var va=parseFloat(a.cells[ci].getAttribute('data-v'))||0;
    var vb=parseFloat(b.cells[ci].getAttribute('data-v'))||0;
    return d==='asc'?va-vb:vb-va;
  });
  while(tb.firstChild)tb.removeChild(tb.firstChild);
  rs.forEach(function(r){tb.appendChild(r)});
}
</script>"""

    def _build_perf_table(table_id, rows, groups, nice_labels, pct_cols, is_total_fn, max_visible=10, is_quantity_mode=False):
        """Build premium sortable HTML table as self-contained HTML for components.html."""
        theme_vars = """:root {
  --bp-primary: #14b8a6;
  --bp-primary-rgb: 20, 184, 166;
  --bp-accent: #2dd4bf;
}""" if is_quantity_mode else """:root {
  --bp-primary: #6366f1;
  --bp-primary-rgb: 99, 102, 241;
  --bp-accent: #818cf8;
}"""
        flat_cols = []
        for gn, gc in groups:
            flat_cols.extend(gc)
        branch_like = [c for c in flat_cols if c in ["Branch","Sales Rep"]]

        # Identify data rows vs total row
        data_rows = [r for r in rows if not is_total_fn(r)]
        total_rows = [r for r in rows if is_total_fn(r)]
        has_total = len(total_rows) > 0

        # Heights
        row_h = 38
        header_h = 75
        total_row_h = 40 if has_total else 0

        num_data = len(data_rows)
        visible_data = min(num_data, max_visible)

        # Capped height for scrolling container
        scroll_h = (visible_data * row_h) + header_h + total_row_h
        
        # Give iframe a generous height so it never shows its own scrollbar
        total_height = scroll_h + 30

        tbl = f'<div class="bp-scroll" style="height:{scroll_h}px; max-height:{scroll_h}px; overflow-y:auto;">'
        tbl += f'<table class="bp-table" id="{table_id}">'
        tbl += '<thead><tr class="bp-group-row">'
        for gn, gc in groups:
            cls = "bp-group-empty" if gn == "" else "bp-group-label"
            tbl += f'<th colspan="{len(gc)}" class="{cls}">{gn}</th>'
        tbl += '</tr><tr class="bp-header-row">'
        col_idx = 0
        for gn, gc in groups:
            for c in gc:
                sortable = c not in branch_like
                cls = "bp-col-branch" if c in branch_like else ("bp-col-pct" if c in pct_cols else "bp-col-num")
                if sortable:
                    tbl += f'<th class="{cls} bp-sortable" onclick="bpSort(\'{table_id}\',{col_idx})">{nice_labels.get(c,c)} <span class="bp-si">&#8693;</span></th>'
                else:
                    tbl += f'<th class="{cls}">{nice_labels.get(c,c)}</th>'
                col_idx += 1
        tbl += '</tr></thead><tbody>'
        for row in data_rows:
            tbl += '<tr>'
            for gn, gc in groups:
                for c in gc:
                    val = row.get(c, "")
                    raw = _raw_val(val)
                    if c in branch_like:
                        tbl += f'<td class="bp-cell-branch" data-v="0">{val}</td>'
                    elif c in pct_cols:
                        tbl += f'<td class="bp-cell-pct" data-v="{raw}">{_pct_badge(val)}</td>'
                    else:
                        tbl += f'<td class="bp-cell-num" data-v="{raw}">{_fmt_num(val)}</td>'
            tbl += '</tr>'
        tbl += '</tbody>'
        
        if total_rows:
            tbl += '<tfoot>'
            for row in total_rows:
                tbl += '<tr>'
                for gn, gc in groups:
                    for c in gc:
                        val = row.get(c, "")
                        raw = _raw_val(val)
                        if c in branch_like:
                            tbl += f'<td class="bp-cell-branch" data-v="0">{val}</td>'
                        elif c in pct_cols:
                            tbl += f'<td class="bp-cell-pct" data-v="{raw}">{_pct_badge(val)}</td>'
                        else:
                            tbl += f'<td class="bp-cell-num" data-v="{raw}">{_fmt_num(val)}</td>'
                tbl += '</tr>'
            tbl += '</tfoot>'
            
        tbl += '</table></div>'

        custom_css = _BP_CSS_JS.replace(":root {\n  --bp-primary: #6366f1;\n  --bp-primary-rgb: 99, 102, 241;\n  --bp-accent: #818cf8;\n}", theme_vars)
        full_html = '<!DOCTYPE html><html><head><meta charset="utf-8">' + custom_css + '</head><body>' + tbl + '</body></html>'
        return full_html, total_height


    bp_groups_sales = [
        ("", ["Branch"]),
        ("B2B", ["B2B MTD Target", "Sales B2B", "B2B %"]),
        ("B2C", ["B2C MTD Target", "Sales B2C", "B2C %"]),
        ("TOTAL", ["Total Target", "Total Sales", "Sales %"]),
    ]
    bp_groups_qty = [
        ("", ["Branch"]),
        ("B2B", ["B2B Qty Target", "Qty B2B", "B2B %"]),
        ("B2C", ["B2C Qty Target", "Qty B2C", "B2C %"]),
        ("TOTAL", ["Total Qty Target", "Total Qty", "Qty %"]),
    ]
    bp_nice = {
        "Branch": "BRANCH", "Sales Rep": "SALES REP",
        "B2B MTD Target": "TARGET", "Sales B2B": "ACTUAL", "B2B %": "ACH %",
        "B2C MTD Target": "TARGET", "Sales B2C": "ACTUAL", "B2C %": "ACH %",
        "Total Target": "TARGET", "Total Sales": "ACTUAL", "Sales %": "ACH %",
        "B2B Qty Target": "TARGET", "Qty B2B": "ACTUAL",
        "B2C Qty Target": "TARGET", "Qty B2C": "ACTUAL",
        "Total Qty Target": "TARGET", "Total Qty": "ACTUAL", "Qty %": "ACH %",
    }

    if st.session_state.bp_view_mode == "sales":
        if not branch_perf:
            st.info("No branch targets available for selected filters.")
        else:
            bp_df = pd.DataFrame(branch_perf)
            totals = bp_df[["B2B MTD Target","Sales B2B","B2C MTD Target","Sales B2C","Total Target","Total Sales"]].sum()
            totals_row = {
                "Branch": "\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a",
                "B2B MTD Target": totals["B2B MTD Target"], "Sales B2B": totals["Sales B2B"],
                "B2B %": (totals["Sales B2B"] / totals["B2B MTD Target"] * 100) if totals["B2B MTD Target"] else None,
                "B2C MTD Target": totals["B2C MTD Target"], "Sales B2C": totals["Sales B2C"],
                "B2C %": (totals["Sales B2C"] / totals["B2C MTD Target"] * 100) if totals["B2C MTD Target"] else None,
                "Total Target": totals["Total Target"], "Total Sales": totals["Total Sales"],
                "Sales %": (totals["Total Sales"] / totals["Total Target"] * 100) if totals["Total Target"] else None,
            }
            all_rows = branch_perf + [totals_row]
            html, h = _build_perf_table("bp-branch-s", all_rows, bp_groups_sales, bp_nice,
                                     ["B2B %","B2C %","Sales %"], lambda r: r["Branch"] == "\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a", is_quantity_mode=False)
            import time
            components.html(html + f"<!-- {time.time()} -->", height=h)
    else:
        if not branch_perf_qty:
            st.info("No branch quantity targets available for selected filters.")
        else:
            bq_df = pd.DataFrame(branch_perf_qty)
            totals_q = bq_df[["B2B Qty Target","Qty B2B","B2C Qty Target","Qty B2C","Total Qty Target","Total Qty"]].sum()
            totals_row_q = {
                "Branch": "\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a",
                "B2B Qty Target": totals_q["B2B Qty Target"], "Qty B2B": totals_q["Qty B2B"],
                "B2B %": (totals_q["Qty B2B"] / totals_q["B2B Qty Target"] * 100) if totals_q["B2B Qty Target"] else None,
                "B2C Qty Target": totals_q["B2C Qty Target"], "Qty B2C": totals_q["Qty B2C"],
                "B2C %": (totals_q["Qty B2C"] / totals_q["B2C Qty Target"] * 100) if totals_q["B2C Qty Target"] else None,
                "Total Qty Target": totals_q["Total Qty Target"], "Total Qty": totals_q["Total Qty"],
                "Qty %": (totals_q["Total Qty"] / totals_q["Total Qty Target"] * 100) if totals_q["Total Qty Target"] else None,
            }
            all_rows_q = branch_perf_qty + [totals_row_q]
            html_q, h_q = _build_perf_table("bp-branch-q", all_rows_q, bp_groups_qty, bp_nice,
                                       ["B2B %","B2C %","Qty %"], lambda r: r["Branch"] == "\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a", is_quantity_mode=True)
            import time
            components.html(html_q + f"<!-- {time.time()} -->", height=h_q)


    # Sales Rep Performance
    section_header("badge", "Sales Rep Performance")
    
    rep_cache_key = (
        branch_choice, 
        tuple(st.session_state.user_branches) if isinstance(st.session_state.user_branches, list) else st.session_state.user_branches,
        cust_filter, 
        brand_filter, 
        channel_category, 
        factor,
        user_permission_type,
        tuple(selected_branches) if isinstance(selected_branches, list) else selected_branches
    )
    
    if "rep_html_cache" in st.session_state and st.session_state.get("rep_cache_key") == rep_cache_key:
        html_rep, h_rep = st.session_state.rep_html_cache
        import time
        components.html(html_rep + f"<!-- cached {time.time()} -->", height=h_rep)
    else:
        rep_perf = []
        col_r_b2b = find_target_column(rep_target, ["Sales Target | B2B", "Sales Target B2B", "B2B MTD Target"])
        col_r_b2c = find_target_column(rep_target, ["Sales Target | B2C", "Sales Target B2C", "B2C MTD Target"])
        col_r_total = find_target_column(rep_target, ["Sales Target | TOTAL", "Sales Target TOTAL", "Total Target"])
    
        # Sales Rep Performance should always use 'Branch based on sales reps' as branch source
        rep_branch_col = "Branch based on sales reps"
        rep_brand_col = "Brand based on sales reps"
    
        # Determine which rep-based branches to include based on the current branch selection.
        if branch_choice == "الكل":
            selected_rep_branches = selected_branches
        else:
            selected_rep_branches = [branch_choice]
    
        # تصفية الفروع المسموحة للبياعين بناءً على صلاحيات فروع المستخدم (من عمود Branch based on sales reps)
        if user_permission_type not in ["super_admin", "all_branches"] and st.session_state.user_branches:
            selected_rep_branches = [b for b in selected_rep_branches if b in st.session_state.user_branches]
    
        # Build sales data for reps using rep-based branch mapping, include returns for net calculation
        sales_rep_data = sales_df[sales_df[rep_branch_col].isin(selected_rep_branches) & sales_df["Sales Type"].isin(["Sales", "Return"])].copy()
        # Apply customer-type filter if set
        if cust_filter and cust_filter != "الكل":
            sales_rep_data = sales_rep_data[sales_rep_data["Customer Type"] == cust_filter]
        # Apply brand filter using rep-based brand column
        if brand_filter and brand_filter != "الكل":
            sales_rep_data = sales_rep_data[sales_rep_data[rep_brand_col] == brand_filter]
        elif channel_category == "Branch":
            sales_rep_data = sales_rep_data[sales_rep_data[rep_brand_col].isin(["EXP", "NS", "ED", "Domyat"])]
        elif channel_category == "Other Channel":
            sales_rep_data = sales_rep_data[sales_rep_data[rep_brand_col].isin(["Shop IN Shop", "Other Channel"])]
    
        # Build complete list of (Sales Rep, Branch) combinations from targets only
        all_pairs = []
        target_pairs = set()
        if isinstance(rep_target, pd.DataFrame) and "Sales Rep" in rep_target.columns and "Branch" in rep_target.columns:
            # Filter rep_target by selected branches and brand
            filtered_rep_target = rep_target[rep_target["Branch"].isin(selected_rep_branches)].copy()
            if brand_filter and brand_filter != "الكل" and "Brand" in filtered_rep_target.columns:
                filtered_rep_target = filtered_rep_target[filtered_rep_target["Brand"] == brand_filter]
            elif channel_category == "Branch" and "Brand" in filtered_rep_target.columns:
                filtered_rep_target = filtered_rep_target[filtered_rep_target["Brand"].isin(["EXP", "NS", "ED", "Domyat"])]
            elif channel_category == "Other Channel" and "Brand" in filtered_rep_target.columns:
                filtered_rep_target = filtered_rep_target[filtered_rep_target["Brand"].isin(["Shop IN Shop", "Other Channel"])]
            
            for _, row in filtered_rep_target.iterrows():
                r = row["Sales Rep"]
                b = row["Branch"]
                if pd.notna(r) and pd.notna(b):
                    target_pairs.add((str(r).strip(), str(b).strip()))
    
        # Sort them by Branch brand priority, then by Branch name, then by Sales Rep name
        all_pairs = sorted(list(target_pairs), key=lambda x: (_brand_sort_key({"Branch": x[1]}), x[1], x[0]))
    
        for rep, branch in all_pairs:
            # Find targets for this rep in this branch
            rep_row = pd.DataFrame()
            if isinstance(rep_target, pd.DataFrame) and "Sales Rep" in rep_target.columns and "Branch" in rep_target.columns:
                rep_row = rep_target[
                    (rep_target["Sales Rep"].astype(str).str.strip() == rep) & 
                    (rep_target["Branch"].astype(str).str.strip() == branch)
                ]
            
            target_b2b = float(pd.to_numeric(rep_row[col_r_b2b], errors="coerce").fillna(0).sum()) * factor if col_r_b2b and not rep_row.empty else 0
            target_b2c = float(pd.to_numeric(rep_row[col_r_b2c], errors="coerce").fillna(0).sum()) * factor if col_r_b2c and not rep_row.empty else 0
            target_total = float(pd.to_numeric(rep_row[col_r_total], errors="coerce").fillna(0).sum()) * factor if col_r_total and not rep_row.empty else 0
    
            # Find actual sales for this rep in this branch
            rep_sales_df = sales_rep_data[
                (sales_rep_data["Sales Person"].astype(str).str.strip() == rep) & 
                (sales_rep_data[rep_branch_col].astype(str).str.strip() == branch)
            ]
            
            sales_b2b = rep_sales_df[rep_sales_df["Customer Type"] == "B2B"]["Total After Disc"].sum()
            sales_b2c = rep_sales_df[rep_sales_df["Customer Type"] == "B2C"]["Total After Disc"].sum()
            sales_total = sales_b2b + sales_b2c
    
            # Skip reps that have no target and no sales
            if target_total == 0 and target_b2b == 0 and target_b2c == 0 and sales_total == 0:
                continue
    
            rep_perf.append({
                "Branch": branch,
                "Sales Rep": rep,
                "B2B MTD Target": target_b2b,
                "Sales B2B": sales_b2b,
                "B2B %": (sales_b2b / target_b2b * 100) if target_b2b else None,
                "B2C MTD Target": target_b2c,
                "Sales B2C": sales_b2c,
                "B2C %": (sales_b2c / target_b2c * 100) if target_b2c else None,
                "Total Target": target_total,
                "Total Sales": sales_total,
                "Sales %": (sales_total / target_total * 100) if target_total else None,
            })
    
        if not rep_perf:
            st.info("No sales rep targets available for selected filters.")
        else:
            rp_df = pd.DataFrame(rep_perf)
            totals = rp_df[["B2B MTD Target","Sales B2B","B2C MTD Target","Sales B2C","Total Target","Total Sales"]].sum()
            totals_row = {
                "Branch": "", "Sales Rep": "\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a",
                "B2B MTD Target": totals["B2B MTD Target"], "Sales B2B": totals["Sales B2B"],
                "B2B %": (totals["Sales B2B"] / totals["B2B MTD Target"] * 100) if totals["B2B MTD Target"] else None,
                "B2C MTD Target": totals["B2C MTD Target"], "Sales B2C": totals["Sales B2C"],
                "B2C %": (totals["Sales B2C"] / totals["B2C MTD Target"] * 100) if totals["B2C MTD Target"] else None,
                "Total Target": totals["Total Target"], "Total Sales": totals["Total Sales"],
                "Sales %": (totals["Total Sales"] / totals["Total Target"] * 100) if totals["Total Target"] else None,
            }
            all_rep_rows = rep_perf + [totals_row]
            rep_groups = [
                ("", ["Branch", "Sales Rep"]),
                ("B2B", ["B2B MTD Target", "Sales B2B", "B2B %"]),
                ("B2C", ["B2C MTD Target", "Sales B2C", "B2C %"]),
                ("TOTAL", ["Total Target", "Total Sales", "Sales %"]),
            ]
            rep_nice = {
                "Branch": "BRANCH", "Sales Rep": "SALES REP",
                "B2B MTD Target": "TARGET", "Sales B2B": "ACTUAL", "B2B %": "ACH %",
                "B2C MTD Target": "TARGET", "Sales B2C": "ACTUAL", "B2C %": "ACH %",
                "Total Target": "TARGET", "Total Sales": "ACTUAL", "Sales %": "ACH %",
            }
            html_rep, h_rep = _build_perf_table("bp-rep", all_rep_rows, rep_groups, rep_nice,
                                         ["B2B %","B2C %","Sales %"],
                                         lambda r: r.get("Sales Rep","") == "\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a", max_visible=10)
            import time
        st.session_state.rep_html_cache = (html_rep, h_rep)
        st.session_state.rep_cache_key = rep_cache_key
        import time
        components.html(html_rep + f"<!-- {time.time()} -->", height=h_rep)

# توجيه الصفحات
def get_first_name_from_email(email):
    local_part = email.split('@')[0]
    first_name = local_part.split('.')[0]
    return first_name

def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        first_name = get_first_name_from_email(st.session_state.user_email)
        user_perm = get_user_permission_type(st.session_state.user_email)
        
        # Determine role labels
        if user_perm == "super_admin":
            role_label = "المدير"
            role_badge = "مسؤول"
            access_label = "كامل الصلاحيات"
            access_color = "#34d399"
        elif user_perm == "all_branches":
            role_label = "مشرف"
            role_badge = "مشرف"
            access_label = "جميع الفروع"
            access_color = "#60a5fa"
        else:
            role_label = "مستخدم"
            role_badge = "عضو"
            access_label = "فروع محددة"
            access_color = "#fbbf24"
        
        # Enhanced Profile Card
        st.sidebar.markdown(f"""
        <div class="sidebar-profile-card">
            <div class="profile-avatar-lg">
                {first_name[0].upper() if first_name else "U"}
            </div>
            <div class="profile-name-lg">{first_name.capitalize()}. مرحباً</div>
            <div class="profile-email-lg">{st.session_state.user_email}</div>
            <div class="profile-role-badge">{role_badge}</div>
            <div class="profile-role-info">
                <div class="role-info-item">
                    <span class="material-symbols-rounded" style="font-size:16px;color:#a78bfa;">shield</span>
                    <div>
                        <div class="ri-label">رتبتك</div>
                        <div class="ri-value" style="color:#e2e8f0;">{role_label}</div>
                    </div>
                </div>
                <div class="role-info-item">
                    <span class="material-symbols-rounded" style="font-size:16px;color:{access_color};">lock_open</span>
                    <div>
                        <div class="ri-label">مستوى الوصول</div>
                        <div class="ri-value" style="color:{access_color};">{access_label}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.rerun()
        
        # Navigation
        st.sidebar.markdown("""
        <div class="sidebar-section-title">
            <span class="material-symbols-rounded">menu</span>
            التنقل
        </div>
        """, unsafe_allow_html=True)
        page = st.sidebar.radio("اختر الصفحة", ["📊 الرئيسية", "⚙️ الإعدادات"], label_visibility="collapsed")
        if "الرئيسية" in page:
            dashboard_page()
        else:
            settings_page()

if __name__ == "__main__":
    main()
