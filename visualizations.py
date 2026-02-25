# models/visualizations.py
import matplotlib
matplotlib.use('Agg')  # Must be set before importing pyplot
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import io
import base64
import threading
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# Configure matplotlib for thread-safe operation
plt.ioff()  # Turn off interactive mode

class Visualizer:
    def __init__(self, data):
        self.data = data
        self.region_names = {
            'AFR': 'Africa',
            'AMR': 'Americas', 
            'EMR': 'Eastern Mediterranean',
            'EUR': 'Europe',
            'SEA': 'South-East Asia',
            'WPR': 'Western Pacific'
        }
        self._lock = threading.Lock()  # Add thread lock for matplotlib operations
    
    def _fig_to_plotly(self, fig, title, width=1200, height=600):
        """Convert matplotlib figure to Plotly figure with embedded image"""
        with self._lock:  # Ensure thread-safe matplotlib operations
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
        
        # Create Plotly figure with the image
        plotly_fig = go.Figure()
        plotly_fig.add_layout_image(
            dict(
                source=f'data:image/png;base64,{img_str}',
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                layer="below"
            )
        )
        plotly_fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, family='Arial Black'),
                x=0.5,
                y=0.98
            ),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            width=width,
            height=height,
            margin=dict(l=0, r=0, t=50, b=0),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        return plotly_fig.to_json()
    
    def create_line_chart(self):
        """Create line chart for TB cases over years - from test1.ipynb"""
        with self._lock:  # Ensure thread-safe matplotlib operations
            plt.style.use('seaborn-v0_8-darkgrid')
            sns.set_palette("husl")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            yearly_cases = self.data.groupby('year')['pulm_labconf_new'].sum().reset_index()
            
            ax.plot(yearly_cases['year'], yearly_cases['pulm_labconf_new'], 
                     marker='o', linewidth=3, markersize=10, color="#FF0E0E", 
                     markerfacecolor="#03F32B", markeredgecolor='white', markeredgewidth=2)
            
            for i, (year, value) in enumerate(zip(yearly_cases['year'], yearly_cases['pulm_labconf_new'])):
                ax.text(year, value + 5000, f'{value:,.0f}', 
                         ha='center', va='bottom', fontweight='bold', fontsize=10)
            
            ax.set_title('Total Pulmonary Lab Confirmed TB Cases Over Years', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Cases', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xticks(yearly_cases['year'])
            ax.set_xticklabels(yearly_cases['year'], rotation=45)
            
            z = np.polyfit(yearly_cases['year'], yearly_cases['pulm_labconf_new'], 1)
            p = np.poly1d(z)
            ax.plot(yearly_cases['year'], p(yearly_cases['year']), "--", alpha=0.7, color="black",
                     label=f'Trend Line (slope={z[0]:,.0f} cases/year)')
            ax.legend()
            
            plt.tight_layout()
        
        return self._fig_to_plotly(fig, 'Total Pulmonary Lab Confirmed TB Cases Over Years', 1200, 600)
    
    def create_bar_chart(self, top_n=10):
        """Create bar chart for top countries - from test1.ipynb"""
        with self._lock:
            fig, ax = plt.subplots(figsize=(14, 8))
            
            top_countries = self.data.groupby('country')['pulm_labconf_new'].sum().nlargest(top_n).reset_index()
            
            colors = plt.cm.YlOrRd_r(np.linspace(0.2, 0.9, top_n))
            bars = ax.barh(top_countries['country'], top_countries['pulm_labconf_new'], color=colors)
            
            for i, (bar, value) in enumerate(zip(bars, top_countries['pulm_labconf_new'])):
                ax.text(value + 5000, bar.get_y() + bar.get_height()/2, 
                         f'{value:,.0f}', va='center', fontweight='bold', fontsize=11)
            
            ax.set_title(f'Top {top_n} Countries with Highest TB Cases', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Total Cases', fontsize=12, fontweight='bold')
            ax.set_ylabel('Country', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            
            plt.tight_layout()
        
        return self._fig_to_plotly(fig, f'Top {top_n} Countries with Highest TB Cases', 1400, 800)
    
    def create_pie_chart(self):
        """Create pie chart for regional distribution - from test1.ipynb"""
        with self._lock:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            if 'g_whoregion' in self.data.columns:
                region_col = 'g_whoregion'
            else:
                region_col = 'Region'
            
            region_data = self.data.groupby(region_col)['pulm_labconf_new'].sum().reset_index()
            
            region_data['region_full'] = region_data[region_col].map(self.region_names)
            
            colors = plt.cm.Set3(np.linspace(0, 1, len(region_data)))
            explode = [0.05] * len(region_data)
            
            total = region_data['pulm_labconf_new'].sum()
            
            wedges, texts, autotexts = ax.pie(region_data['pulm_labconf_new'], 
                                              labels=region_data['region_full'],
                                              autopct=lambda pct: f'{pct:.1f}%\n({pct*total/100:,.0f})',
                                              colors=colors,
                                              explode=explode,
                                              startangle=90,
                                              textprops={'fontsize': 10, 'fontweight': 'bold'})
            
            ax.set_title('TB Cases Distribution by WHO Region', fontsize=16, fontweight='bold', pad=20)
            ax.axis('equal')
            
            plt.tight_layout()
        
        return self._fig_to_plotly(fig, 'TB Cases Distribution by WHO Region', 1000, 800)
    
    def create_correlation_matrix(self):
        """Create correlation matrix heatmap - from test1.ipynb"""
        with self._lock:
            fig, ax = plt.subplots(figsize=(16, 12))
            
            key_columns = ['pulm_labconf_new', 'pulm_labconf_ret', 'pulm_labconf_unk', 
                           'r_rlt_new', 'r_rlt_ret', 'rr_new', 'rr_ret', 
                           'mdr_new', 'mdr_ret', 'xdr', 'year']
            
            available_cols = [col for col in key_columns if col in self.data.columns]
            corr_data = self.data[available_cols].select_dtypes(include=[np.number])
            
            correlation_matrix = corr_data.corr()
            
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            
            # Create heatmap using seaborn
            sns.heatmap(correlation_matrix, 
                        mask=mask,
                        annot=True,
                        center=0,
                        cmap='viridis',
                        square=True, 
                        linewidths=1, 
                        cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
                        fmt='.2f',
                        annot_kws={'size': 10, 'fontweight': 'bold'},
                        ax=ax)
            
            ax.set_title('Correlation Matrix of Key TB Indicators', fontsize=16, fontweight='bold', pad=20)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=11)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
            
            plt.tight_layout()
        
        return self._fig_to_plotly(fig, 'Correlation Matrix of Key TB Indicators', 1600, 1200)
    
    def create_scatter_plot(self):
        """Create scatter plot for TB vs MDR cases - from test1.ipynb"""
        if 'mdr_new' not in self.data.columns:
            return None
        
        with self._lock:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            df_scatter = self.data.copy()
            if 'g_whoregion' in df_scatter.columns:
                df_scatter['region_full'] = df_scatter['g_whoregion'].map(self.region_names)
            else:
                df_scatter['region_full'] = df_scatter['Region']
            
            region_colors = {
                'Africa': '#FF6B6B',
                'Americas': '#4ECDC4',
                'Eastern Mediterranean': '#45B7D1',
                'Europe': '#96CEB4',
                'South-East Asia': '#FFE194',
                'Western Pacific': '#D4A5A5'
            }
            
            for region, color in region_colors.items():
                region_data = df_scatter[df_scatter['region_full'] == region]
                if len(region_data) > 0:
                    ax.scatter(region_data['pulm_labconf_new'], 
                               region_data['mdr_new'],
                               c=color, 
                               label=region,
                               alpha=0.6,
                               s=50,
                               edgecolors='white',
                               linewidth=1)
            
            # Add trend line
            valid_data = df_scatter[['pulm_labconf_new', 'mdr_new']].dropna()
            if len(valid_data) > 0:
                z = np.polyfit(valid_data['pulm_labconf_new'], valid_data['mdr_new'], 1)
                p = np.poly1d(z)
                x_sorted = valid_data['pulm_labconf_new'].sort_values()
                ax.plot(x_sorted, p(x_sorted), "--", linewidth=2, alpha=0.8, color='red',
                         label=f'Trend Line (slope={z[0]:.4f})')
                
                correlation = valid_data['pulm_labconf_new'].corr(valid_data['mdr_new'])
                ax.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                         transform=ax.transAxes, fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            ax.set_xlabel('Pulmonary Lab Confirmed New TB Cases', fontsize=12, fontweight='bold')
            ax.set_ylabel('MDR-TB Cases', fontsize=12, fontweight='bold')
            ax.set_title('Relationship Between New TB Cases and MDR-TB Cases by WHO Region', 
                      fontsize=16, fontweight='bold', pad=20)
            
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.set_xscale('log')
            ax.set_yscale('log')
            
            plt.tight_layout()
        
        return self._fig_to_plotly(fig, 'Relationship Between New TB Cases and MDR-TB Cases by WHO Region', 1200, 800)
    
    def create_boxplot(self):
        """Create boxplot for TB cases distribution - from test1.ipynb"""
        with self._lock:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            data = self.data['pulm_labconf_new'].dropna()
            
            bp = ax.boxplot(data,
                            vert=True,
                            patch_artist=True,
                            showmeans=True,
                            meanline=True,
                            widths=0.5,
                            boxprops=dict(facecolor='#74b9ff', color='#2d3436', linewidth=2, alpha=0.8),
                            whiskerprops=dict(color='#2d3436', linewidth=2, linestyle='-'),
                            capprops=dict(color='#2d3436', linewidth=2),
                            medianprops=dict(color='#e17055', linewidth=3),
                            meanprops=dict(color='#00b894', linewidth=2, linestyle='--'),
                            flierprops=dict(marker='o', markerfacecolor='#fab1a0', 
                                           markersize=6, alpha=0.6, markeredgecolor='#d63031'))
            
            ax.set_xticks([1])
            ax.set_xticklabels(['New Pulmonary TB Cases'], fontsize=14, fontweight='bold')
            ax.set_ylabel('Number of Cases', fontsize=14, fontweight='bold', labelpad=15)
            ax.set_title('Distribution of New Pulmonary TB Cases', 
                         fontsize=18, fontweight='bold', pad=20, color='#2d3436')
            
            ax.set_ylim(bottom=0)
            ax.grid(True, axis='y', alpha=0.15, linestyle='--', color='#636e72')
            ax.set_facecolor('#f5f6fa')
            
            q1, q2, q3 = np.percentile(data, [25, 50, 75])
            ax.axhline(y=q2, xmin=0.65, xmax=0.9, color='#e17055', linestyle='--', linewidth=1.5, alpha=0.5)
            ax.axhline(y=q1, xmin=0.65, xmax=0.9, color='#0984e3', linestyle='--', linewidth=1.5, alpha=0.5)
            ax.axhline(y=q3, xmin=0.65, xmax=0.9, color='#0984e3', linestyle='--', linewidth=1.5, alpha=0.5)
            
            from matplotlib.lines import Line2D
            legend_elements = [
                Line2D([0], [0], color='#e17055', lw=3, label='Median'),
                Line2D([0], [0], color='#00b894', lw=2, linestyle='--', label='Mean'),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='#fab1a0',
                       markersize=6, label='Outliers', markeredgecolor='#d63031')
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=11, 
                      framealpha=0.9, edgecolor='#2d3436')
            
            plt.tight_layout()
        
        return self._fig_to_plotly(fig, 'Distribution of New Pulmonary TB Cases', 1200, 800)
    
    def create_region_boxplot(self):
        """Create boxplot by region - from test1.ipynb"""
        with self._lock:
            fig, ax = plt.subplots(figsize=(14, 8))
            
            if 'g_whoregion' in self.data.columns:
                region_col = 'g_whoregion'
                self.data['region_full'] = self.data[region_col].map(self.region_names)
            else:
                self.data['region_full'] = self.data['Region']
            
            # Remove any rows with missing region or values
            plot_data = self.data[['region_full', 'pulm_labconf_new']].dropna()
            regions = plot_data['region_full'].unique()
            
            region_data = []
            for region in regions:
                region_values = plot_data[plot_data['region_full'] == region]['pulm_labconf_new']
                region_data.append(region_values)
            
            medians = [data.median() for data in region_data]
            norm_medians = (medians - min(medians)) / (max(medians) - min(medians) + 1e-10)
            colors = plt.cm.viridis(norm_medians)
            
            bp = ax.boxplot(region_data,
                            labels=regions,
                            patch_artist=True,
                            showmeans=True,
                            meanline=True,
                            boxprops=dict(linewidth=2, color='#2d3436'),
                            whiskerprops=dict(color='#2d3436', linewidth=1.5),
                            capprops=dict(color='#2d3436', linewidth=1.5),
                            medianprops=dict(color='#e17055', linewidth=2.5),
                            meanprops=dict(color='#00b894', linewidth=2, linestyle='--'),
                            flierprops=dict(marker='o', markerfacecolor='#fab1a0', 
                                           markersize=5, alpha=0.5, markeredgecolor='#d63031'))
            
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.8)
            
            ax.set_ylabel('Number of New Pulmonary Cases', fontsize=14, fontweight='bold')
            ax.set_xlabel('WHO Region', fontsize=14, fontweight='bold')
            ax.set_title('TB Cases Distribution by WHO Region', 
                         fontsize=18, fontweight='bold', pad=20)
            ax.set_ylim(bottom=0)
            ax.grid(True, axis='y', alpha=0.15, linestyle='--')
            ax.set_facecolor('#f5f6fa')
            
            plt.tight_layout()
        
        return self._fig_to_plotly(fig, 'TB Cases Distribution by WHO Region', 1400, 800)
    
    def generate_report(self):
        """Generate HTML report with all visualizations"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TB Data Analysis Report</title>
            <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #f5f5f5;
                }
                h1 { 
                    color: #2c3e50; 
                    text-align: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }
                h2 { 
                    color: #34495e; 
                    margin-top: 30px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #3498db;
                }
                .chart-container { 
                    margin: 20px 0; 
                    background: white; 
                    padding: 20px; 
                    border-radius: 10px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                .stats { 
                    display: grid; 
                    grid-template-columns: repeat(4, 1fr); 
                    gap: 20px; 
                    margin: 20px 0; 
                }
                .stat-card { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 20px; 
                    border-radius: 10px; 
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                .stat-card h3 {
                    margin: 0 0 10px 0;
                    font-size: 16px;
                    opacity: 0.9;
                }
                .stat-card p {
                    margin: 0;
                    font-size: 24px;
                    font-weight: bold;
                }
                .footer { 
                    text-align: center; 
                    margin-top: 30px; 
                    color: #7f8c8d;
                    padding: 20px;
                    border-top: 1px solid #ddd;
                }
                .timestamp {
                    text-align: right;
                    color: #7f8c8d;
                    margin-bottom: 20px;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <h1>TB Data Analysis Report</h1>
            <div class="timestamp">Generated on: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</div>
            
            <div class="stats">
        """
        
        # Add statistics
        total_cases = self.data['pulm_labconf_new'].sum()
        total_mdr = self.data['mdr_new'].sum() if 'mdr_new' in self.data.columns else 0
        total_xdr = self.data['xdr'].sum() if 'xdr' in self.data.columns else 0
        years_range = f"{int(self.data['year'].min())}-{int(self.data['year'].max())}" if 'year' in self.data.columns else "N/A"
        
        html_content += f"""
                <div class="stat-card"><h3>Total TB Cases</h3><p>{total_cases:,.0f}</p></div>
                <div class="stat-card"><h3>Total MDR-TB</h3><p>{total_mdr:,.0f}</p></div>
                <div class="stat-card"><h3>Total XDR-TB</h3><p>{total_xdr:,.0f}</p></div>
                <div class="stat-card"><h3>Years</h3><p>{years_range}</p></div>
            </div>
        """
        
        # Add all charts
        charts = [
            ('line', 'TB Cases Over Years'),
            ('bar', 'Top Countries by TB Cases'),
            ('pie', 'Regional Distribution'),
            ('correlation', 'Correlation Matrix'),
            ('scatter', 'TB vs MDR-TB Cases'),
            ('boxplot', 'Distribution of TB Cases'),
            ('region_boxplot', 'Distribution by Region')
        ]
        
        for chart_type, title in charts:
            try:
                print(f"Generating {chart_type} chart for report...")
                if chart_type == 'bar':
                    chart_json = self.create_bar_chart(10)
                elif chart_type == 'scatter':
                    chart_json = self.create_scatter_plot()
                elif chart_type == 'correlation':
                    chart_json = self.create_correlation_matrix()
                elif chart_type == 'boxplot':
                    chart_json = self.create_boxplot()
                elif chart_type == 'region_boxplot':
                    chart_json = self.create_region_boxplot()
                elif chart_type == 'line':
                    chart_json = self.create_line_chart()
                elif chart_type == 'pie':
                    chart_json = self.create_pie_chart()
                
                if chart_json:
                    html_content += f'<div class="chart-container"><h2>{title}</h2><div id="{chart_type}"></div></div>\n'
                    html_content += f'<script>var {chart_type}Data = {chart_json}; Plotly.newPlot("{chart_type}", {chart_type}.data, {chart_type}.layout);</script>\n'
                else:
                    html_content += f'<div class="chart-container"><h2>{title}</h2><p style="color:orange">No data available for this chart</p></div>\n'
            except Exception as e:
                print(f"Error adding {chart_type} to report: {e}")
                html_content += f'<div class="chart-container"><h2>{title}</h2><p style="color:red">Error generating chart: {str(e)}</p></div>\n'
        
        html_content += """
            <div class="footer">
                <p>Report generated automatically by TB Data Analysis Platform</p>
                <p>Data source: WHO TB surveillance data</p>
            </div>
        </body>
        </html>
        """
        
        return html_content