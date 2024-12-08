from static.elements import gradient_text
import streamlit as st
from utils.db import execute_query
from static.elements import gradient_button, animated_container, tile, line_chart, scatter_chart, metric_tile
import time
import pandas as pd
from utils.stats import calculate_trade_statistics, get_account_trades, get_user_accounts, get_account_info

def AccountsPage():
    with st.container(border=False):
        st.subheader("My Accounts", anchor=False)

        user_id = st.session_state.get("user_id", "User")

        # Get the list of account numbers for the user
        account_numbers = get_user_accounts(user_id)

        # Prepare the account number options for the selectbox
        if account_numbers:
            account_options = account_numbers
        else:
            account_options = ["No accounts available"]

        col1, col2 = st.columns(2, vertical_alignment="bottom")

        # Create the selectbox with the retrieved account number options
        with col1:
            account_selection = st.selectbox("Select Account", account_options)

        with col2:
            @st.dialog("Add Account")
            def add_account_dialog():
                account_number = st.text_input("Account Number", placeholder="Account Number")
                password = st.text_input("Investor Password", placeholder="Investor Password", type="password")
                server = st.text_input("Server", placeholder="Server")
                platform = st.selectbox("Platform", ("mt4", "mt5"), placeholder="Platform")

                confirm_add_account_button = gradient_button("Add Account", key="confirm_add_account_button", icon=":material/check:")

                if confirm_add_account_button:
                    with st.spinner("Adding your account..."):
                        time.sleep(2)
                    st.success("Account successfully added! (TEST)")
                    time.sleep(2)
                    st.rerun()

            open_add_account_dialog = gradient_button(label="Add Account", key="open_add_account_dialog", icon=":material/add_circle:")

            if open_add_account_dialog: add_account_dialog()

        # Check if an account is selected (ensure account_selection is not "No accounts available")
        if account_selection and account_selection != "No accounts available":
            # Query the database to get the `api_account_id` and `account_id` for the selected account
            account_info = get_account_info(user_id, account_selection)  # Assuming this returns (api_account_id, account_id)

            if account_info:
                api_account_id, account_id = account_info  # Unpack the account info tuple

                # Retrieve trades for the specific account
                trades = get_account_trades(api_account_id)

                # Convert the result into a DataFrame
                trades_df = pd.DataFrame(trades)
                

                if trades_df.empty:
                    st.info("No trading data available.")

                else:
                    trades_df['close_time'] = pd.to_datetime(trades_df['close_time'])
                    trades_df['cum_gain'] = trades_df['gain'].cumsum()
                    trades_df['type'] = trades_df['type'].replace({
                                            'DEAL_TYPE_SELL': 'Sell',
                                            'DEAL_TYPE_BUY': 'Buy'
                                        })

                    statistics = calculate_trade_statistics(trades_df)

                    # Create the new DataFrame with renamed columns
                    trades_display = trades_df.rename(columns={
                        'ticket': 'Ticket',
                        'symbol': 'Symbol',
                        'type': 'Type',
                        'volume': 'Volume',
                        'open_time': 'Open Time',
                        'open_price': 'Open Price',
                        'close_time': 'Close Time',
                        'close_price': 'Close Price',
                        'profit': 'Profit',
                        'gain': 'Gain'
                    })[
                        ['Ticket', 'Symbol', 'Type', 'Volume', 'Open Time', 
                        'Open Price', 'Close Time', 'Close Price', 'Profit', 'Gain']
                    ]

                    performance, trade_journal, advanced_analytics, ai_insights, account_settings = st.tabs(["Performance", 
                                                                                                            "Trade Journal", 
                                                                                                            "Advanced Analytics", 
                                                                                                            "AI Insights", 
                                                                                                            "Settings"
                                                                                                            ])

                    with performance: # ------ PERFORMANCE STATS ------ #
                        st.subheader("Performance", anchor=False)
                        
                        performance_overview, risk_drawdown_analysis, trading_efficiency, symbol_breakdown, time_analysis, profitability, advanced_statistics = st.tabs(["Performance Overview",
                                                                                                                                                                         "Risk & Drawdown Analysis",
                                                                                                                                                                         "Trading Activity & Efficiency",
                                                                                                                                                                         "Instrument & Symbol Breakdown",
                                                                                                                                                                         "Time-Based Analysis",
                                                                                                                                                                         "Profitability & Risk Ratios",
                                                                                                                                                                         "Advanced Statistics"
                                                                                                                                                                         ])

                        with performance_overview:
                            st.subheader("Performance Overview", anchor=False)
                            st.caption('''A high-level summary of the account’s overall performance, profitability, and key return metrics.''')

                            st.markdown('''
                                            **Charts & Visuals:**

                                            - **Balance (Line Chart)**: Show evolution of account balance over time.
                                            - **Daily & Cumulative Net P/L (Bar and Line Chart)**: Bar for daily P/L, line for cumulative P/L over same timeline.
                                            - **Net Daily P/L Bar**: Daily profits/losses as a bar chart.

                                            **KPIs (Tiles/Tables):**

                                            - Total P/L
                                            - Gross Profit
                                            - Gross Loss
                                            - Dividends
                                            - Swaps
                                            - Commissions (Total Commissions, Total Fees)
                                            - Annualised Return
                                            - Average Daily P&L
                                            - Monthly Gain (Table: month-by-month P/L)
                                            - Best Month & Lowest Month + related figures (e.g. $13,582.24 in Aug 2024)
                                            - Average per Month
                                            - Account Balance & P/L (Overall summaries)
                                            - ATH quote, Days since ATH, Return since ATH
                                            - Top 5 Symbol Net Profit (Tile or small table)
                                        ''')

                        with risk_drawdown_analysis:
                            st.subheader("Risk & Drawdown Analysis", anchor=False)
                            st.caption('''Focus on how risk is managed, the extent of drawdowns, variability in returns, and volatility measures.''')

                            st.markdown('''
                                            **Charts & Visuals:**

                                            - **Balance vs Drawdown Line Chart**
                                            - **Drawdown Chart & Distribution**: A line chart showing drawdown over time plus a histogram of drawdown depths.
                                            - **Risk Management (VaR) Chart**: Plot minimum, maximum, and monthly VaR.
                                            - **Max. positive/negative excursion per position** (Bar Chart)
                                            - **Duration vs Profit distribution matrix** (Heatmap/Scatter)
                                            - **Return Distribution (Daily/Weekly histogram)**

                                            **KPIs (Tiles):**

                                            - Max Drawdown (Absolute & %)
                                            - Average Drawdown (Absolute & %)
                                            - Max VaR, Min VaR
                                            - Annualised Volatility
                                            - Daily STDV
                                            - Skewness, Kurtosis
                                            - Sortino ratio, Sharpe ratio
                                        ''')
                            
                        with trading_efficiency:
                            st.subheader("Trading Activity & Efficiency", anchor=False)
                            st.caption('''Drill down into the execution metrics such as the number of trades, their success rate, and trade-by-trade profitability/duration patterns.''')

                            st.markdown('''
                                            **Charts & Visuals:**

                                            - **P/L per Day of the Week (Bar Chart)**
                                            - **Long/Short Count with Net Line overlay**
                                            - **Donut Chart showing Long vs Short Split**
                                            - **Bar Chart for Long Sum & Short Sum Each Day of Week**

                                            **KPIs (Tiles/Tables):**

                                            - Total Number of Trades
                                            - Number of Winning Trades, Losing Trades, Break Even Trades
                                            - Win % (Trade Win %)
                                            - Average Winning Trade (in cash/%)
                                            - Average Losing Trade (in cash/%)
                                            - Payoff Ratio (Average Win / Average Loss)
                                            - Trade Expectancy
                                            - Average Hold Time (All, Winning, Losing, Scratch)
                                            - Max Consecutive Wins, Max Consecutive Losses
                                            - Open Trades (current)
                                            - Daily trade frequency
                                            - pct Long Exposure
                                        ''')

                        with symbol_breakdown:
                            st.subheader("Instrument & Symbol Breakdown", anchor=False)
                            st.caption('''Performance by instrument, helping identify which symbols or assets contribute most to P/L.''')
                                       
                            st.markdown('''
                                            **Charts & Visuals:**

                                            - **Donut Symbol Breakdown (P/L or Volume)**
                                            - **Profit Factor for each symbol (Bar Chart)**
                                            - **Net profit for each symbol (Bar Chart)**

                                            **KPIs (Tiles/Tables):**

                                            - Fees for each symbol
                                            - Asset allocation (donut chart with breakdown, tiles for number of trades, win %, return per symbol)
                                            - Top 5 Symbol Net Profit (Gain and Cash)
                                        ''')
                            
                        with time_analysis:
                            st.subheader("Time-Based Analysis", anchor=False)
                            st.caption('''Evaluate how performance differs by time segments (day of week, month, session''')

                            st.markdown('''
                                            **Charts & Visuals:**

                                            - **Calendar Chart (Monthly view of daily P/L)**
                                            - **Balance vs. Deposit Load Line Chart**
                                            - **Return Distribution for day of week (Line chart with cumulative returns for each day)**
                                            - **Trade Time Performance Scatter** (e.g. plot trades over time of day)
                                            - **Trading time distribution (bar chart or donut) by session (Europe/America/Asia)**

                                            **KPIs (Tiles/Tables):**

                                            - Trades per Week
                                            - Current Winning day streak
                                            - Max Consecutive Winning Days, Max Consecutive Losing Days
                                            - Winning Days, Losing Days, Breakeven Days
                                            - Total Trading Days
                                            - Logged Days
                                        ''')
                        
                        with profitability:
                            st.subheader("Profitability & Risk Ratios", anchor=False)
                            st.caption('''Focus on the ratios and metrics that describe risk-adjusted returns and efficiency.''')

                            st.markdown('''
                                            **Charts & Visuals:**

                                            - **P/L Chart with Profit/Loss columns and Net Line Overlay**
                                            - **MFE/MAE over time as stacked chart** (Max Favourable/Adverse excursion)
                                            - **Balance vs. Deposit Load** (line chart)
                                            - **Best vs. Worst Trade (bar)**

                                            **KPIs (Tiles/Tables):**

                                            - Profit Factor (overall and by symbol)
                                            - Recovery Factor
                                            - Sortino ratio, Sharpe ratio
                                            - Return since ATH
                                            - Average Planned R-Multiple, Average Realized R-Multiple
                                            - Black Box Score (if applicable)
                                        ''')

                        with advanced_statistics:
                            st.subheader("Advanced Statistics & Distributions", anchor=False)
                            st.caption('''More sophisticated statistical analyses and return distributions.''')

                            st.markdown('''
                                            **Charts & Visuals:**

                                            - **Trade Duration Performance Scatter** (plot duration vs. P/L)
                                            - **Return distribution histograms (Daily/Weekly)**
                                            - **Drawdown distribution histogram**

                                            **KPIs (Tiles/Tables):**

                                            - Skewness, Kurtosis
                                            - Annualised return & volatility
                                            - Distribution metrics (how many days/weeks are positive/negative within certain return bands)
                                        ''')




                        # ------ OVERVIEW ------ #

                        # st.subheader("Overview", anchor=False)
                        # st.caption(f"General performance overview for account {account_selection}.")

                        # chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        # with chart:
                        #     with tile("overview_chart", 385, border=True):
                        #         st.markdown("**Overview**")

                        #         line_chart(
                        #             data=trades_df, 
                        #             x='close_time', 
                        #             y='cum_gain', 
                        #             x_label='Time', 
                        #             y_label='Cumulative Gain (%)', 
                        #             height=335
                        #         )

                        # with stats:
                        #     animated_container(
                        #         key="performance_overview_stat_1", 
                        #         content=f"""
                        #             <div style="line-height: 1.45;">
                        #                 <p style="margin: 0; font-size: 0.75em; color: #E8E8E8;">Total Gain</p>
                        #                 <p style="margin: 0; font-size: 1em; font-weight: bold; color: #E8E8E8;">{statistics['Total Gain']}</p>
                        #             </div>
                        #             """
                        #         )
                        #     #metric_tile("performance_overview_stat_1", "Total Gain", statistics['Total Gain'], 39, "secondary", tooltip=None, border=False)
                        #     metric_tile("performance_overview_stat_2", "Win Rate", statistics['Win Rate'], 39, "primary", tooltip="Percentage of winning trades.", border=True)
                        #     metric_tile("performance_overview_stat_3", "Profit Factor", statistics['Profit Factor'], 39, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_overview_stat_4", "Account Age", statistics['Account Age'], 39, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_overview_stat_5", "Most Traded Symbol", statistics['Most Traded Symbol'], 39, "primary", tooltip=None, border=True)

                        # st.divider()

                        # # ------ TRADE EFFICIENCY ------ #
                    
                        # st.subheader("Trade Efficiency", anchor=False)
                        # st.caption("Evaluate the effectiveness and precision of recent trades based on set metrics.")

                        # chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        # with chart:
                        #     with tile("trade_efficiency_chart", 385, border=True):
                        #         st.markdown("**Gain vs. Duration**")

                        #         scatter_chart(
                        #             data=trades_df, 
                        #             x='duration_mins', 
                        #             y='gain', 
                        #             x_label='Duration (Mins)', 
                        #             y_label='Gain (%)', 
                        #             height=335
                        #         )

                        # with stats:
                        #     metric_tile("performance_efficiency_stat_1", "Avg Trade Duration", statistics['Avg Trade Duration'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_efficiency_stat_2", "Avg Profit Per Trade", statistics['Avg Profit Per Trade'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_efficiency_stat_3", "Max Profit", statistics['Max Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_efficiency_stat_4", "Min Profit", statistics['Min Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_efficiency_stat_5", "Most Frequent Type", statistics['Most Frequent Type'], 40, "primary", tooltip=None, border=True)

                        # st.divider()

                        # # ------ RISK ANALYSIS ------ #
                    
                        # st.subheader("Risk Analysis", anchor=False)
                        # st.caption("Assess trading risks and operational efficiency to optimize risk management strategies.")

                        # chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        # with chart:
                        #     with tile("risk_analysis_chart_1", 170, border=True):
                        #         st.markdown("**Chart 1**")

                        #     with tile("risk_analysis_chart_2", 170, border=True):
                        #         st.markdown("**Chart 2**")

                        # with stats:
                        #     metric_tile("performance_risk_stat_1", "Max Drawdown", statistics['Max Drawdown'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_risk_stat_2", "Avg Risk Per Trade", statistics['Avg Risk Per Trade'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_risk_stat_3", "Sharpe Ratio", statistics['Sharpe Ratio'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_risk_stat_4", "Risk Reward Ratio", statistics['Risk Reward Ratio'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_risk_stat_5", "Trades at Risk", statistics['Trades at Risk'], 40, "primary", tooltip=None, border=True)

                        # with tile("risk_analysis_chart_3", 170, border=True):
                        #         st.markdown("**Chart 3**")

                        # st.divider()

                        # # ------ BEHAVIOURAL PATTERNS ------ #
                    
                        # st.subheader("Behavioural Patterns", anchor=False)
                        # st.caption("Identify trends in trading behavior that impact performance outcomes.")

                        # chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        # with chart:
                        #     with tile("behavioural_patterns_chart", 385, border=True):
                        #         st.markdown("**Chart**")

                        # with stats:
                        #     metric_tile("performance_behaviour_stat_1", "Favourite Symbol", statistics['Most Frequent Symbol'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_behaviour_stat_2", "Most Active Time", statistics['Most Active Time'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_behaviour_stat_3", "Avg Trade Volume", statistics['Avg Trade Volume'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_behaviour_stat_4", "Largest Trade", statistics['Largest Volume Trade'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_behaviour_stat_5", "Expected Outcome", statistics['Most Frequent Outcome'], 40, "primary", tooltip=None, border=True)

                        # st.divider()

                        # # ------ MARKET CONDITION ANALYSIS ------ #
                    
                        # st.subheader("Market Condition Analysis", anchor=False)
                        # st.caption("Analyse how different market conditions influence trade decisions and results.")

                        # chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        # with chart:
                        #     with tile("market_condition_chart", 385, border=True):
                        #         st.markdown("**Chart**")

                        # with stats:
                        #     metric_tile("performance_market_stat_1", "Best Symbol Profit", statistics['Best Symbol Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_market_stat_2", "Worst Symbol Profit", statistics['Worst Symbol Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_market_stat_3", "Most Traded Symbol", statistics['Most Traded Symbol'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_market_stat_4", "Stat 4", "Value", 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_market_stat_5", "Stat 5", "Value", 40, "primary", tooltip=None, border=True)

                        # st.divider()

                        # # ------ DAILY/WEEKLY PERFORMANCE SUMMARY ------ #
                    
                        # st.subheader("Daily/Weekly Performance Summary", anchor=False)
                        # st.caption("Summary of performance metrics over daily and weekly intervals for tracking progress and trends.")

                        # chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        # with chart:
                        #     with tile("daily_weekly_summary_chart", 385, border=True):
                        #         st.markdown("**Chart**")

                        # with stats:
                        #     metric_tile("performance_summary_stat_1", "Best Day Profit", statistics['Best Day Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_summary_stat_2", "Worst Day Profit", statistics['Worst Day Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_summary_stat_3", "Average Daily Profit", statistics['Average Daily Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_summary_stat_4", "Best Week Profit", statistics['Best Week Profit'], 40, "primary", tooltip=None, border=True)
                        #     metric_tile("performance_summary_stat_5", "Worst Week Profit", statistics['Worst Week Profit'], 40, "primary", tooltip=None, border=True)

                    with trade_journal: # ------ TRADING JOURNAL ------ #
                        st.subheader("Trading Jorunal", anchor=False)
                        st.caption(f"Journal of all trades for account {account_selection}.")

                        # Add an empty Notes column if not present
                        if "Notes" not in trades_display.columns:
                            trades_display['Notes'] = ""

                        # Editable table with disabled columns for read-only data
                        edited_trades_display = st.data_editor(
                            trades_display,
                            column_config={
                                "Ticket": "Ticket",
                                "Symbol": "Symbol",
                                "Type": "Trade Type",
                                "Volume": "Volume",
                                "Open Time": "Open Time",
                                "Open Price": "Open Price",
                                "Close Time": "Close Time",
                                "Close Price": "Close Price",
                                "Profit": "Profit",
                                "Gain": "Gain",
                                "Notes": st.column_config.TextColumn(
                                    "Notes",
                                    help="Add notes for each trade",
                                    max_chars=500,
                                ),
                            },
                            disabled=["Ticket", "Symbol", "Type", "Volume", "Open Time", 
                                    "Open Price", "Close Time", "Close Price", "Profit", "Gain"],
                            hide_index=True,
                            use_container_width=True
                        )

                    with advanced_analytics: # ------ Advanced Analytics ------ #
                        st.subheader("Advanced Analytics", anchor=False)
                        st.caption(f"Avanced analytical tools to delve further into your trading performance for account {account_selection}.")

                        # Parse dates and extract day of the week
                        trades_display['Open Time'] = pd.to_datetime(trades_display['Open Time'])
                        trades_display['Day of Week'] = trades_display['Open Time'].dt.day_name()

                        filter, run = st.columns(2, vertical_alignment="top")

                        with run:
                            with st.popover("Filters", icon=":material/filter_alt:", use_container_width=True):
                                
                                st.subheader("What-If Analysis Filters", anchor=False)
                                st.caption("Apply filters to your original trading history, to identify areas of potential improvement to your strategy.")
                                
                                with st.expander("Weekday", icon=":material/date_range:"):

                                    # 1. Checkbox for trading days
                                    all_days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                                    existing_days = trades_display['Day of Week'].unique()

                                    # Display checkboxes for each day, with existing days checked by default
                                    selected_days = []
                                    st.markdown("**Trading Days**")
                                    for day in all_days_of_week:
                                        # If the day exists in the data, make the checkbox enabled and checked by default
                                        if day in existing_days:
                                            if st.checkbox(day, value=True):
                                                selected_days.append(day)
                                        # If the day doesn't exist in the data, display the checkbox but disable it
                                        else:
                                            st.checkbox(day, value=False, disabled=True)

                            
                                with st.expander("Types", icon=":material/swap_vert:"):
                                    # Get unique trade directions present in the data
                                    all_directions = ['Buy', 'Sell']
                                    existing_directions = trades_display['Type'].unique()

                                    # Sidebar for "What-If" analysis
                                    st.markdown("**Trade Direction**")

                                    # Display checkboxes for each trade direction, with existing directions checked by default
                                    selected_directions = []
                                    for direction in all_directions:
                                        # If the direction exists in the data, make the checkbox enabled and checked by default
                                        if direction in existing_directions:
                                            if st.checkbox(direction, value=True):
                                                selected_directions.append(direction)
                                        # If the direction doesn't exist in the data, display the checkbox but disable it
                                        else:
                                            st.checkbox(direction, value=False, disabled=True)

                            
                                with st.expander("Symbols", icon=":material/paid:"):

                                    # 3. Checkbox for symbols
                                    symbols = trades_display['Symbol'].unique()
                                    selected_symbols = st.multiselect(
                                        "Select Symbols", options=symbols, default=symbols
                                    )

                        # Filter the dataframe based on selected options
                        filtered_df = trades_display[
                            (trades_display['Day of Week'].isin(selected_days)) &
                            (trades_display['Symbol'].isin(selected_symbols)) &
                            (trades_display['Type'].isin(selected_directions))
                        ]

                        # Calculate new cumulative gain on the filtered dataframe
                        filtered_df['Total Gain'] = filtered_df['Gain'].cumsum()


                        filtered_df = filtered_df.drop(columns=['Notes', 'Day of Week'])

                        # Display filtered results
                        with filter:
                            st.subheader("Filtered Trades", anchor=False)

                        st.caption("See below your trading history, with the filters applied.")
                        st.dataframe(filtered_df, hide_index=True)

                        # Display impact on cumulative gain
                        st.subheader("Impact of Filters on Cumulative Gain")
                        with tile("overview_chart", 385, border=True):
                            st.markdown("**Filtered Trading Performance**")

                            line_chart(
                                filtered_df, 
                                'Open Time', 
                                'Total Gain', 
                                'Open Time', 
                                'Cumulative Gain (%)',
                                height=335
                                )
                        
        else:
            st.info("No Account Selected")

if __name__ == "__main__":
    AccountsPage()
