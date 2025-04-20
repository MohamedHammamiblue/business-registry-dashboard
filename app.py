import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# ============================================
# 🎨 PAGE CONFIGURATION & GLOBAL STYLING
# ============================================
st.set_page_config(
    page_title="Business Registry Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling with RTL support
st.markdown("""
    <style>
    :root {
        --primary: #2c3e50;
        --secondary: #3498db;
        --accent: #e74c3c;
        --background: #f8f9fa;
        --card: #ffffff;
        --text: #333333;
    }
    
    .main {
        background-color: var(--background);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--primary);
        color: white;
    }
    
    .sidebar .stMultiSelect [data-baseweb=select] span,
    .sidebar .stRadio [role=radiogroup] {
        background-color: var(--card) !important;
        color: var(--text) !important;
    }
    
    .metric-card {
        border-radius: 8px;
        padding: 20px;
        background-color: var(--card);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid var(--secondary);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    h1, h2, h3 {
        color: var(--primary);
        font-weight: 600;
    }
    
    h1 {
        border-bottom: 2px solid var(--secondary);
        padding-bottom: 10px;
    }
    
    .stRadio > div {
        background-color: var(--card);
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .stMarkdown hr {
        margin: 1.5rem 0;
        border-top: 2px solid var(--secondary);
        opacity: 0.2;
    }
    
    /* RTL support for Arabic text */
    [dir="rtl"] {
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# 📊 DATA PREPARATION - SIMPLIFIED FOR 2024-2025 COMPARISON
# ============================================
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("statistiques_operations_2024_2025.xlsx")
        
        # Data cleaning and validation
        df = df.dropna(how='all')  # Remove completely empty rows
        numeric_cols = ['2024 العدد', '2025 العدد']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()  # Return empty dataframe to prevent app crash

df = load_data()

# ============================================
# 🎛️ SIDEBAR - FILTERS & NAVIGATION
# ============================================
with st.sidebar:
    st.image("logo.png", width=200)  # Adjust width as needed
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("### 🏢 Business Registry Dashboard")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 0.8em; color: #bdc3c7;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not df.empty:
        operation_types = df['نوع العملية'].unique()
        selected_operations = st.multiselect(
            "Filter Operation Types",
            options=operation_types,
            default=["مجموع عمليات التأسيس","مجموع عمليات التحيين","استخراج مضمون", "طلب شهادة حجز تسمية","ترسيم رهون","ترسيم إيجار","دعوة لجلسة عامة","التصريح بالمستفيد الحقيقي"
        ],            help="Select operation types to analyze"
        )
    else:
        st.warning("No data available for filtering")
        selected_operations = []
    
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.subheader("Navigation")
    page = st.radio(
        "Go to:",
        ["📋 Data Overview", "📈 Creation Analysis", "🔄 Modification Analysis", 
         "📊 Additional Services", "📌 Executive Summary"],
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Apply filters with validation
if not df.empty:
    df_filtered = df[df['نوع العملية'].isin(selected_operations)] if selected_operations else df
else:
    df_filtered = pd.DataFrame()

# ============================================
# 📋 DATA OVERVIEW PAGE - FOCUSED ON COMPARISON
# ============================================
if page == "📋 Data Overview":
    st.title("Business Registry Data Overview")
    st.markdown("---")
    
    if not df.empty:
        # Calculate comparison metrics
        # Calculate total while excluding rows 6 and 16 (0-based index)
        total_2024 = df.drop([5,8, 15])['2024 العدد'].sum()  # Rows 6 and 16 (subtract 1 for 0-based index)
        total_2025 = df.drop([5,8, 15])['2025 العدد'].sum()
        change_pct = ((total_2025 - total_2024) / total_2024) * 100 if total_2024 != 0 else 0
        
        # Get creation values with error handling
        try:
            crea_2024 = df.loc[df['نوع العملية'] == 'مجموع عمليات التأسيس', '2024 العدد'].values[0]
            crea_2025 = df.loc[df['نوع العملية'] == 'مجموع عمليات التأسيس', '2025 العدد'].values[0]
        except (IndexError, KeyError):
            crea_2024, crea_2025 = 0, 0
            
        # Professional summary cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card" dir="rtl">
                    <h3 style='color: var(--primary);'>📅 مجموع 2024 </h3>
                    <h2 style='margin: 10px 0;'>{total_2024:,}</h2>
                    <p style='color: #7f8c8d; font-size: 0.9em;'>إجمالي العمليات</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card" dir="rtl">
                    <h3 style='color: var(--primary);'>📅  مجموع 2025</h3>
                    <h2 style='margin: 10px 0;'>{total_2025:,}</h2>
                    <p style='color: #7f8c8d; font-size: 0.9em;'>إجمالي العمليات</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card" dir="rtl">
                    <h3 style='color: var(--primary);'>📈 التغيير السنوي</h3>
                    <h2 style='margin: 10px 0; color: {'#27ae60' if change_pct >=0 else '#e74c3c'}'>
                        {abs(change_pct):.1f}% {'↑' if change_pct >=0 else '-↓'}
                    </h2>
                    <p style='color: #7f8c8d; font-size: 0.9em;'>مقارنة بالسنة السابقة</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Comparison visualization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['2024', '2025'],
            y=[total_2024, total_2025],
            marker_color=['#3498db', '#2c3e50'],
            text=[f"{total_2024:,}", f"{total_2025:,}"],
            textposition='auto'
        ))
        fig.update_layout(
            title="<b>مقارنة إجمالي العمليات بين 2024 و 2025</b>",
            yaxis_title="عدد العمليات",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table with comparison
        st.subheader("Detailed Operation Comparison")
        tab1, tab2 = st.tabs(["📊 Filtered Data", "📈 Full Data"])
        
        with tab1:
            if not df_filtered.empty:
                st.dataframe(
                    df_filtered.style.format({
                        '2024 العدد': '{:,}',
                        '2025 العدد': '{:,}'
                    }).background_gradient(cmap='Blues', subset=['2024 العدد', '2025 العدد']),
                    use_container_width=True,
                    height=400
                )
            else:
                st.warning("No data available with current filters")
                
        with tab2:
            st.dataframe(
                df.style.format({
                    '2024 العدد': '{:,}',
                    '2025 العدد': '{:,}'
                }).background_gradient(cmap='Blues', subset=['2024 العدد', '2025 العدد']),
                use_container_width=True,
                height=600
            )
    else:
        st.error("No data available to display")

# ============================================
# 📈 CREATION ANALYSIS PAGE - COMPARISON FOCUS
# ============================================
elif page == "📈 Creation Analysis":
    st.title("Business Creation Analysis")
    st.markdown("---")
    
    if not df.empty:
        # Filter creation-related operations
        creation_ops = [op for op in df['نوع العملية'].unique() if 'طلب تأسيس' in op or 'إنشاء' in op]
        df_creations = df[df['نوع العملية'].isin(creation_ops)]
        
        if not df_creations.empty:
            # Calculate comparison metrics
            crea_2024 = df_creations['2024 العدد'].sum()
            crea_2025 = df_creations['2025 العدد'].sum()
            crea_change = crea_2025 - crea_2024
            crea_change_pct = (crea_change / crea_2024) * 100 if crea_2024 != 0 else 0
            
            # Professional metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>📅 مجموع التأسيس 2024</h3>
                        <h2 style='margin: 10px 0;'>{crea_2024:,}</h2>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>📅 مجموع التأسيس 2025</h3>
                        <h2 style='margin: 10px 0;'>{crea_2025:,}</h2>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>📈 التغيير السنوي</h3>
                        <h2 style='margin: 10px 0; color: {'#27ae60' if crea_change_pct >=0 else '#e74c3c'}'>
                            {crea_change_pct:.1f}% {'↑' if crea_change_pct >=0 else '↓'}
                        </h2>
                        <p style='color: #7f8c8d; font-size: 0.9em; direction: rtl; text-align: right;'>  {'زيادة' if crea_change >=0 else 'انخفاض'} {abs(crea_change):,}
</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Creation trends comparison
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_creations['نوع العملية'],
                y=df_creations['2024 العدد'],
                name='2024',
                marker_color='#3498db',
                hovertemplate='<b>%{x}</b><br>2024: %{y:,} تأسيس<extra></extra>'
            ))
            fig.add_trace(go.Bar(
                x=df_creations['نوع العملية'],
                y=df_creations['2025 العدد'],
                name='2025',
                marker_color='#2c3e50',
                hovertemplate='<b>%{x}</b><br>2025: %{y:,} تأسيس<extra></extra>'
            ))
            fig.update_layout(
                title="<b>مقارنة عمليات التأسيس حسب النوع</b>",
                yaxis_title="عدد عمليات التأسيس",
                xaxis_title="نوع العملية",
                barmode='group',
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Yearly change visualization
            df_creations['change_pct'] = ((df_creations['2025 العدد'] - df_creations['2024 العدد']) / df_creations['2024 العدد']) * 100
            fig = px.bar(
                df_creations,
                x='نوع العملية',
                y='change_pct',
                title="<b>النسبة المئوية للتغيير في عمليات التأسيس</b>",
                labels={'change_pct': 'النسبة المئوية للتغيير'},
                color='change_pct',
                color_continuous_scale=px.colors.diverging.RdYlGn,
                range_color=[-100, 100]
            )
            fig.update_layout(
                yaxis_title="النسبة المئوية للتغيير",
                xaxis_title="نوع العملية",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No creation-related data available with current filters")
    else:
        st.error("No data available to display")

# ============================================
# 🔄 UPDATE ANALYSIS PAGE - COMPARISON FOCUS
# ============================================
elif page == "🔄 Modification Analysis":
    st.title("Analysis of Business Records Modifications")
    st.markdown("---")
    
    if not df.empty:
        # Filter update-related operations
        update_ops = [op for op in df['نوع العملية'].unique() if 'طلب عمليات' in op or 'تحديث' in op]
        df_updates = df[df['نوع العملية'].isin(update_ops)]
        
        if not df_updates.empty:
            # Calculate comparison metrics
            update_2024 = df_updates['2024 العدد'].sum()
            update_2025 = df_updates['2025 العدد'].sum()
            update_change = update_2025 - update_2024
            update_change_pct = (update_change / update_2024) * 100 if update_2024 != 0 else 0
            
            # Professional metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>🔄 2024 التحيين</h3>
                        <h2 style='margin: 10px 0;'>{update_2024:,}</h2>
                        <p style='color: #7f8c8d; font-size: 0.9em;'>إجمالي عمليات التحيين</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>🔄 2025 التحيين</h3>
                        <h2 style='margin: 10px 0;'>{update_2025:,}</h2>
                        <p style='color: #7f8c8d; font-size: 0.9em;'>إجمالي عمليات التحيين</p>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>📈 التغيير السنوي</h3>
                        <h2 style='margin: 10px 0; color: {'#27ae60' if update_change_pct >=0 else '#e74c3c'}'>
                            {abs(update_change_pct):.1f}% {'↑' if update_change_pct >=0 else '- ↓'}
                        </h2>
                        <p style='color: #7f8c8d; font-size: 0.9em; direction: rtl; text-align: right; unicode-bidi: embed;'> {'زيادة ' if update_change >=0 else 'انخفاض '}<br>{abs(update_change):,}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Update trends comparison
            fig = px.line(
                df_updates.melt(id_vars=['نوع العملية'], 
                               value_vars=['2024 العدد', '2025 العدد'],
                               var_name='السنة', 
                               value_name='العدد'),
                x='نوع العملية',
                y='العدد',
                color='السنة',
                title="<b>اتجاهات تحديث الأعمال</b>",
                markers=True,
                labels={'العدد': 'عدد التحديثات', 'نوع العملية': 'نوع التحديث'},
                color_discrete_map={'2024 العدد': '#3498db', '2025 العدد': '#2c3e50'}
            )
            fig.update_layout(
                hovermode="x unified",
                xaxis_title="نوع التحديث",
                yaxis_title="عدد التحديثات",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Yearly change visualization
            df_updates['change_pct'] = ((df_updates['2025 العدد'] - df_updates['2024 العدد']) / df_updates['2024 العدد']) * 100
            fig = px.bar(
                df_updates,
                x='نوع العملية',
                y='change_pct',
                title="<b>النسبة المئوية للتغيير في عمليات التحديث</b>",
                labels={'change_pct': 'النسبة المئوية للتغيير'},
                color='change_pct',
                color_continuous_scale=px.colors.diverging.RdYlGn,
                range_color=[-100, 100]
            )
            fig.update_layout(
                yaxis_title="النسبة المئوية للتغيير",
                xaxis_title="نوع العملية",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No update-related data available with current filters")
    else:
        st.error("No data available to display")

# ============================================
# 📊 Additional Services PAGE - COMPARISON FOCUS
# ============================================
elif page == "📊 Additional Services":
    st.title("Additional Services Analysis")
    st.markdown("---")
    
    if not df.empty:
        # Filter Additional Services
        service_ops = [
            'ترسيم رهون', 'ترسيم إيجار', 'طلب شهادة حجز تسمية',
            'استخراج مضمون', 'دعوة لجلسة عامة', 'التصريح بالمستفيد الحقيقي'
        ]
        df_services = df[df['نوع العملية'].isin(service_ops)]
        
        if not df_services.empty:
            # Calculate comparison metrics
            service_2024 = df_services['2024 العدد'].sum()
            service_2025 = df_services['2025 العدد'].sum()
            service_change = service_2025 - service_2024
            service_change_pct = (service_change / service_2024) * 100 if service_2024 != 0 else 0
            
            # Find most requested service
            most_requested = df_services.loc[df_services['2025 العدد'].idxmax(), 'نوع العملية']
            most_requested_count = df_services['2025 العدد'].max()
            
            # Find biggest increase and decrease
            df_services['change_pct'] = ((df_services['2025 العدد'] - df_services['2024 العدد']) / 
                                       df_services['2024 العدد']) * 100
            biggest_increase = df_services.loc[df_services['change_pct'].idxmax(), 'نوع العملية']
            biggest_increase_pct = df_services['change_pct'].max()
            biggest_decrease = df_services.loc[df_services['change_pct'].idxmin(), 'نوع العملية']
            biggest_decrease_pct = df_services['change_pct'].min()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>📄 الخدمة الأكثر طلباً</h3>
                        <h2 style='margin: 10px 0;'>{most_requested}</h2>
                        <p style='color: #7f8c8d; font-size: 1.2em;'>{most_requested_count:,} طلب</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>📈 أكبر زيادة</h3>
                        <h2 style='margin: 10px 0;'>{biggest_increase}</h2>
                        <p style='color: #27ae60; font-size: 1.2em;'>{biggest_increase_pct:.1f}↑</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                    <div class="metric-card" dir="rtl">
                        <h3 style='color: var(--primary);'>📉 أكبر انخفاض</h3>
                        <h2 style='margin: 10px 0;'>{biggest_decrease}</h2>
                        <p style='color: #e74c3c; font-size: 1.2em;'>{abs(biggest_decrease_pct):.1f} - ↓ </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Service trends comparison
            try:
                fig = px.line(
                    df_services,
                    x='نوع العملية',
                    y=['2024 العدد', '2025 العدد'],
                    title="<b>مقارنة خدمات التسجيل</b>",
                    markers=True,
                    labels={'value': 'عدد الخدمات', 'variable': 'السنة'},
                    color_discrete_sequence=['#3498db', '#2c3e50']
                )
                fig.update_layout(
                    hovermode="x unified",
                    xaxis_title="نوع الخدمة",
                    yaxis_title="عدد الخدمات",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating trend chart: {str(e)}")
            
            # Service distribution comparison
            try:
                total_services = df_services['2025 العدد'].sum()
                fig = px.sunburst(
                    df_services,
                    path=['نوع العملية'],
                    values='2025 العدد',
                    title="<b>توزيع الخدمات الإظافية لسنة 2025</b>",
                    color='2025 العدد',
                    color_continuous_scale='Blues',
                    branchvalues='total'
                )
                fig.update_traces(
                    textinfo='label+percent parent',
                    texttemplate='<b>%{label}</b><br>%{percentParent:.1%}',
                    textfont_size=12,
                    hovertemplate='<b>%{label}</b><br>العدد: %{value:,}<br>النسبة: %{percentParent:.1%}',
                    insidetextorientation='auto'
                )
                fig.update_layout(
                    margin=dict(t=50, b=20, l=20, r=20),
                    title_font_size=18,
                    title_x=0.5
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating distribution chart: {str(e)}")
                
        else:
            st.warning("لا توجد بيانات خدمات متاحة مع عوامل التصفية الحالية")
    else:
        st.error("لا توجد بيانات متاحة للعرض")
# ============================================
# 📌 EXECUTIVE SUMMARY PAGE - COMPARISON FOCUS
# ============================================
elif page == "📌 Executive Summary":
    st.title("Executive Summary")
    st.markdown("---")
    
    if not df.empty:
        # Exclude the last row (total row) if it exists
        df_for_summary = df.iloc[:-1] if 'مجموع' in df.iloc[-1]['نوع العملية'] else df
        
        # Calculate KPIs from filtered data (excluding last row)
        total_2024 = df.drop([5,8, 15])['2024 العدد'].sum()  # Rows 6 and 16 (subtract 1 for 0-based index)
        total_2025 = df.drop([5,8, 15])['2025 العدد'].sum()
        change_pct = ((total_2025 - total_2024) / total_2024) * 100 if total_2024 != 0 else 0
        
        # Get creation and update metrics
        creation_ops = [op for op in df_for_summary['نوع العملية'].unique() if 'طلب تأسيس' in op or 'إنشاء' in op]
        update_ops = [op for op in df_for_summary['نوع العملية'].unique() if 'طلب عمليات' in op or 'تحديث' in op]
        
        df_creations = df_for_summary[df_for_summary['نوع العملية'].isin(creation_ops)]
        df_updates = df_for_summary[df_for_summary['نوع العملية'].isin(update_ops)]
        
        crea_2024 = df_creations['2024 العدد'].sum() if not df_creations.empty else 0
        crea_2025 = df_creations['2025 العدد'].sum() if not df_creations.empty else 0
        crea_change_pct = ((crea_2025 - crea_2024) / crea_2024) * 100 if crea_2024 != 0 else 0
        
        update_2024 = df_updates['2024 العدد'].sum() if not df_updates.empty else 0
        update_2025 = df_updates['2025 العدد'].sum() if not df_updates.empty else 0
        update_change_pct = ((update_2025 - update_2024) / update_2024) * 100 if update_2024 != 0 else 0
        
        # Find biggest increase and decrease across all operations
        df_for_summary['change_pct'] = ((df_for_summary['2025 العدد'] - df_for_summary['2024 العدد']) / df_for_summary['2024 العدد']) * 100
        biggest_increase = df_for_summary.loc[df_for_summary['change_pct'].idxmax(), 'نوع العملية']
        biggest_increase_pct = df_for_summary['change_pct'].max()
        biggest_decrease = df_for_summary.loc[df_for_summary['change_pct'].idxmin(), 'نوع العملية']
        biggest_decrease_pct = df_for_summary['change_pct'].min()
        
        # Top 5 operations (excluding last row)
        top_ops = df_for_summary.nlargest(5, '2025 العدد')
        
        # Professional KPI Cards
        st.subheader("Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 مجموع الخدمات</h3>
                    <h2>{total_2025:,}</h2>
                    <p style='color: {'#27ae60' if change_pct >=0 else '#e74c3c'}'>
                        {'↑' if change_pct >=0 else '↓'} {abs(change_pct):.1f}%
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>🏢 مجموع التأسيس</h3>
                    <h2>{crea_2025:,}</h2>
                    <p style='color: {'#27ae60' if crea_change_pct >=0 else '#e74c3c'}'>
                        {'↑' if crea_change_pct >=0 else '↓'} {abs(crea_change_pct):.1f}%
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>🔄 مجموع التحيين</h3>
                    <h2>{update_2025:,}</h2>
                    <p style='color: {'#27ae60' if update_change_pct >=0 else '#e74c3c'}'>
                        {'↑' if update_change_pct >=0 else '↓'} {abs(update_change_pct):.1f}%
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>📅 التغيير السنوي</h3>
                    <h2>2024 → 2025</h2>
                    <p style='color: {'#27ae60' if (total_2025 > total_2024) else '#e74c3c'}'>
                        {'Growth' if (total_2025 > total_2024) else 'Decline'}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Comparison visualization
        st.subheader("التغيير السنوي للثلالثي الأول")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[' إجمالي العمليات', 'التأسيس', 'التحيين'],
            y=[total_2024, crea_2024, update_2024],
            name='2024',
            marker_color='#3498db'
        ))
        fig.add_trace(go.Bar(
            x=[' إجمالي العمليات', 'التأسيس', 'التحيين'],
            y=[total_2025, crea_2025, update_2025],
            name='2025',
            marker_color='#2c3e50'
        ))
        fig.update_layout(
            barmode='group',
            title="<b>Key Metrics Comparison</b>",
            yaxis_title="عدد العمليات",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top operations visualization
        st.markdown("---")
        st.subheader("أهم العمليات في 2025")
        fig = px.bar(
            top_ops,
            x='نوع العملية',
            y='2025 العدد',
            title="<b>أعلى 5 عمليات حسب الحجم</b>",
            color='2025 العدد',
            color_continuous_scale='Blues',
            labels={'2025 العدد': 'الحجم', 'نوع العملية': 'Operation Type'}
        )
        fig.update_layout(
            xaxis_title="نوع العملية",
            yaxis_title="الحجم",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights section
        st.markdown("---")
        st.subheader("Key Insights الرؤى الرئيسية")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown(f"""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; 
                          border-left: 4px solid #3498db; text-align: right; direction: rtl;'>
                    <h4 style='color: #2c3e50; margin-top: 0;'>📈 اتجاهات النمو</h4>
                    <ul style='padding-right: 20px;'>
                        <li>إجمالي العمليات تغيرت بنسبة <strong>{abs(change_pct):.1f}{"+" if change_pct >= 0 else "-" + "%"}</strong></li>
                        <li>عمليات التأسيس تغيرت بنسبة <strong>{abs(crea_change_pct):.1f}{"+ %" if crea_change_pct >= 0 else "- %"}</strong></li>
                        <li>عمليات التحيين تغيرت بنسبة <strong>{abs(update_change_pct):.1f}{"+" if update_change_pct >= 0 else "-" + "%"}</strong></li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
    with insight_col2:
        try:
            # Safely get values with fallbacks
            top_op_name = top_ops.iloc[0].get('نوع_العملية', 'غير متوفر')
            top_op_count = top_ops.iloc[0].get('2025_العدد', 0)
            
            # Arabic Version (same styling)
            st.markdown("""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #e74c3c; text-align: right; direction: rtl;'>
                    <h4 style='color: #2c3e50; margin-top: 0;'>📊 النقاط البارزة</h4>
                    <ul style='padding-right: 20px;'>
                        <li>أعلى عملية في 2025: <strong>{}</strong> بعدد {:,} طلب</li>
                        <li>أكبر زيادة في: <strong>{}</strong> ({:.1f}%)</li>
                        <li>أكبر انخفاض في: <strong>{}</strong> ({:.1f}- %)</li>
                    </ul>
                </div>
            """.format(
                top_ops.iloc[0]['نوع العملية'],
                top_ops.iloc[0]['2025 العدد'],
                biggest_increase,
                biggest_increase_pct,
                biggest_decrease,
                abs(biggest_decrease_pct)
            ), unsafe_allow_html=True)
    
        except Exception as e:
            st.error(f"Error displaying data: {str(e)}")
else:
    st.error("No data available to display")

# ============================================
# 🚀 FOOTER
# ============================================
st.markdown(f"""
    <div style='text-align: center; margin-top: 40px; color: #7f8c8d; font-size: 0.9em;'>
        <hr style='border-top: 1px solid #ecf0f1;'>
        <p>Business Registry Dashboard </p>
        <p>© {datetime.now().year} CRNE</p>
    </div>
""", unsafe_allow_html=True)