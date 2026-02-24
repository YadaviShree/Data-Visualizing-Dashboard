# 🦠 TB Data Analysis Platform  
### A Comprehensive Tool for Tuberculosis Surveillance Data Analysis

| Key | Value |
|-----|-------|
| **Version** | 1.0.0 |
| **Python** | 3.8+ |
| **Flask** | 2.0+ |
| **Plotly** | Interactive |
| **License** | MIT |

---

## 📄 Abstract

The **TB Data Analysis Platform** is a comprehensive web-based application for visualizing and analyzing global tuberculosis surveillance data from the World Health Organization (WHO).

The platform provides:

- Interactive dashboards  
- Statistical analysis  
- Export capabilities  
- Real-time data refresh  

Designed for TB researchers and public health officials.

---

# 📚 Table of Contents

1. [Overview](#overview)  
2. [Mathematical Framework](#mathematical-framework)  
3. [Installation](#installation)  
4. [Usage Guide](#usage-guide)  
5. [Statistical Methods](#statistical-methods)  
6. [API Reference](#api-reference)  
7. [Project Structure](#project-structure)  
8. [Configuration](#configuration)  
9. [Troubleshooting](#troubleshooting)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

# 1️⃣ Overview

The TB Data Analysis Platform facilitates tuberculosis surveillance data analysis through interactive visualizations and statistical methods.

It processes WHO TB data to provide insights into:

- Disease patterns  
- Drug resistance trends  
- Regional distributions  

## 🔑 Key Features

- Interactive visualizations (zoom, pan, hover)
- Statistical analysis and correlations
- Full-screen chart mode
- Export charts as PNG
- Export data as CSV
- Generate complete HTML reports
- Real-time WHO data refresh
- Responsive UI design

---

# 2️⃣ Mathematical Framework

## 📌 TB Incidence Rate

$$
\text{Incidence Rate} = \frac{N_{\text{cases}}}{P} \times 100,000
$$

Where:

- \(N_{\text{cases}}\) = Number of new TB cases  
- \(P\) = Population  

---

## 📌 Drug Resistance Ratios

**MDR Ratio**

$$
\text{MDR Ratio} = \frac{N_{\text{MDR}}}{N_{\text{total}}} \times 100\%
$$

**XDR Ratio**

$$
\text{XDR Ratio} = \frac{N_{\text{XDR}}}{N_{\text{total}}} \times 100\%
$$

---

## 📌 Temporal Analysis

**Year-over-Year Growth**

$$
G_y = \left(\frac{V_y - V_{y-1}}{V_{y-1}}\right) \times 100\%
$$

**CAGR**

$$
\text{CAGR} = \left(\frac{V_n}{V_0}\right)^{\frac{1}{n}} - 1
$$

---

## 📌 Statistical Measures

**Mean**

$$
\mu = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

**Standard Deviation**

$$
\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \mu)^2}
$$

**Correlation Coefficient**

$$
r_{xy} =
\frac{\sum (x_i - \bar{x})(y_i - \bar{y})}
{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
$$

---

# 3️⃣ Installation

## ✅ Prerequisites

- Python 3.8+
- pip
- Git (optional)

---

## 🔹 Clone Repository

```bash
git clone https://github.com/yourusername/tb-analysis-platform.git
cd tb-analysis-platform
```

---

## 🔹 Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 🔹 Install Dependencies

```bash
pip install -r req.txt
```

### req.txt

```txt
Flask==2.3.3
Flask-CORS==4.0.0
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
scikit-learn==1.3.0
plotly==5.15.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

---

## 🔹 Create Directories

```bash
mkdir -p data static/css static/js templates/models
```

---

## 🔹 Run Application

```bash
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

# 4️⃣ Usage Guide

## 🔹 Navigation

| Page | Description | URL |
|------|------------|------|
| Home | Overview | `/` |
| Dashboard | Full dashboard | `/dashboard` |
| Visualizations | Individual charts | `/visualizations` |

---

## 🔹 Interactive Features

| Action | Description |
|--------|------------|
| Hover | View data points |
| Zoom | Select area to zoom |
| Pan | Move chart |
| Legend Click | Toggle series |
| Expand | Full-screen mode |
| Download | Save as PNG |

---

# 5️⃣ Statistical Methods

## 📌 Variance

$$
s^2 = \frac{1}{n-1}\sum (x_i - \bar{x})^2
$$

---

## 📌 Interquartile Range (IQR)

$$
\text{IQR} = Q_3 - Q_1
$$

Outliers:

$$
x < Q_1 - 1.5 \times IQR
\quad \text{or} \quad
x > Q_3 + 1.5 \times IQR
$$

---

# 6️⃣ API Reference

## 📌 Endpoints

| Endpoint | Method | Description |
|-----------|--------|------------|
| `/` | GET | Home |
| `/dashboard` | GET | Dashboard |
| `/visualizations` | GET | Charts |
| `/api/visualization/<type>` | GET | Chart data |
| `/api/analysis/<type>` | GET | Analysis |
| `/data/preview` | GET | Preview |
| `/api/refresh-data` | GET | Refresh |
| `/api/export/report` | GET | Export HTML |
| `/api/export/csv` | GET | Export CSV |

---

## 📌 Example API Call

```http
GET /api/visualization/line
```

Response:

```json
{
  "success": true,
  "chart": {
    "data": [...],
    "layout": {...}
  }
}
```

---

# 7️⃣ Project Structure

```
tb-analysis-platform/
│
├── app.py
├── config.py
├── req.txt
├── README.md
│
├── models/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── analysis.py
│   └── visualizations.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── visualizations/
│
├── static/
│   ├── css/
│   └── js/
│
└── data/
    └── tb_data_cache.csv
```

---

# 8️⃣ Configuration

## 📌 .env

```env
SECRET_KEY=your-super-secret-key
FLASK_DEBUG=True
PORT=5000
HOST=0.0.0.0
DATA_URL=https://your-dataset-url.csv
DATA_CACHE_FILE=data/tb_data_cache.csv
```

---

# 9️⃣ Troubleshooting

## Module Not Found

```bash
pip install -r req.txt
```

## Port Already in Use

### Linux / Mac

```bash
sudo lsof -i:5000
kill -9 <PID>
```

### Windows

```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

# 🔟 Contributing

1. Fork repository  
2. Create branch  
3. Commit changes  
4. Push branch  
5. Create Pull Request  

---

# 📜 License

Boost Software License  

Copyright (c) 2026 TB Data Analysis Platform  

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files.

---

# ⭐ Thank You for Using TB Data Analysis Platform !
