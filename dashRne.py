import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ============================================
# 🎨 PAGE CONFIGURATION & GLOBAL STYLING
# ============================================
st.set_page_config(
    page_title="Business Registry Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .sidebar .sidebar-content {background-color: #e8f4f8;}
    .metric-card {border-radius: 10px; padding: 15px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .st-bq {border-radius: 10px;}
    .st-eb {border-radius: 10px;}
    .css-1aumxhk {background-color: #ffffff;}
    </style>
    """, unsafe_allow_html=True)

# ============================================
# 📊 DATA PREPARATION
# ============================================
@st.cache_data
def load_data():
    df = pd.read_excel("C:/Users/Lenovo/Downloads/statistiques_operations_2024_2025.xlsx")
    return df

df = load_data()

# ============================================
# 🎛️ SIDEBAR - FILTERS & NAVIGATION
# ============================================
with st.sidebar:
    st.title("🏢 Business Registry")
    st.markdown("---")
    
    operation_types = df['نوع العملية'].unique()
    selected_operations = st.multiselect(
        "Filter Operation Types",
        options=operation_types,
        default=["مجموع عمليات التأسيس", "مجموع عمليات التحيين", "استخراج مضمون", "طلب شهادة حجز تسمية"]
    )
    
    st.markdown("---")
    st.subheader("Navigation")
    page = st.radio(
        "Go to:",
        ["📋 Data Overview", "📈 Creation Analysis", "🔄 Update Analysis", 
         "📊 Registration Services", "📌 Executive Summary"],
        label_visibility="collapsed"
    )

# Apply filters
df_filtered = df[df['نوع العملية'].isin(selected_operations)] if selected_operations else df

# ============================================
# 📋 PAGE: DATA OVERVIEW
# ============================================
if page == "📋 Data Overview":
    st.title("Business Registry Data Overview")
    st.markdown("---")
    
    # Summary cards
    total_2024 = df['2024 العدد'].sum()
    total_2025 = df['2025 العدد'].sum()
    change_pct = ((total_2025 - total_2024) / total_2024) * 100
    # Get the specific "مجموع عمليات التأسيس" values
    crea_2024 = df.loc[df['نوع العملية'] == 'مجموع عمليات التأسيس', '2024 العدد'].values[0] + df.loc[df['نوع العملية'] == 'المجموع', '2024 العدد'].values[0]
    crea_2025 = df.loc[df['نوع العملية'] == 'مجموع عمليات التأسيس', '2025 العدد'].values[0] + df.loc[df['نوع العملية'] == 'المجموع', '2025 العدد'].values[0]
    totalf_2024 = total_2024 - crea_2024
    totalf_2025 = total_2025 - crea_2025
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Operations 2024", f"{totalf_2024:,}", "All categories")
    with col2:
        st.metric("Total Operations 2025", f"{totalf_2025:,}", "All categories")
    with col3:
        st.metric("Yearly Change", f"{change_pct:.1f}%")
    
    st.markdown("---")
    
    # Data table with tabs
    tab1, tab2 = st.tabs(["📊 Filtered Data", "📈 Full Data"])
    with tab1:
        st.dataframe(df_filtered.style.format({
            '2024 العدد': '{:,}',
            '2025 العدد': '{:,}',
            'إجمالي العمليات': '{:,}'
        }), use_container_width=True, height=400)
    with tab2:
        st.dataframe(df.style.format({
            '2024 العدد': '{:,}',
            '2025 العدد': '{:,}',
            'إجمالي العمليات': '{:,}'
        }), use_container_width=True, height=400)

# ============================================
# 📈 PAGE: CREATION ANALYSIS
# ============================================
elif page == "📈 Creation Analysis":
    st.title("Business Creation Analysis")
    st.markdown("---")
    
    # Filter creation-related operations
    creation_ops = [op for op in df['نوع العملية'] if 'طلب تأسيس' in op]
    df_creations = df[df['نوع العملية'].isin(creation_ops)]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Creations 2024", f"{df_creations['2024 العدد'].sum():,}")
    with col2:
        st.metric("Total Creations 2025", f"{df_creations['2025 العدد'].sum():,}")
    
    # Creation trends
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_creations['نوع العملية'],
        y=df_creations['2024 العدد'],
        name='2024',
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        x=df_creations['نوع العملية'],
        y=df_creations['2025 العدد'],
        name='2025',
        marker_color='darkblue'
    ))
    fig.update_layout(
        title="<b>Business Creations by Type</b>",
        yaxis_title="Number of Creations",
        barmode='group',
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Creation composition
    fig = px.pie(
        df_creations,
        values='2025 العدد',
        names='نوع العملية',
        title="<b>2025 Creation Composition</b>",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 🔄 PAGE: UPDATE ANALYSIS
# ============================================
elif page == "🔄 Update Analysis":
    st.title("Business Update Analysis")
    st.markdown("---")
    
    # Filter update-related operations
    update_ops = [op for op in df['نوع العملية'] if 'تحيين' in op]
    df_updates = df[df['نوع العملية'].isin(update_ops)]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Updates 2024", f"{df_updates['2024 العدد'].sum():,}")
    with col2:
        st.metric("Total Updates 2025", f"{df_updates['2025 العدد'].sum():,}")
    
    # Update trends
    fig = px.bar(
        df_updates,
        x='نوع العملية',
        y=['2024 العدد', '2025 العدد'],
        title="<b>Business Updates Comparison</b>",
        labels={'value': 'Number of Updates', 'variable': 'Year'},
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Change analysis
    df_updates['الإنزلاق السنوي عدد'] = df_updates['الإنزلاق السنوي'].str.replace('%', '').str.replace(',', '.').astype(float)
    fig = px.bar(
        df_updates,
        x='نوع العملية',
        y='الإنزلاق السنوي عدد',
        title="<b>Yearly Change in Update Operations</b>",
        color='الإنزلاق السنوي عدد',
        color_continuous_scale=px.colors.diverging.RdYlGn,
        text=df_updates['الإنزلاق السنوي']
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 📊 PAGE: REGISTRATION SERVICES
# ============================================
elif page == "📊 Registration Services":
    st.title("Registration Services Analysis")
    st.markdown("---")
    
    # Filter registration services
    service_ops = [
        'ترسيم رهون', 'ترسيم إيجار', 'طلب شهادة حجز تسمية',
        'استخراج مضمون', 'دعوة لجلسة عامة', 'التصريح بالمستفيد الحقيقي'
    ]
    df_services = df[df['نوع العملية'].isin(service_ops)]
    
    # Service metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Most Requested Service", "استخراج مضمون", 
                 f"{df_services[df_services['نوع العملية'] == 'استخراج مضمون']['2025 العدد'].values[0]:,}")
    with col2:
        st.metric("Biggest Increase", "ترسيم رهون", "+16.6%")
    with col3:
        st.metric("Biggest Decrease", "طلب عمليات تحيين أشخاص طبيعيين", "-90.2%")
    
    # Service trends
    fig = px.line(
        df_services,
        x='نوع العملية',
        y=['2024 العدد', '2025 العدد'],
        title="<b>Registration Services Comparison</b>",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Service composition
    fig = px.sunburst(
        df_services,
        path=['نوع العملية'],
        values='2025 العدد',
        title="<b>2025 Service Distribution</b>"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 📌 PAGE: EXECUTIVE SUMMARY
# ============================================
# ============================================
# 📌 PAGE: EXECUTIVE SUMMARY
# ============================================
elif page == "📌 Executive Summary":
    st.title("Executive Summary")
    st.markdown("---")
    
    # Exclude the last row (total row) if it exists
    df_for_summary = df.iloc[:-1] if 'مجموع' in df.iloc[-1]['نوع العملية'] else df
    
    # Calculate KPIs from filtered data (excluding last row)
    total_2024 = df_for_summary['2024 العدد'].sum()
    total_2025 = df_for_summary['2025 العدد'].sum()
    change_pct = ((total_2025 - total_2024) / total_2024) * 100
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Operations 2024", f"{total_2024:,}", "All categories")
    with col2:
        st.metric("Total Operations 2025", f"{total_2025:,}", "All categories")
    with col3:
        st.metric("Yearly Change", f"{change_pct:.1f}%")
    
    st.markdown("---")
    
    # Mini charts
    st.subheader("Performance Highlights")
    
    # Top 5 operations (excluding last row)
    top_ops = df_for_summary.nlargest(5, '2025 العدد')
    
    # Create 3 small charts
    fig1 = px.bar(
        top_ops,
        x='نوع العملية',
        y='2025 العدد',
        title="Top 5 Operations (2025)"
    )
    
    fig2 = px.bar(
        df_for_summary[df_for_summary['نوع العملية'].isin(['مجموع عمليات التأسيس', 'مجموع عمليات التحيين'])],
        x='نوع العملية',
        y='2025 العدد',
        title="Main Categories Volume"
    )
    
    fig3 = px.pie(
        df_for_summary.nlargest(5, '2025 العدد'),
        values='2025 العدد',
        names='نوع العملية',
        title="Top 5 Distribution"
    )
    
    # Display in columns
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Data summary (excluding last row)
    st.markdown("---")
    st.subheader("Data Summary")
    st.dataframe(df_for_summary.describe().style.format("{:,.2f}"), use_container_width=True)