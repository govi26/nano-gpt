# The path to the input text file containing the URLs
input_file_path = "./pdf_links.txt"  # Replace with your input file path
# The path to the output text file that will contain the filtered URLs
output_file_path = "./filtered_pdf_links.txt"  # Replace with your output file path

# The base URL to filter by
specific_base_url_to_filter = "https://nccn.org/professionals/physician_gls/"

# Filter the URLs and write to the new output file
with open(input_file_path, "r") as input_file, open(
    output_file_path, "w"
) as output_file:
    for line in input_file:
        clean_line = line.strip()
        if clean_line.startswith(specific_base_url_to_filter):
            output_file.write(clean_line + "\n")

# The code also checks the first few lines of the output to verify the result
