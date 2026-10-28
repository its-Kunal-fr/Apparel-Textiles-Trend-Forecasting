# Apparel & Textiles: Qualitative Market Context

This note complements the quantitative retail-sales proxy in this repository. It separates broad industry themes from measured findings in the downloaded time series.

## Themes to investigate

### Demand and affordability
Apparel demand can be sensitive to household purchasing power, discounting, and consumer confidence. Nominal sales may rise because prices rise even if the number of garments sold does not. Compare nominal sales with an appropriate price index and unit-volume data before concluding that demand has strengthened.

### Channel mix
Online retail, marketplaces, physical stores, and direct-to-consumer channels can change at different rates. The selected FRED series represents clothing and clothing-accessory store sales, not every channel through which clothing is sold. Channel substitution may therefore make this proxy diverge from total apparel spending.

### Inventory and markdown risk
Forecasts can support inventory planning, but a sales forecast alone does not determine the right purchase quantity. Lead times, opening inventory, sell-through, returns, markdown exposure, supplier minimums, and replenishment flexibility also matter. Scenario planning is safer than treating one point forecast as a target.

### Sourcing and input-cost volatility
Fibre prices, energy, freight, labour, exchange rates, tariffs, and supplier concentration can affect margins and sourcing choices. Retail sales data alone cannot identify these causes. Add input-cost and trade data before making causal claims about margin changes or production shifts.

### Sustainability and material choices
Material traceability, recycled fibres, durability, waste reduction, and supplier transparency are relevant strategic topics, but consumer interest does not automatically imply a measurable sales premium in this dataset. Test demand or willingness-to-pay claims with specific evidence.

## Credible starting sources
1. FRED — Retail Sales: Clothing and Clothing Accessory Stores: https://fred.stlouisfed.org/series/MRTSSM448USS
2. U.S. Census Bureau — Monthly Retail Trade Survey: https://www.census.gov/retail/index.html
3. McKinsey — State of Fashion reports: https://www.mckinsey.com/industries/retail/our-insights/state-of-fashion
4. Textile Exchange — Materials Market Report and resources: https://textileexchange.org/knowledge-center/reports/
5. World Bank — Commodity Markets: https://www.worldbank.org/en/research/commodity-markets

Check each source's publication year, definitions, and methodology before quoting figures. Industry reports may contain forecasts or survey findings rather than measured outcomes.

## Combining qualitative and quantitative evidence
- Quantitative finding: describe only what the script calculates from the downloaded series, including the exact period and units.
- Qualitative context: use sources above to propose plausible mechanisms or strategic considerations.
- Do not claim causality: a coincident movement in retail sales and cotton prices does not establish that cotton prices caused the sales movement.
- State uncertainty: forecasts depend on the selected series, history window, model, and structural conditions.
- Translate to decisions carefully: recommend inventory buffers, flexible replenishment, and scenario checks as options to evaluate, not guaranteed outcomes from a single model.
