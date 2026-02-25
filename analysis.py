import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self, data):
        self.data = data
    
    def get_summary_statistics(self):
        """Get summary statistics for key metrics"""
        key_metrics = ['pulm_labconf_new', 'mdr_new', 'xdr']
        stats = {}
        
        for metric in key_metrics:
            if metric in self.data.columns:
                stats[metric] = {
                    'total': self.data[metric].sum(),
                    'mean': self.data[metric].mean(),
                    'median': self.data[metric].median(),
                    'std': self.data[metric].std(),
                    'min': self.data[metric].min(),
                    'max': self.data[metric].max()
                }
        
        return stats
    
    def get_yearly_trends(self):
        """Get yearly trends for key metrics"""
        if 'year' not in self.data.columns:
            return {}
        
        metrics = ['pulm_labconf_new', 'mdr_new', 'xdr']
        trends = {}
        
        for metric in metrics:
            if metric in self.data.columns:
                yearly = self.data.groupby('year')[metric].sum().reset_index()
                trends[metric] = {
                    'years': yearly['year'].tolist(),
                    'values': yearly[metric].tolist(),
                    'growth_rate': self._calculate_growth_rate(yearly[metric].tolist())
                }
        
        return trends
    
    def _calculate_growth_rate(self, values):
        """Calculate growth rate between first and last value"""
        if len(values) < 2:
            return 0
        return ((values[-1] - values[0]) / values[0]) * 100 if values[0] != 0 else 0
    
    def get_top_countries(self, metric='pulm_labconf_new', n=10):
        """Get top countries by metric"""
        if metric not in self.data.columns:
            return []
        
        top = self.data.groupby('country')[metric].sum().nlargest(n).reset_index()
        return top.to_dict('records')
    
    def get_regional_summary(self):
        """Get regional summary"""
        if 'g_whoregion' in self.data.columns:
            region_col = 'g_whoregion'
        else:
            region_col = 'Region'
        
        summary = self.data.groupby(region_col).agg({
            'pulm_labconf_new': ['sum', 'mean', 'count'],
            'mdr_new': 'sum' if 'mdr_new' in self.data.columns else lambda x: 0,
            'xdr': 'sum' if 'xdr' in self.data.columns else lambda x: 0
        }).round(2)
        
        return summary.to_dict()
    
    def get_mdr_trend(self):
        """Get MDR-TB trend over years"""
        if 'mdr_new' not in self.data.columns or 'year' not in self.data.columns:
            return {}
        
        mdr_trend = self.data.groupby('year')['mdr_new'].sum().reset_index()
        
        return {
            'years': mdr_trend['year'].tolist(),
            'values': mdr_trend['mdr_new'].tolist()
        }
    
    def get_correlation_analysis(self):
        """Get correlation between key variables"""
        key_vars = ['pulm_labconf_new', 'mdr_new', 'xdr', 'year']
        available = [v for v in key_vars if v in self.data.columns]
        
        if len(available) < 2:
            return {}
        
        corr_matrix = self.data[available].corr().round(3)
        
        # Find strongest correlations
        corr_pairs = []
        for i in range(len(available)):
            for j in range(i+1, len(available)):
                corr_pairs.append({
                    'var1': available[i],
                    'var2': available[j],
                    'correlation': corr_matrix.iloc[i, j]
                })
        
        corr_pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            'matrix': corr_matrix.to_dict(),
            'top_pairs': corr_pairs[:5]
        }