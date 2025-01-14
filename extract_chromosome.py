import os
import pysam

def extract_chromosome(input_vcf, output_vcf, chromosome):
    # Validate input file
    if not os.path.exists(input_vcf):
        raise FileNotFoundError(f"Input VCF file '{input_vcf}' does not exist.")
    
    try:
        # Open the input VCF file
        with pysam.VariantFile(input_vcf, 'r') as vcf_in:
            # Determine the naming convention in the VCF (e.g., "chr1" or "1")
            vcf_chromosomes = set(vcf_in.header.contigs)
            if chromosome in vcf_chromosomes:
                vcf_chrom = chromosome
            elif chromosome.startswith("chr") and chromosome[3:] in vcf_chromosomes:
                vcf_chrom = chromosome[3:]
            elif not chromosome.startswith("chr") and f"chr{chromosome}" in vcf_chromosomes:
                vcf_chrom = f"chr{chromosome}"
            else:
                raise ValueError(f"Chromosome '{chromosome}' not found in the input VCF.")
            
            # Open the output VCF file for writing
            with pysam.VariantFile(output_vcf, 'w', header=vcf_in.header) as vcf_out:
                variant_count = 0
                for record in vcf_in.fetch(vcf_chrom):
                    vcf_out.write(record)
                    variant_count += 1
        
        print(f"Extracted {variant_count} variants from chromosome '{chromosome}' to '{output_vcf}'.")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
