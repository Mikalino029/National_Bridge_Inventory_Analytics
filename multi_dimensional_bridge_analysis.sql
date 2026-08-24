SELECT 
    Bridge_ID,
    State_Code,
    Material_Type,
    Infrastructure_Generation,
    Average_Condition_Score,
    -- Window Function: Calculate network average score for this specific material type
    ROUND(AVG(Average_Condition_Score) OVER(PARTITION BY Material_Type), 2) AS Material_Network_Avg,
    -- Window Function: Calculate network average score for this specific age generation
    ROUND(AVG(Average_Condition_Score) OVER(PARTITION BY Infrastructure_Generation), 2) AS Generation_Network_Avg
FROM bridge_inspections
ORDER BY Average_Condition_Score ASC;