import streamlit as st
import pandas as pd
import os
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Product Recommendation System", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Styling dasar tombol Streamlit agar konsisten */
    .stButton button, .stDownloadButton button {
        width: 100% !important;
        height: 42px !important;
    }
    
    .block-container {
        padding-top: 2rem;
    }

    /* KONTROL TINGGI CARD */
    .stContainer {
        min-height: 400px; 
        display: flex;
        flex-direction: column;
        justify-content: space-between; 
    }

    /* KONTROL GAMBAR di dalam card */
    .stContainer img {
        height: 200px; 
        object-fit: contain; 
        width: 100%;
        padding-bottom: 10px; 
    }

    /* Styling Tombol WhatsApp Custom agar mirip tombol Streamlit */
    .wa-button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 42px;
        background-color: #25D366;
        color: white !important;
        text-decoration: none;
        font-weight: 500;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 0.3s;
    }
    .wa-button:hover {
        background-color: #128C7E;
        color: white !important;
    }

    .detail-card-content {
        flex-grow: 1; 
    }
</style>
""", unsafe_allow_html=True)

# --- HANDLER LOGIC ---
def handle_reset():
    st.session_state.show_dialog = False
    st.session_state.detail_row = None
    st.session_state.submitted = False
    if 'filter_params' in st.session_state:
        st.session_state.filter_params = {} 

def click_detail(row):
    st.session_state.detail_row = row
    st.session_state.show_dialog = True

# --- FUNGSI LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Dataset_Normalized_Complete.csv", sep=";", encoding='latin1')
    except UnicodeDecodeError:
        df = pd.read_csv("Dataset_Normalized_Complete.csv", sep=";")
    df.columns = df.columns.str.strip() 
    return df

# --- FUNGSI CEK GAMBAR ---
def get_image_path(filename):
    if pd.isna(filename):
        return "https://via.placeholder.com/300x200?text=No+Image"
    base_path = os.path.join("static", "images")
    clean_name = str(filename).strip()
    if os.path.exists(os.path.join(base_path, f"{clean_name}.jpg")):
        return os.path.join(base_path, f"{clean_name}.jpg")
    if os.path.exists(os.path.join(base_path, f"{clean_name}.png")):
        return os.path.join(base_path, f"{clean_name}.png")
    return "https://via.placeholder.com/300x200?text=No+Image"

# --- FUNGSI POPUP DETAIL ---
@st.dialog("Detail Produk", width="large")
def show_detail(row):
    brand = row['Brand'] if not pd.isna(row['Brand']) else "-"
    model = row['Model Variations'] if not pd.isna(row['Model Variations']) else "-"
    st.header(f"{brand} - {model}")
    
    img_path = get_image_path(row.get('General Specifications'))
    st.image(img_path, width=250) 
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Spesifikasi Umum")
        st.write(f"**Tipe Produk:** {row.get('Product_type', '-')}")
        st.write(f"**Kategori Ukuran:** {row.get('Ukuran Produk', '-')}")
        st.write(f"**Kategori Berat:** {row.get('Berat Produk', '-')}")
        # --- PENAMBAHAN DATA POWER SOURCE ---
        st.write(f"**Sumber Daya:** {row.get('Power Source', '-')}")
        # ------------------------------------
        st.write(f"**Net Weight:** {row.get('Net Weight (kg)', '-')} Kg")
        
    with col2:
        st.subheader("Dimensi (Measures)")
        st.write(f"**Panjang (L):** {row.get('Measures_L', '-')} mm")
        st.write(f"**Lebar (W):** {row.get('Measures_W', '-')} mm")
        st.write(f"**Tinggi (H):** {row.get('Measures_H', '-')} mm")
        st.write(f"**Total Dimensi:** {row.get('Measures_Total', '-')} mm")

    st.markdown("---")
    
    # LOGIKA TOMBOL AKSI
    spec_name = str(row.get('General Specifications', '')).strip()
    found_path = os.path.join("static", "brochures", f"{spec_name}.pdf")
    
    col_dl, col_share = st.columns(2) 

    if os.path.exists(found_path):
        with col_dl:
            with open(found_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Brosur (PDF)",
                    data=pdf_file,
                    file_name=f"{spec_name}.pdf",
                    mime="application/pdf",
                    key=f"dl_{spec_name}"
                )

        with col_share:
            BASE_URL = "https://tn-pd-library.streamlit.app/" 
            public_url = f"{BASE_URL}/static/brochures/{spec_name}.pdf" 
            message = f"Lihat/Download brosur produk {brand} - {spec_name} melalui link berikut: {public_url}"
            encoded_message = re.sub(r'\s+', '%20', message)
            whatsapp_url = f"https://wa.me/?text={encoded_message}"
            
            st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                    <div class="wa-button">📲 Share ke WhatsApp</div>
                </a>
                """, unsafe_allow_html=True)
    else:
        st.info("Brosur digital belum tersedia untuk produk ini.")
    
    st.markdown("---")
    st.caption("Gunakan ikon 'X' di pojok kanan atas untuk menutup detail.")

# --- MAIN APP ---
def main():
    if 'form_key' not in st.session_state: st.session_state.form_key = 0
    if 'show_dialog' not in st.session_state: st.session_state.show_dialog = False
    if 'submitted' not in st.session_state: st.session_state.submitted = False
    if 'filter_params' not in st.session_state: st.session_state.filter_params = {}

    df = load_data()

    # --- EKSTRAKSI DATA UNIK ---
    def get_uniques(col):
        if col in df.columns:
            temp = df[col].dropna().astype(str).str.replace(r"[\[\]']", '', regex=True)
            all_items = temp.str.split(',').explode().str.strip()
            return sorted([i for i in all_items.unique() if i])
        return []

    unique_locations = get_uniques('Processed_Locations')
    unique_floors = get_uniques('Floor_Type_List')

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🎛️ Filter Pencarian")
    if st.sidebar.button("🔄 Reset Filter"):
        handle_reset()
        st.session_state.form_key += 1
        st.rerun()

    with st.sidebar.form(key=f"filter_form_{st.session_state.form_key}"):
        pilihan_produk = st.radio("Brand / Kategori", ["Semua", "Manual (Fiorentini)", "Otomatis (Gausium)"], 
                                 index=["Semua", "Manual (Fiorentini)", "Otomatis (Gausium)"].index(st.session_state.filter_params.get('pilihan_produk', "Semua")))
        
        types = sorted(df['Product_type'].dropna().unique().tolist())
        filter_type = st.multiselect("Tipe Produk", types, default=st.session_state.filter_params.get('filter_type', []))
        filter_loc = st.multiselect("Lokasi Aplikasi", unique_locations, default=st.session_state.filter_params.get('filter_loc', [])) 
        filter_area = st.number_input("Target Area (m²/h)", min_value=0, step=100, value=st.session_state.filter_params.get('filter_area', 0))
        
        sizes = sorted(df['Ukuran Produk'].dropna().unique().tolist()) if 'Ukuran Produk' in df.columns else []
        filter_size = st.multiselect("Ukuran Produk", sizes, default=st.session_state.filter_params.get('filter_size', []))
        
        weights = sorted(df['Berat Produk'].dropna().unique().tolist()) if 'Berat Produk' in df.columns else []
        filter_weight = st.multiselect("Berat Produk", weights, default=st.session_state.filter_params.get('filter_weight', []))

        filter_floor = st.multiselect("Tipe Lantai", unique_floors, default=st.session_state.filter_params.get('filter_floor', []))

        if st.form_submit_button("Cari Rekomendasi 🚀"):
            st.session_state.submitted = True
            st.session_state.filter_params = {
                'pilihan_produk': pilihan_produk, 'filter_type': filter_type,
                'filter_loc': filter_loc, 'filter_area': filter_area,
                'filter_size': filter_size, 'filter_weight': filter_weight,
                'filter_floor': filter_floor
            }

    # --- LOGIKA FILTERING ---
    if st.session_state.submitted and st.session_state.filter_params:
        params = st.session_state.filter_params
        res = df.copy()

        # Hard Filtering
        if params['pilihan_produk'] == "Manual (Fiorentini)":
            res = res[res['Brand'].str.contains("Fiorentini", case=False, na=False)]
        elif params['pilihan_produk'] == "Otomatis (Gausium)":
            res = res[res['Brand'].str.contains("Gausium", case=False, na=False)]
            
        if params['filter_type']:
            res = res[res['Product_type'].isin(params['filter_type'])]
            
        if params['filter_area'] > 0:
            res['Recommended Coverage Area_min'] = pd.to_numeric(res['Recommended Coverage Area_min'], errors='coerce')
            res['Recommended Coverage Area_max'] = pd.to_numeric(res['Recommended Coverage Area_max'], errors='coerce')
            res = res[(res['Recommended Coverage Area_min'] <= params['filter_area']) & (res['Recommended Coverage Area_max'].fillna(float('inf')) >= params['filter_area'])]
        
        if params['filter_size']: res = res[res['Ukuran Produk'].isin(params['filter_size'])]
        if params['filter_weight']: res = res[res['Berat Produk'].isin(params['filter_weight'])]

        if params['filter_loc']:
            pattern = "|".join([re.escape(f) for f in params['filter_loc']])
            res = res[res['Processed_Locations'].astype(str).str.contains(pattern, flags=re.IGNORECASE, na=False)]

        if params['filter_floor']:
            pattern = "|".join([re.escape(f) for f in params['filter_floor']])
            res = res[res['Floor_Type_List'].astype(str).str.contains(pattern, flags=re.IGNORECASE, na=False)]

        # Tampilkan Hasil
        st.divider()
        st.subheader(f"Hasil: {len(res)} Produk Ditemukan")
        
        if len(res) > 0:
            cols = st.columns(3)
            for idx, (index, row) in enumerate(res.iterrows()):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.image(get_image_path(row['General Specifications']))
                        st.markdown("<div class='detail-card-content'>", unsafe_allow_html=True)
                        st.markdown(f"**{row['Brand']}**")
                        st.caption(f"{row['General Specifications']}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.button("Lihat Detail", key=f"btn_{index}", on_click=click_detail, args=(row,))
        else:
            st.warning("Tidak ada produk yang cocok.")
            
    if st.session_state.show_dialog and st.session_state.detail_row is not None:
        show_detail(st.session_state.detail_row)

if __name__ == "__main__":
    main()
