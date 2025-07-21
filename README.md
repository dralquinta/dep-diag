# Dependency Diagram Analysis Tool

A comprehensive network dependency analysis toolkit that visualizes device connections and infers applications based on network traffic patterns. This project provides interactive network diagrams and detailed application analysis for enterprise infrastructure monitoring.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Data Format](#data-format)
- [Notebooks](#notebooks)
- [Visualization](#visualization)
- [Application Inference](#application-inference)
- [Output Analysis](#output-analysis)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

This project analyzes network dependency data to create interactive visualizations and intelligent application inference. It processes connection data between devices in an enterprise network and provides:

- **Interactive Network Diagrams**: Using Jaal for dynamic network visualization
- **Application Inference**: Smart detection of applications based on ports and device names
- **Connection Analysis**: Detailed statistics on network traffic patterns
- **Device Mapping**: Comprehensive mapping of device relationships

## ✨ Features

### Network Visualization
- Interactive network graphs with hover tooltips
- Configurable physics simulation (can be disabled for static views)
- Node sizing based on connection weights
- Edge thickness representing connection strength
- Responsive web-based interface

### Application Analysis
- **Port-based Application Detection**: Maps common ports to known applications
- **Device Name Analysis**: Infers applications from device naming conventions
- **Enhanced Inference Logic**: Combines multiple detection methods for accuracy
- **Confidence Scoring**: Shows inference method used for transparency

### Data Processing
- CSV data ingestion with validation
- Data cleaning and normalization
- Connection aggregation and deduplication
- Statistical analysis and reporting

## 🛠 Prerequisites

### System Requirements
- Python 3.7+
- Jupyter Notebook/Lab
- Modern web browser (for Jaal visualizations)
- Minimum 4GB RAM (recommended 8GB+ for large datasets)

### Python Dependencies
```
pandas>=1.3.0
jaal>=0.1.9
jupyter>=1.0.0
matplotlib>=3.3.0
plotly>=5.0.0
```

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dep-diag
   ```

2. **Install dependencies**:
   ```bash
   chmod +x init.sh
   ./init.sh
   ```

3. **Launch Jupyter**:
   ```bash
   jupyter notebook
   # or
   jupyter lab
   ```

## 🚀 Usage

### Quick Start

1. **Prepare your data**: Ensure your CSV file contains the required columns (see [Data Format](#data-format))
   - Place your data file as `dump.csv` in the project root
   - Data source: Migration Commander (MC) or Stratozone exports

2. **Run dependency analysis**:
   - Open `dependency.ipynb` in Jupyter
   - Run all cells sequentially to generate interactive network diagram

3. **Run application analysis**:
   - Open `potential_app.ipynb` in Jupyter
   - Execute all cells to see application inference results

### Step-by-Step Workflow

#### 1. Data Loading and Validation
```python
# Load and inspect your data
sz_file_csv = pd.read_csv("./dump.csv", usecols=[
    'initiatingDeviceName', 'receivingDeviceName', 'connectionCount'
])
```

#### 2. Network Visualization
```python
# Create interactive network diagram
from jaal import Jaal
jaal_app = Jaal(edges_df, nodes_df)
jaal_app.plot(vis_opts=visualization_options)
```

#### 3. Application Analysis
```python
# Infer applications from ports and device names
df['inferredReceivingApp'] = df.apply(infer_app_by_device_port, axis=1)
```

## 📊 Data Format

### Required CSV Columns

Your input CSV file must contain these columns:

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `initiatingDeviceName` | String | Source device name | `WEB-SERVER-01` |
| `receivingDeviceName` | String | Target device name | `DB-SERVER-02` |
| `connectionCount` | Integer | Number of connections | `1524` |

### Optional Columns

For enhanced analysis, you may include:

| Column Name | Type | Description |
|-------------|------|-------------|
| `initiatingPort` | Integer | Source port number |
| `receivingPort` | Integer | Target port number |
| `protocol` | String | Network protocol |
| `timestamp` | DateTime | Connection timestamp |

### Sample Data Format
```csv
initiatingDeviceName,receivingDeviceName,connectionCount,receivingPort
WEB-SERVER-01,DB-MYSQL-01,1524,3306
APP-SERVER-02,WEB-SERVER-01,892,80
LOAD-BALANCER,WEB-SERVER-01,2341,443
```

## 📓 Notebooks

### 1. dependency.ipynb - Network Visualization

**Purpose**: Creates interactive network dependency diagrams

**Key Features**:
- Data loading and validation
- Network graph construction
- Interactive Jaal visualization
- Connection statistics

**Cells Overview**:
1. **Import Libraries**: Load required packages (pandas, jaal)
2. **Data Loading**: Read CSV and validate structure
3. **Data Inspection**: Display data summary and statistics
4. **Edge Processing**: Transform data for network analysis
5. **Node Creation**: Build node attributes and weights
6. **Visualization**: Generate interactive Jaal diagram

### 2. potential_app.ipynb - Application Analysis

**Purpose**: Infers applications based on network patterns

**Key Features**:
- Port-to-application mapping
- Device name analysis
- Enhanced inference algorithms
- Comparison reporting

**Analysis Methods**:
- **Port-Based**: Uses common port mappings
- **Device Name Hints**: Analyzes device naming patterns
- **Combined Analysis**: Merges multiple inference methods
- **Pattern Matching**: Regex-based fallback detection

## 🎨 Visualization

### Jaal Network Diagrams

The interactive network visualization provides:

#### Visual Elements
- **Nodes**: Represent devices (size = connection weight)
- **Edges**: Represent connections (thickness = connection count)
- **Colors**: Group-based coloring (customizable)
- **Labels**: Device names with hover details

#### Interaction Features
- **Zoom/Pan**: Navigate large networks
- **Hover Tooltips**: Show connection details
- **Node Selection**: Highlight connected devices
- **Search**: Find specific devices

#### Configuration Options
```python
vis_opts = {
    'height': '600px',
    'width': '100%',
    'physics': {'enabled': False},  # Static layout
    'interaction': {'hover': True},
    'nodes': {
        'size': {'field': 'weight', 'scale': 'linear'}
    },
    'edges': {
        'width': {'field': 'weight', 'scale': 'linear'}
    }
}
```

### Accessing the Visualization
- Diagrams are served on `http://127.0.0.1:8050/`
- Embedded in Jupyter notebook as iframe
- Fully interactive web interface

## 🧠 Application Inference

### Port Mapping Database

Comprehensive mapping of common ports to applications:

```python
common_ports = {
    80: 'HTTP',           # Web servers
    443: 'HTTPS',         # Secure web
    22: 'SSH',            # Secure shell
    3306: 'MySQL',        # MySQL database
    1433: 'MSSQL',        # SQL Server
    5432: 'PostgreSQL',   # PostgreSQL
    27017: 'MongoDB',     # MongoDB
    6379: 'Redis',        # Redis cache
    # ... and many more
}
```

### Device Name Keywords

Smart detection based on device naming conventions:

```python
app_keywords = {
    'web': ['HTTP', 'HTTPS'],
    'mysql': ['MySQL'],
    'postgres': ['PostgreSQL'],
    'oracle': ['Oracle Database'],
    'mongo': ['MongoDB'],
    'redis': ['Redis'],
    # ... additional patterns
}
```

### Inference Logic Hierarchy

1. **Device+Port Match** (Highest Confidence)
   - Device name suggests application AND port confirms it
   - Example: `MYSQL-SERVER-01:3306` → `MySQL (Device+Port Match)`

2. **Device Name Hint** (Medium Confidence)
   - Device name suggests application, port unknown
   - Example: `WEB-SERVER-01:8080` → `HTTP (Device Name Hint)`

3. **Port Based** (Standard Confidence)
   - Standard port mapping, no device hint
   - Example: `SERVER-01:443` → `HTTPS (Port Based)`

4. **Pattern Matching** (Low Confidence)
   - Regex-based fallback for unknown combinations
   - Example: `DB-SERVER-01:9999` → `Database Service`

## 📈 Output Analysis

### Network Statistics

The analysis provides comprehensive metrics:

#### Connection Summary
- Total unique device pairs
- Connection count distribution
- Top connected devices
- Isolated devices

#### Application Distribution
- Applications by connection volume
- Port usage statistics
- Inference method effectiveness
- Unknown application percentage

### Sample Output

```
=== Network Analysis Summary ===
Total Devices: 273
Total Connections: 19,629
Unique Device Pairs: 3,305

=== Top Applications by Connections ===
1. HTTPS (Port Based): 8,234 connections
2. MySQL (Device+Port Match): 3,456 connections
3. HTTP (Port Based): 2,891 connections
4. SSH (Port Based): 1,234 connections

=== Inference Method Distribution ===
Port Based: 45.2%
Device+Port Match: 28.7%
Device Name Hint: 15.3%
Unknown Application: 10.8%
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Jaal Diagram Not Displaying
**Symptoms**: Empty iframe or no visualization
**Solutions**:
```python
# Check data format
print("Edges columns:", df_edges.columns.tolist())
print("Nodes columns:", df_nodes.columns.tolist())

# Verify data types
df_edges['from'] = df_edges['from'].astype(str)
df_edges['to'] = df_edges['to'].astype(str)

# Clean data
df_clean = df.dropna()
```

#### 2. Memory Issues with Large Datasets
**Symptoms**: Kernel crashes or slow performance
**Solutions**:
```python
# Sample large datasets
df_sample = df.sample(n=10000) if len(df) > 10000 else df

# Filter low-volume connections
df_filtered = df[df['connectionCount'] >= 5]
```

#### 3. Application Inference Accuracy
**Symptoms**: Many "Unknown Application" results
**Solutions**:
```python
# Extend port mappings
common_ports.update({
    8081: 'HTTP-alt',
    9200: 'Elasticsearch',
    5672: 'RabbitMQ'
})
```

### Performance Optimization

#### For Large Networks (>1000 nodes)
1. **Disable Physics**: Set `physics: {enabled: false}`
2. **Filter Data**: Remove low-volume connections
3. **Increase Memory**: Adjust Jupyter memory limits
4. **Use Sampling**: Analyze representative subset

### Data Quality Issues

#### Missing Data
```python
# Check for missing values
print(df.isnull().sum())

# Handle missing device names
df = df.dropna(subset=['initiatingDeviceName', 'receivingDeviceName'])
```

#### Duplicate Connections
```python
# Remove duplicates
df_clean = df.groupby(['initiatingDeviceName', 'receivingDeviceName']).agg({
    'connectionCount': 'sum'
}).reset_index()
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Update documentation as needed
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Add docstrings for all functions
- Include unit tests for new features
- Update README for significant changes

## 📄 License

This project is licensed under the MIT License.

---

## 🆘 Support

For questions, issues, or contributions:

- **Issues**: Use GitHub Issues for bug reports
- **Documentation**: Check this README and inline comments
- **Examples**: See the included notebook files

---

**Last Updated**: July 2025  
**Version**: 1.0.0  
**Data Sources**: Migration Commander (MC), Stratozone