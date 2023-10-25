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

date_max = (1,2)

prompt = "What is the <tax_element> for <industry> industry in <region> for <date>?"

query = '''SELECT `<tax_element>`
FROM industry_entity_tax
WHERE report_id IN (
        SELECT id
        FROM report
        WHERE
            reporting_month = ""<date>""
    )
    AND industry_entity_id IN (
        SELECT id
        FROM industry_entity
        WHERE entity_id IN (
                SELECT id
                FROM entity
                WHERE
                    name LIKE ""%<region>%""
            )
            AND `name` LIKE ""%<industry>%""
    )
    AND `name` = ""Total"";'''

def make_question_string(region, industry, tax_element, year, month):
  date_string = month + " " + year
  filled_question = prompt.replace("<region>", region).replace("<industry>", industry).replace("<tax_element>", tax_element).replace("<date>", date_string)
  return filled_question

def make_query_string(region, industry, tax_element, year, month_i):
  date_string = year + "-" + str(month_i+1).rjust(2,"0") + "-01"
  tax_element_string = tax_element.lower()
  filled_query = query.replace("<region>", region).replace("<industry>", industry).replace("<tax_element>", tax_element_string).replace("<date>", date_string)
  return filled_query

def generate():
  print("input,output,text,sqlquery")
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

            line = "\"" + prompt_string + "\",,,\"" + query_string + "\""
            print(line)

generate()