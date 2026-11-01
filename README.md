-- High risk customers jinka contract month-to-month hai
SELECT TOP 20 p.customer_id, p.churn_probability, b.contract, b.monthly_charges
FROM dbo.churn_predictions p
JOIN dbo.billing b ON b.customer_id = p.customer_id
WHERE p.risk_level = 'High'
ORDER BY p.churn_probability DESC;



