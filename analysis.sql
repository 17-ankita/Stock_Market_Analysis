-- =============================================================
-- STOCK MARKET ANALYSIS SQL FILE
-- Table name: stock_market
-- =============================================================

-- Q1. Total companies
SELECT 
    COUNT(*) AS total_companies
FROM stock_market;

-- Q2. Total industries
SELECT 
    COUNT(DISTINCT Industry) AS total_industries
FROM stock_market;

-- Q3. Total headquarters / regions
SELECT 
    COUNT(DISTINCT Headquarters) AS total_regions
FROM stock_market;

-- Q4. Overall KPI summary
SELECT
    COUNT(*) AS total_companies,
    ROUND(AVG(Market_Capital), 2) AS avg_market_cap,
    ROUND(AVG(ROCE), 2) AS avg_roce,
    ROUND(AVG(Profit_Percent), 2) AS avg_profit_percent,
    ROUND(AVG(Website_Design_Score), 2) AS avg_website_design_score,
    ROUND(AVG(UX_Score), 2) AS avg_ux_score,
    ROUND(AVG(Performance_Score), 2) AS avg_performance_score
FROM stock_market;

-- Q5. Industry-wise company count
SELECT 
    Industry,
    COUNT(*) AS total_companies
FROM stock_market
GROUP BY Industry
ORDER BY total_companies DESC;

-- Q6. Market capital by industry
SELECT 
    Industry,
    COUNT(*) AS total_companies,
    ROUND(SUM(Market_Capital), 2) AS total_market_cap,
    ROUND(AVG(Market_Capital), 2) AS avg_market_cap
FROM stock_market
GROUP BY Industry
ORDER BY total_market_cap DESC;

-- Q7. Top companies by ROCE
SELECT 
    Company,
    Industry,
    Headquarters,
    Market_Capital,
    ROCE
FROM stock_market
ORDER BY ROCE DESC
LIMIT 10;

-- Q8. Top companies by profit percentage
SELECT 
    Company,
    Industry,
    Headquarters,
    Market_Capital,
    Profit_Percent
FROM stock_market
ORDER BY Profit_Percent DESC
LIMIT 10;

-- Q9. Regional company distribution
SELECT 
    Headquarters,
    COUNT(*) AS total_companies
FROM stock_market
GROUP BY Headquarters
ORDER BY total_companies DESC;

-- Q10. Average market capital by headquarters
SELECT 
    Headquarters,
    COUNT(*) AS total_companies,
    ROUND(AVG(Market_Capital), 2) AS avg_market_cap,
    ROUND(SUM(Market_Capital), 2) AS total_market_cap
FROM stock_market
GROUP BY Headquarters
ORDER BY avg_market_cap DESC;

-- Q11. Website quality by industry
SELECT 
    Industry,
    COUNT(*) AS total_companies,
    ROUND(AVG(Website_Design_Score), 2) AS avg_website_score,
    ROUND(AVG(UX_Score), 2) AS avg_ux_score,
    ROUND(AVG(Performance_Score), 2) AS avg_performance_score
FROM stock_market
GROUP BY Industry
ORDER BY avg_website_score DESC;

-- Q12. Website design type analysis
SELECT 
    Website_Design_Type,
    COUNT(*) AS total_companies,
    ROUND(AVG(Website_Design_Score), 2) AS avg_website_score,
    ROUND(AVG(Performance_Score), 2) AS avg_performance_score,
    SUM(Design_Issues) AS total_design_issues
FROM stock_market
GROUP BY Website_Design_Type
ORDER BY total_design_issues DESC;

-- Q13. Companies with poor website quality
SELECT 
    Company,
    Industry,
    Headquarters,
    Website_Design_Score,
    UX_Score,
    Performance_Score,
    Design_Issues
FROM stock_market
WHERE Website_Design_Score < 70
ORDER BY Website_Design_Score ASC;

-- Q14. UX vs performance relationship
SELECT 
    Website_Design_Type,
    ROUND(AVG(UX_Score), 2) AS avg_ux_score,
    ROUND(AVG(Performance_Score), 2) AS avg_performance_score
FROM stock_market
GROUP BY Website_Design_Type
ORDER BY avg_performance_score DESC;

-- Q15. Companies with high design issues
SELECT 
    Company,
    Industry,
    Headquarters,
    Website_Design_Type,
    Design_Issues,
    Website_Design_Score
FROM stock_market
WHERE Design_Issues >= 5
ORDER BY Design_Issues DESC;

-- Q16. Client potential scorecard
SELECT 
    Company,
    Industry,
    Headquarters,
    Market_Capital,
    ROCE,
    Profit_Percent,
    Website_Design_Score,
    Performance_Score
FROM stock_market
ORDER BY ROCE DESC, Profit_Percent DESC
LIMIT 20;

-- Q17. Industry opportunity score
SELECT 
    Industry,
    COUNT(*) AS total_companies,
    ROUND(AVG(Market_Capital), 2) AS avg_market_cap,
    ROUND(AVG(ROCE), 2) AS avg_roce,
    ROUND(AVG(Profit_Percent), 2) AS avg_profit,
    ROUND(AVG(Website_Design_Score), 2) AS avg_website_score,
    ROUND(AVG(Design_Issues), 2) AS avg_design_issues
FROM stock_market
GROUP BY Industry
ORDER BY total_companies DESC, avg_design_issues DESC;

-- Q18. Region opportunity score
SELECT 
    Headquarters,
    COUNT(*) AS total_companies,
    ROUND(AVG(Market_Capital), 2) AS avg_market_cap,
    ROUND(AVG(ROCE), 2) AS avg_roce,
    ROUND(AVG(Website_Design_Score), 2) AS avg_website_score
FROM stock_market
GROUP BY Headquarters
ORDER BY total_companies DESC, avg_market_cap DESC;

-- Q19. Potential Inmogic target companies
SELECT 
    Company,
    Industry,
    Headquarters,
    Website_Design_Score,
    UX_Score,
    Performance_Score,
    Design_Issues
FROM stock_market
WHERE Website_Design_Score < 70
   OR Performance_Score < 70
   OR Design_Issues >= 5
ORDER BY Website_Design_Score ASC, Design_Issues DESC;

-- Q20. Full business scorecard
SELECT 
    Company,
    Industry,
    Headquarters,
    Market_Capital,
    ROCE,
    Profit_Percent,
    Website_Design_Type,
    Website_Design_Score,
    UX_Score,
    Performance_Score,
    Design_Issues
FROM stock_market
ORDER BY Market_Capital DESC;