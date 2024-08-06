import pysam

def extract_chromosome(input_vcf, output_vcf, chromosome):
    try:
        # Open the input VCF file
        vcf_in = pysam.VariantFile(input_vcf, 'r')
        
        # Prepare the output VCF file with the same header as input
        vcf_out = pysam.VariantFile(output_vcf, 'w', header=vcf_in.header)
        
        # Fetch and write records from the specified chromosome
        for record in vcf_in.fetch(chromosome):
            vcf_out.write(record)
        
        print(f"Chromosome {chromosome} has been extracted to {output_vcf}")
    
    except FileNotFoundError:
        print(f"Error: The file {input_vcf} does not exist.")
    
    except ValueError as e:
        print(f"Error: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    finally:
        # Ensure files are closed even if an error occurs
        if 'vcf_in' in locals() and not vcf_in.closed:
            vcf_in.close()
        if 'vcf_out' in locals() and not vcf_out.closed:
            vcf_out.close()

