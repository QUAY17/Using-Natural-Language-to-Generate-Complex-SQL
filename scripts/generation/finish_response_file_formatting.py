import pandas as pd
import re

infile = "scripts/gen_queries_out.csv"
outfile = "trainData.csv"

df = pd.read_csv(infile)

def generate_output_and_text(df):
    # Regular expression pattern to match the components
    pattern = r"What is the (.+?) for (.+?) industry in (.+?) for (.+?)\?"

    for index, row in df.iterrows():
        match = re.match(pattern, row['input'])
        
        if match:
            tax_element = match.group(1)
            industry = match.group(2)
            region = match.group(3)
            date = match.group(4)

            # Construct output string
            output = f"The {tax_element.lower()} for {industry} industry in {region} for {date} was {row['answer']}."
            
            # Construct text string
            text = f"###Human:\n{row['input']}\n\n### Assistant:\n{output}"
            
            # Set the values in the dataframe
            df.at[index, 'output'] = output
            df.at[index, 'text'] = text

    return df


df = generate_output_and_text(df)

df.to_csv(outfile, index=False)

