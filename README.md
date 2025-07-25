# Monte Carlo Portfolio Simulation

Full-stack Monte Carlo simulation platform with **Python simulation engine**, **FastAPI backend**, and **React frontend**. Features regime-dependent risk modeling, customizable portfolios, and interactive visualizations. Explore how macroeconomic shifts impact portfolio outcomes through real market data, advanced financial mathematics, and intuitive web interface.

## 🎯 Project Overview

- **Full-stack architecture**: Python simulation engine + FastAPI + React dashboard
- **Default portfolio simulation** with pre-configured 6-asset portfolio across 3 regimes (historical, fiat debasement, geopolitical crisis)
- **Fully customizable portfolios** with interactive web interface - modify tickers, weights, asset count, mean/volatility factors, and correlation adjustments
- **Advanced financial mathematics**: Regime-dependent risk modeling with sophisticated correlation adjustments
- **Professional visualizations**: Interactive charts with Monte Carlo paths, correlation matrices, and risk analysis
- **Real-time portfolio validation** with form feedback and error handling

## 📸 Screenshots & Demo

**Live Demo**: [monte-carlo-regime-portfolio-simulator.vercel.app](https://monte-carlo-regime-portfolio-simulator.vercel.app/default-portfolio)

### Default Portfolio Dashboard

![Portfolio Interface](screenshots/default-portfolio-geopolitical-crisis.png)
_Interactive dashboard with portfolio composition and regime analysis_

### Monte Carlo Simulation Results

![Monte Carlo Paths](screenshots/monte-carlo-fiat-debasement.png)
_1000 simulation paths showing potential portfolio outcomes with confidence intervals_

### Portfolio Builder Interface

![Custom Portfolio Builder](screenshots/custom-portfolio-form.png)
_Interactive form with real-time validation - create any portfolio combination_

### Risk Analysis Dashboard

<details>
<summary>📊 View Additional Analysis Charts</summary>

![Correlation Matrix](screenshots/correlation-matrix-heatmap-fiat-debasement.png)
_Asset correlation heatmap showing regime-dependent relationships_

![PCA Analysis](screenshots/risk-factor-analysis-fiat-debasement.png)
_Principal component analysis identifying dominant risk factors_

</details>

## 🏗️ Architecture & Features

**Three-tier separation:**

- **Simulation Engine + API Layer** (`api/`) - Core Monte Carlo with regime modeling + FastAPI wrapper with CORS configuration
- **Frontend** (`frontend/src/`) - React dashboard with interactive charts

**Technology Stack:**

- **Backend**: Python, FastAPI, NumPy, Pandas, Matplotlib, yfinance
- **Frontend**: React 19, TypeScript, Vite, shadcn/ui, Recharts, TanStack Query, Zustand

## 🎨 Frontend Features

**Interactive Portfolio Dashboard:**

- **Portfolio Composition Chart** - Pie chart visualization of asset weights
- **Regime Factors Radar Chart** - Visual comparison of mean/volatility factors and correlation adjustments
- **Three Generated Visualizations** - Monte Carlo simulation paths, correlation matrix heatmap, PCA risk factor analysis

**Fully Customizable Form:**

- **Dynamic asset management** - Add/remove tickers with real-time validation
- **Custom weightings** - Adjustable portfolio weights with automatic normalization
- **Date range selection** - Historical data period customization
- **Regime parameter tuning** - Individual mean/volatility factors per asset
- **Global correlation adjustment** - Portfolio-wide correlation modification
- **Real-time feedback** - Form validation with error messages and success indicators

## 📊 Backend Simulation Features

**Generated Outputs (each regime produces):**

- **Monte Carlo simulation paths** - Confidence intervals, key trajectories, risk metrics (VaR, CVaR)
- **Correlation matrix heatmap** - Asset correlations with matrix conditioning analysis
- **PCA risk factor analysis** - Principal components, explained variance, factor loadings

**Key Metrics:**

- Complete portfolio performance statistics (median, mean, best/worst case outcomes)
- Professional risk assessment with confidence intervals and stress testing
- Systematic risk factor identification and asset contribution analysis

**Advanced Mathematical Methodology:**

- **Data Foundation**: Historical daily returns from Yahoo Finance API with comprehensive data validation
- **Regime Modeling**: Two-stage covariance adjustment process:
  - _Stage 1_: Scale each covariance element Σ[i,j] by vol_factor[i] × vol_factor[j], preserving correlation structure while adjusting joint risk magnitudes
  - _Stage 2_: Extract correlation matrix, apply regime-specific correlation_move_pct to off-diagonal elements, then reconstruct covariance with numerical clipping to [-1,1]
- **Monte Carlo Engine**: 1000 simulations using multivariate normal sampling over 252 trading days with regime-adjusted parameters
- **Risk Factor Analysis**: PCA identifies key risk factors (eigenvalue > 1.0 threshold) with smart asset selection (top 2 contributors or all above 10% threshold)
- **Risk Metrics**: Professional VaR/CVaR calculations at 95% and 99% confidence levels with percentile-based path analysis
- **Numerical Stability**: Ensures mathematical validity through correlation matrix conditioning and eigenvalue monitoring
- **Assumptions**: Frictionless markets (no transaction costs), perfect daily rebalancing, normally distributed returns

## 🚀 API Endpoints

**Live API Documentation**: [https://monte-carlo-regime-portfolio-simulator-production.up.railway.app/docs](https://monte-carlo-regime-portfolio-simulator-production.up.railway.app/docs)

- **`GET /api/portfolio/default`** - Default 6-asset portfolio composition and date range
- **`POST /api/simulate/{regime}`** - Run Monte Carlo simulation for default portfolio (historical/fiat_debasement/geopolitical_crisis)
- **`POST /api/simulate/custom`** - Run simulation for fully customizable portfolio with custom regime parameters
- **`POST /api/portfolio/validate`** - Validate portfolio tickers, weights, and date ranges
- **`GET /api/regimes`** - Available regime scenarios with descriptions
- **`GET /api/regimes/{regime}/parameters`** - Regime-specific factor adjustments

## 📚 Educational Value

This project bridges fundamental mathematical concepts with real-world financial applications, demonstrating:

**What You'll Learn:**

- **Linear Algebra in Action**: Matrix operations, PCA, and correlation analysis applied to real financial data
- **Statistics & Probability**: Monte Carlo methods, risk calculations, and working with correlated random variables
- **Financial Modeling**: Portfolio theory, regime analysis, and professional risk metrics (VaR/CVaR)
- **Full-Stack Development**: Python backend, React frontend, API design, and data visualization
- **Production Skills**: Error handling, data validation, performance optimization, and deployment
- **Modern Development Practices**: AI-assisted development with Cursor and Claude Code, demonstrating AI literacy and prompt engineering skills

This project shows how foundational math and programming knowledge can be applied to build real financial analysis tools.

## 📊 Default Portfolio Composition

| Asset                            | Ticker  | Weight | Description                     |
| -------------------------------- | ------- | ------ | ------------------------------- |
| Bitcoin                          | BTC-EUR | 60%    | Cryptocurrency hedge            |
| iShares MSCI World Energy Sector | 5MVW.DE | 13%    | Global developed energy markets |
| SPDR S&P 500                     | SPYL.DE | 10.5%  | US large-cap stocks             |
| VanEck S&P Global Mining         | WMIN.DE | 7%     | Global miners                   |
| iShares Core MSCI EM IMI         | IS3N.DE | 6%     | Emerging market stocks          |
| Gold                             | 4GLD.DE | 3.5%   | Precious metals                 |

## 🚀 Installation & Setup

**Prerequisites:** Python 3.8+, Node.js 18+

### Backend Setup

```bash
# Clone repository
git clone <repository-url>
cd monte-carlo

# Install Python dependencies
pip install -r requirements.txt

# Run API server
cd api && uvicorn app:app --reload --port 8000
```

### Frontend Setup

```bash
# In new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev          # Development (port 5173)
npm run build        # Production build
npm run preview      # Preview production build
```

## 📈 Usage

### Full-Stack Web Application

1. **Start API server**: `cd api && uvicorn app:app --reload --port 8000`
2. **Start frontend**: `cd frontend && npm run dev`
3. **Access application**: http://localhost:5173

### Standalone Python Simulation

```bash
# Run all scenarios (generates charts/ folder)
python api/main.py
```
