dataset: gross receipt taxes of New Mexico 
time period: 2009 - 2023

The project premise is to fine tune an open source LLM like Llama 2 with a specific dataset.
The goal is to train the model with natural language prompts in order to generate sql queries to our database.
We would set a "correct answers returned" success rate we would want to achieve (i.e. > 85%).
Essentially making an assistant for generating queries for the data.

This tool would enable users to quickly understand features of the data like revenue generation, sector performance, and broader economic patterns at both the state and local levels; potentially becoming an invaluable asset for revenue forecasting, policy formation, and economic analytics.

Further work on this project includes predictive analytics for state tax data.

# Example SQL Queries

What counties are included in the tax data?

```sql
SELECT *
FROM entity
WHERE id IN (
        SELECT entity_id
        FROM (
                SELECT *
                FROM
                    entity_category_rel ecr
                    JOIN entity_category ec on ecr.category_id = ec.id
            ) AS categories
        WHERE
            categories.name = "County"
    );
```

---

What was the total retail trade industry tax paid for Albuquerque in April 2018

```sql
SELECT total_tax_paid
FROM industry_entity_tax
WHERE report_id IN (
        SELECT id
        FROM report
        WHERE
            reporting_month = "2018-04-01"
    )
    AND industry_entity_id IN (
        SELECT id
        FROM industry_entity
        WHERE entity_id IN (
                SELECT id
                FROM entity
                WHERE
                    name LIKE "%Albuquerque%"
            )
            AND `name` LIKE "%Retail Trade%"
    )
    AND `name` = "Total";
```

---

What was the maximum construction industry taxable receipts for Bernalillo County in 2016?

```sql
SELECT MAX(taxable_receipts) as max_taxable_receipts
FROM industry_entity_tax
WHERE report_id IN (
        SELECT id
        FROM report
        WHERE
            reporting_month BETWEEN "2016-01-01" AND "2016-12-31"
    )
    AND industry_entity_id IN (
        SELECT id
        FROM industry_entity
        WHERE entity_id IN (
                SELECT id
                FROM entity
                WHERE
                    name LIKE "%Bernalillo County%"
            )
            AND `name` LIKE "%Construction%"
    )
    AND `name` = "Total";
```
