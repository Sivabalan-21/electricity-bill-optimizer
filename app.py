"""
ELECTRICITY BILL OPTIMIZER - STREAMLIT WEB APP
===============================================
To run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="⚡ Electricity Bill Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {padding: 0rem 1rem;}
    .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
    h1 {color: #1f77b4;}
    .stButton>button {width: 100%;}
</style>
""", unsafe_allow_html=True)

# ==================== CONFIGURATION ====================
ELECTRICITY_RATES = {
    'rate_0_100': 3.0,
    'rate_100_200': 4.5,
    'rate_200_300': 6.0,
    'rate_300_plus': 8.0,
    'fixed_charge': 50
}

# ==================== FUNCTIONS ====================

def calculate_bill(units):
    """Calculate electricity bill based on slab rates"""
    bill = ELECTRICITY_RATES['fixed_charge']
    
    if units <= 100:
        bill += units * ELECTRICITY_RATES['rate_0_100']
    elif units <= 200:
        bill += 100 * ELECTRICITY_RATES['rate_0_100']
        bill += (units - 100) * ELECTRICITY_RATES['rate_100_200']
    elif units <= 300:
        bill += 100 * ELECTRICITY_RATES['rate_0_100']
        bill += 100 * ELECTRICITY_RATES['rate_100_200']
        bill += (units - 200) * ELECTRICITY_RATES['rate_200_300']
    else:
        bill += 100 * ELECTRICITY_RATES['rate_0_100']
        bill += 100 * ELECTRICITY_RATES['rate_100_200']
        bill += 100 * ELECTRICITY_RATES['rate_200_300']
        bill += (units - 300) * ELECTRICITY_RATES['rate_300_plus']
    
    return round(bill, 2)

def create_sample_data():
    """Create sample data for demonstration"""
    months = ['Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24',
              'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24', 'Nov-24', 'Dec-24']
    units = [220, 200, 240, 320, 380, 350, 340, 310, 270, 250, 230, 240]
    amounts = [calculate_bill(u) for u in units]
    
    return pd.DataFrame({
        'month': months,
        'units': units,
        'amount': amounts
    })

def analyze_bills(df):
    """Analyze electricity bills"""
    stats = {
        'avg_units': df['units'].mean(),
        'avg_amount': df['amount'].mean(),
        'max_units': df['units'].max(),
        'min_units': df['units'].min(),
        'max_month': df.loc[df['units'].idxmax(), 'month'],
        'min_month': df.loc[df['units'].idxmin(), 'month'],
        'total_units': df['units'].sum(),
        'total_amount': df['amount'].sum()
    }
    
    # Calculate trend
    if len(df) >= 6:
        recent_3 = df.tail(3)['units'].mean()
        old_3 = df.head(3)['units'].mean()
        stats['trend'] = ((recent_3 - old_3) / old_3) * 100
    else:
        stats['trend'] = 0
    
    return stats

def get_savings_tips(avg_units):
    """Get personalized savings tips"""
    tips = []
    
    if avg_units > 300:
        tips.append({
            'icon': '🌡️',
            'title': 'High Consumption Alert',
            'description': 'Your consumption is quite high',
            'action': 'Set AC to 24-26°C instead of lower temperatures',
            'saving': '₹500-800/month',
            'priority': 'HIGH'
        })
    
    if avg_units > 250:
        tips.append({
            'icon': '❄️',
            'title': 'Optimize AC Usage',
            'description': 'AC consumes 40-50% of your bill',
            'action': 'Use AC only in occupied rooms, close doors/windows',
            'saving': '₹300-500/month',
            'priority': 'HIGH'
        })
    
    tips.extend([
        {
            'icon': '💡',
            'title': 'Switch to LED Bulbs',
            'description': 'LED bulbs use 75% less energy',
            'action': 'Replace all traditional bulbs with LED',
            'saving': '₹200-300/month',
            'priority': 'MEDIUM'
        },
        {
            'icon': '🚿',
            'title': 'Water Heater Timer',
            'description': 'Water heaters consume 15-20% of electricity',
            'action': 'Use timer - heat only 30 minutes before use',
            'saving': '₹150-250/month',
            'priority': 'MEDIUM'
        },
        {
            'icon': '🔌',
            'title': 'Unplug Devices',
            'description': 'Phantom load can waste 5-10% energy',
            'action': 'Turn off devices at night, unplug chargers',
            'saving': '₹100-150/month',
            'priority': 'LOW'
        },
        {
            'icon': '🔧',
            'title': 'Regular Maintenance',
            'description': 'Dirty AC filters increase consumption',
            'action': 'Clean AC filters monthly, service annually',
            'saving': '₹150-200/month',
            'priority': 'LOW'
        }
    ])
    
    return tips

def compare_with_average(avg_units):
    """Compare with typical households"""
    typical = {
        'Small Apartment (1-2 BHK)': 150,
        'Medium Apartment (2-3 BHK)': 250,
        'Large Apartment (3+ BHK)': 350,
        'Independent House': 400
    }
    
    comparison = []
    for house_type, units in typical.items():
        diff = avg_units - units
        status = "✅ Below Average" if diff < 0 else "⚠️ Above Average"
        comparison.append({
            'House Type': house_type,
            'Typical': f"{units} units",
            'Your Average': f"{avg_units:.0f} units",
            'Difference': f"{diff:+.0f} units",
            'Status': status
        })
    
    # Find closest match
    closest = min(typical.items(), key=lambda x: abs(x[1] - avg_units))
    
    return pd.DataFrame(comparison), closest

# ==================== MAIN APP ====================

# Header
st.title("⚡ Electricity Bill Optimizer")
st.markdown("### 💰 Save Money on Your Electricity Bills!")
st.markdown("---")

# Initialize session state
if 'bills' not in st.session_state:
    st.session_state.bills = []
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

# Sidebar - Input Section
with st.sidebar:
    st.header("📊 Input Your Bills")
    
    # Input method selection
    input_method = st.radio(
        "Choose Input Method:",
        ["📝 Manual Entry", "📤 Upload CSV", "📊 Sample Data"],
        label_visibility="visible"
    )
    
    if input_method == "📝 Manual Entry":
        st.markdown("---")
        st.subheader("Add Monthly Bills")
        
        with st.form("bill_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                month = st.text_input("Month", placeholder="Jan-24")
            with col2:
                units = st.number_input("Units", min_value=0.0, step=10.0, format="%.1f")
            
            amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
            
            submitted = st.form_submit_button("➕ Add Bill", use_container_width=True)
            
            if submitted and month:
                st.session_state.bills.append({
                    'month': month,
                    'units': float(units),
                    'amount': float(amount)
                })
                st.success(f"✅ Added: {month}")
                st.session_state.analyzed = False
        
        # Show current bills
        if st.session_state.bills:
            st.markdown("---")
            st.subheader("📋 Your Bills")
            df_display = pd.DataFrame(st.session_state.bills)
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns(2)
            if col1.button("🗑️ Clear All", use_container_width=True):
                st.session_state.bills = []
                st.session_state.analyzed = False
                st.rerun()
    
    elif input_method == "📤 Upload CSV":
        st.markdown("---")
        st.info("📄 CSV format: month, units, amount")
        st.markdown("Example:\n```\nmonth,units,amount\nJan-24,250,1500\nFeb-24,280,1700\n```")
        
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.success(f"✅ Loaded {len(df)} months of data!")
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.session_state.analyzed = False
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
    
    else:  # Sample Data
        st.markdown("---")
        st.info("👉 Click below to load 12 months of sample data")
        
        if st.button("📊 Load Sample Data", use_container_width=True):
            st.session_state.df = create_sample_data()
            st.success("✅ Sample data loaded!")
            st.session_state.analyzed = False
    
    # Customize rates
    st.markdown("---")
    with st.expander("⚙️ Customize Electricity Rates"):
        st.markdown("##### Modify rates for your state:")
        ELECTRICITY_RATES['rate_0_100'] = st.number_input(
            "0-100 units (₹/unit)", value=3.0, step=0.1, format="%.2f"
        )
        ELECTRICITY_RATES['rate_100_200'] = st.number_input(
            "100-200 units (₹/unit)", value=4.5, step=0.1, format="%.2f"
        )
        ELECTRICITY_RATES['rate_200_300'] = st.number_input(
            "200-300 units (₹/unit)", value=6.0, step=0.1, format="%.2f"
        )
        ELECTRICITY_RATES['rate_300_plus'] = st.number_input(
            "300+ units (₹/unit)", value=8.0, step=0.1, format="%.2f"
        )
        ELECTRICITY_RATES['fixed_charge'] = st.number_input(
            "Fixed Charge (₹)", value=50.0, step=10.0, format="%.2f"
        )

# Main Content Area
if 'df' in st.session_state or st.session_state.bills:
    # Get dataframe
    if 'df' in st.session_state:
        df = st.session_state.df
    else:
        df = pd.DataFrame(st.session_state.bills)
    
    # Analyze button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔍 ANALYZE MY BILLS", type="primary", use_container_width=True):
            st.session_state.analyzed = True
    
    if st.session_state.analyzed:
        # Show bills table
        st.subheader("📋 Your Electricity Bills")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Analyze
        stats = analyze_bills(df)
        
        # Key Metrics
        st.markdown("---")
        st.subheader("📊 Summary Statistics")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Avg Monthly Units", f"{stats['avg_units']:.0f} kWh")
        with col2:
            st.metric("Avg Monthly Bill", f"₹{stats['avg_amount']:.0f}")
        with col3:
            st.metric("Peak Month", stats['max_month'], f"{stats['max_units']:.0f} units")
        with col4:
            st.metric("Lowest Month", stats['min_month'], f"{stats['min_units']:.0f} units")
        with col5:
            trend_emoji = "📈" if stats['trend'] > 5 else "📉" if stats['trend'] < -5 else "➡️"
            st.metric("Trend", f"{trend_emoji} {abs(stats['trend']):.1f}%")
        
        # Tabs for different sections
        st.markdown("---")
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Charts", "💡 Savings Tips", "🏘️ Comparison", "🔮 Prediction"])
        
        with tab1:
            st.subheader("Consumption Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly consumption bar chart
                fig1 = px.bar(
                    df, x='month', y='units',
                    title='📊 Monthly Consumption (kWh)',
                    labels={'units': 'Units (kWh)', 'month': 'Month'},
                    color='units',
                    color_continuous_scale='Blues'
                )
                fig1.add_hline(
                    y=stats['avg_units'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Average: {stats['avg_units']:.0f}",
                    annotation_position="right"
                )
                fig1.update_layout(showlegend=False)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Monthly bills line chart
                fig2 = px.line(
                    df, x='month', y='amount',
                    title='💰 Monthly Bill Amount (₹)',
                    labels={'amount': 'Amount (₹)', 'month': 'Month'},
                    markers=True
                )
                fig2.update_traces(line_color='green', line_width=3, marker_size=10)
                st.plotly_chart(fig2, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                # Cost per unit
                df['cost_per_unit'] = df['amount'] / df['units']
                fig3 = px.bar(
                    df, x='month', y='cost_per_unit',
                    title='📉 Average Rate per Unit (₹/kWh)',
                    labels={'cost_per_unit': 'Rate (₹/kWh)', 'month': 'Month'},
                    color='cost_per_unit',
                    color_continuous_scale='Oranges'
                )
                fig3.update_layout(showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)
            
            with col4:
                # Pie chart - consumption breakdown estimate
                breakdown = {
                    'Appliance': ['AC', 'Water Heater', 'Refrigerator', 'Lights & Fans', 'Others'],
                    'Percentage': [45, 18, 12, 17, 8]
                }
                fig4 = px.pie(
                    breakdown, values='Percentage', names='Appliance',
                    title='🔌 Estimated Consumption Breakdown',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig4, use_container_width=True)
        
        with tab2:
            st.subheader("💡 Personalized Money-Saving Tips")
            
            tips = get_savings_tips(stats['avg_units'])
            
            # Calculate total savings
            total_monthly_saving = 0
            for tip in tips:
                try:
                    min_save = int(tip['saving'].split('-')[0].replace('₹', ''))
                    total_monthly_saving += min_save
                except:
                    pass
            
            # Show potential savings
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💵 Potential Monthly Savings", f"₹{total_monthly_saving}+")
            with col2:
                st.metric("💰 Potential Yearly Savings", f"₹{total_monthly_saving * 12}+")
            
            st.markdown("---")
            
            # Display tips
            for i, tip in enumerate(tips, 1):
                priority_color = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }
                
                with st.expander(f"{tip['icon']} {tip['title']} {priority_color.get(tip['priority'], '')}", expanded=i<=2):
                    st.markdown(f"**{tip['description']}**")
                    st.info(f"✅ **Action:** {tip['action']}")
                    st.success(f"💰 **Potential Saving:** {tip['saving']}")
        
        with tab3:
            st.subheader("🏘️ How You Compare")
            
            comparison_df, closest = compare_with_average(stats['avg_units'])
            
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.info(f"📍 **Your consumption profile matches:** {closest[0]}")
            
            # Show recommendation based on comparison
            if stats['avg_units'] > closest[1] * 1.2:
                diff_pct = ((stats['avg_units'] / closest[1] - 1) * 100)
                potential_save = (stats['avg_units'] - closest[1]) * 6
                st.warning(f"⚠️ You're using **{diff_pct:.0f}% MORE** than typical {closest[0]}")
                st.error(f"💰 Potential monthly savings: **₹{potential_save:.0f}** by optimizing to typical levels")
            elif stats['avg_units'] < closest[1] * 0.8:
                diff_pct = ((1 - stats['avg_units'] / closest[1]) * 100)
                st.success(f"✅ Great job! You're using **{diff_pct:.0f}% LESS** than typical {closest[0]}")
                st.balloons()
            else:
                st.success("✅ Your consumption is within normal range for this house type")
        
        with tab4:
            st.subheader("🔮 Next Month Prediction")
            
            # Simple prediction
            recent_avg = df.tail(3)['units'].mean()
            predicted_units = recent_avg
            predicted_amount = calculate_bill(predicted_units)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                delta_units = predicted_units - stats['avg_units']
                st.metric(
                    "Expected Consumption",
                    f"{predicted_units:.0f} units",
                    delta=f"{delta_units:+.0f} vs avg"
                )
            
            with col2:
                delta_amount = predicted_amount - stats['avg_amount']
                st.metric(
                    "Expected Bill",
                    f"₹{predicted_amount:.0f}",
                    delta=f"₹{delta_amount:+.0f} vs avg"
                )
            
            with col3:
                best_case = calculate_bill(stats['min_units'])
                worst_case = calculate_bill(stats['max_units'])
                st.markdown(f"**Best Case:** ₹{best_case:.0f}")
                st.markdown(f"**Worst Case:** ₹{worst_case:.0f}")
                st.markdown(f"**Range:** ₹{worst_case - best_case:.0f}")
            
            st.markdown("---")
            st.info("💡 **Tip:** Prediction based on last 3 months average. Follow savings tips to reduce your next bill!")

else:
    # Welcome screen
    st.info("👈 **Get Started!** Use the sidebar to input your bills or load sample data")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ## 🎯 How to Use This Tool
        
        ### Step 1: Input Your Data
        - **Manual Entry:** Type your bills month by month
        - **Upload CSV:** Load bills from a file
        - **Sample Data:** Try with demo data first
        
        ### Step 2: Analyze
        Click the "Analyze My Bills" button to get:
        
        ✅ **Consumption Trends** - See your usage patterns  
        ✅ **Savings Tips** - Get personalized recommendations  
        ✅ **Comparisons** - See how you stack up  
        ✅ **Predictions** - Know your next bill estimate  
        
        ### Step 3: Save Money!
        Follow the tips and watch your bills drop! 💰
        
        ---
        
        ### 📄 CSV File Format
        ```
        month,units,amount
        Jan-24,250,1500
        Feb-24,280,1700
        Mar-24,320,2100
        ```
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "<p>⚡ Electricity Bill Optimizer | Made with ❤️ using Streamlit</p>"
    "<p>💡 Start saving money on your electricity bills today!</p>"
    "</div>",
    unsafe_allow_html=True
)