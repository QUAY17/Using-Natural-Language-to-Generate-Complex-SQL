import mysql.connector
import csv

regions = [
  "Santa Fe County",
  "Bernalillo County",
  "Eddy County",
  "Chaves County",
  "Curry County",
  "Lea County",
  "Dona Ana County",
  "Grant County",
  "Colfax County",
  "Quay County",
  "Roosevelt County",
  "San Miguel Co",
  "McKinley County",
  "Valencia County",
  "Otero County",
  "San Juan County",
  "Rio Arriba County",
  "Union County",
  "Luna County",
  "Taos County",
  "Sierra County",
  "Torrance County",
  "Hidalgo County",
  "Guadalupe County",
  "Socorro County",
  "Lincoln County",
  "De Baca County",
  "Catron County",
  "Sandoval County",
  "Mora County",
  "Harding County",
  "Cibola County"
]

industries = [
  "Agriculture, Forestry, Fishing and Hunting",
  "Mining, Quarrying, and Oil and Gas Extraction",
  "Utilities",
  "Construction",
  "Manufacturing",
  "Wholesale trade",
  "Retail Trade",
  "Transportation and Warehousing",
  "Information",
  "Finance and Insurance",
  "Real Estate and Rental and Leasing",
  "Professional, Scientific, and Technical Services",
  "Management of Companies and Enterprises",
  "Administrative and Support and Waste Management and Remediation Services",
  "Educational Services",
  "Health Care and Social Assistance",
  "Arts, Entertainment, and Recreation",
  "Accommodation and Food Services",
  "Other Services (except Public Administration)",
  "Public Administration",
  "Unclassified Establishments",
  "All Industries"
]

industry_tax_elements = [
  "Returns",
  "Total Receipts",
  "Taxable Receipts",
  "Matched Taxable Receipts",
  "Total Tax Due",
  "Total Tax Paid",
  "Recipient Paid",
  "Recipient Due",
  "Adjustment"
]

db_column_mapping = {
    "Returns": "returns",
    "Total Receipts": "total_receipts",
    "Taxable Receipts": "taxable_receipts",
    "Matched Taxable Receipts": "matched_taxable_receipts",
    "Total Tax Due": "total_tax_due",
    "Total Tax Paid": "total_tax_paid",
    "Recipient Paid": "recipient_paid",
    "Recipient Due": "recipient_due",
    "Adjustment": "adjustment"
}

years = [
  "2022",
  "2023"
]

months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
]

date_max = (1,0)

prompt = "What is the <tax_element> for <industry> industry in <region> for <date>?"

query = '''SELECT `<tax_element>`
FROM industry_entity_tax
WHERE report_id IN (
        SELECT id
        FROM report
        WHERE
            reporting_month = '<date>'
    )
    AND industry_entity_id IN (
        SELECT id
        FROM industry_entity
        WHERE entity_id IN (
                SELECT id
                FROM entity
                WHERE
                    name LIKE "%<region>%"
            )
            AND `name` LIKE "%<industry>%"
    )
    AND `name` = "Total";'''

def make_question_string(region, industry, tax_element, year, month):
  date_string = month + " " + year
  filled_question = prompt.replace("<region>", region).replace("<industry>", industry).replace("<tax_element>", tax_element).replace("<date>", date_string)
  return filled_question

def make_query_string(region, industry, tax_element, year, month_i):
    date_string = year + "-" + str(month_i+1).rjust(2,"0") + "-01"
    tax_element_db_column = db_column_mapping[tax_element]
    filled_query = query.replace("<region>", region).replace("<industry>", industry).replace("<tax_element>", tax_element_db_column).replace("<date>", date_string)
    return filled_query

def generate_sql_as_answer():

    with open('SQLQueriesV2.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Writing the headers to the CSV
        csvwriter.writerow(["prompt", "input", "schema", "query", "text"])

        for region in regions:
            for industry in industries:
                for tax_element in industry_tax_elements:
                    for year_i in range(len(years)):
                        for month_i in range(len(months)):
                            if year_i == date_max[0] and month_i > date_max[1]:
                                break

                            year = years[year_i]
                            month = months[month_i]

                            prompt_string = make_question_string(region, industry, tax_element, year, month)
                            query_string = make_query_string(region, industry, tax_element, year, month_i)

                            # The schema is essentially the formatted SQL query with placeholders
                            schema = query.replace("<region>", region).replace("<industry>", industry).replace("<tax_element>", db_column_mapping[tax_element]).replace("<date>", year + "-" + str(month_i+1).rjust(2,"0") + "-01")

                            # The output includes the phrase "Your SQL query: {sql query}"
                            output = f"Execute this SQL query: {query_string}"

                            # The text column reflects the interaction with SQL as the output
                            text_format = f"###Human:\n{prompt_string}\n\n###Assistant:\n{output}"

                            line = [prompt, prompt_string, schema, query_string, text_format]
                            csvwriter.writerow(line)


generate_sql_as_answer()
