"""
CREATIVITY ADDITIONS:
1. Added functionality to analyze a specific country's data (min, max, avg life expectancy)
2. Added ability to find the largest year-to-year drop for a selected country
3. Added data validation and error handling for user inputs
4. Added summary statistics showing the range of years and number of countries in dataset
"""

def parse_float (value):
    """Safely parse a float value, handling empty strings"""
    try:
        return float(value) if value.strip() else None
    except ValueError:
        return None

def main():
    # Initialize variables for overall min and max
    overall_max_life = -1
    overall_max_country = ""
    overall_max_year = 0
    overall_min_life = float('inf')
    overall_min_country = ""
    overall_min_year = 0
    
    # Store all data for additional analysis
    all_data = []
    countries = set()
    years = set()
    
    try:
        with open('life-expectancy.csv', 'r') as file:
            # Skip header line
            header = file.readline().strip().split(',')
            
            # Process each line
            for line_num, line in enumerate(file, start=2):
                # Clean and split the line
                parts = line.strip().split(',')
                
                if len(parts) >= 3:
                    country = parts[0].strip()
                    code = parts[1].strip()
                    year_str = parts[2].strip()
                    
                    # Handle life expectancy (might be in column 3 or 4 depending on format)
                    life_exp_str = parts[3].strip() if len(parts) > 3 else parts[2].strip()
                    
                    # Parse year and life expectancy
                    try:
                        year = int(year_str)
                        life_exp = parse_float(life_exp_str)
                        
                        if life_exp is not None:
                            # Add to sets for summary
                            countries.add(country)
                            years.add(year)
                            
                            # Store for additional analysis
                            all_data.append({
                                'country': country,
                                'year': year,
                                'life_exp': life_exp
                            })
                            
                            # Check for overall max
                            if life_exp > overall_max_life:
                                overall_max_life = life_exp
                                overall_max_country = country
                                overall_max_year = year
                            
                            # Check for overall min
                            if life_exp < overall_min_life:
                                overall_min_life = life_exp
                                overall_min_country = country
                                overall_min_year = year
                    
                    except ValueError:
                        # Skip lines with invalid data
                        continue
        
        # Display dataset summary
        print("\n" + "="*60)
        print("LIFE EXPECTANCY DATA ANALYSIS")
        print("="*60)
        print(f"Dataset Summary:")
        print(f"- Years covered: {min(years)} to {max(years)}")
        print(f"- Number of countries: {len(countries)}")
        print(f"- Total records: {len(all_data)}")
        
        # Display overall min and max
        print(f"\nThe overall max life expectancy is: {overall_max_life} from {overall_max_country} in {overall_max_year}")
        print(f"The overall min life expectancy is: {overall_min_life} from {overall_min_country} in {overall_min_year}")
        
        # Year analysis
        print("\n" + "-"*60)
        while True:
            try:
                year_input = input("\nEnter the year of interest (or 'quit' to exit): ")
                
                if year_input.lower() == 'quit':
                    break
                    
                year = int(year_input)
                
                if year < min(years) or year > max(years):
                    print(f"Please enter a year between {min(years)} and {max(years)}")
                    continue
                
                # Filter data for the selected year
                year_data = [d for d in all_data if d['year'] == year]
                
                if year_data:
                    # Calculate average
                    avg_life = sum(d['life_exp'] for d in year_data) / len(year_data)
                    
                    # Find min and max for the year
                    max_for_year = max(year_data, key=lambda x: x['life_exp'])
                    min_for_year = min(year_data, key=lambda x: x['life_exp'])
                    
                    print(f"\nFor the year {year}:")
                    print(f"The average life expectancy across all countries was {avg_life:.3f}")
                    print(f"The max life expectancy was in {max_for_year['country']} with {max_for_year['life_exp']}")
                    print(f"The min life expectancy was in {min_for_year['country']} with {min_for_year['life_exp']}")
                    
                    # CREATIVITY: Offer additional analysis options
                    print("\n" + "-"*30)
                    print("Additional Analysis Options:")
                    print("1. Analyze a specific country")
                    print("2. Find largest year-to-year drop for a country")
                    print("3. Return to year selection")
                    
                    choice = input("\nEnter your choice (1-3): ").strip()
                    
                    if choice == '1':
                        # Country analysis
                        country = input("Enter country name: ").strip()
                        country_data = [d for d in all_data if d['country'].lower() == country.lower()]
                        
                        if country_data:
                            country_avg = sum(d['life_exp'] for d in country_data) / len(country_data)
                            country_min = min(country_data, key=lambda x: x['life_exp'])
                            country_max = max(country_data, key=lambda x: x['life_exp'])
                            
                            print(f"\nStatistics for {country_data[0]['country']}:")
                            print(f"Years available: {min(d['year'] for d in country_data)} to {max(d['year'] for d in country_data)}")
                            print(f"Average life expectancy: {country_avg:.3f}")
                            print(f"Minimum: {country_min['life_exp']} in {country_min['year']}")
                            print(f"Maximum: {country_max['life_exp']} in {country_max['year']}")
                        else:
                            print(f"No data found for country: {country}")
                    
                    elif choice == '2':
                        # Find largest year-to-year drop
                        country = input("Enter country name to analyze drops: ").strip()
                        country_data = [d for d in all_data if d['country'].lower() == country.lower()]
                        country_data.sort(key=lambda x: x['year'])
                        
                        if len(country_data) > 1:
                            max_drop = 0
                            max_drop_year = None
                            max_drop_from = None
                            
                            for i in range(1, len(country_data)):
                                drop = country_data[i-1]['life_exp'] - country_data[i]['life_exp']
                                if drop > max_drop:
                                    max_drop = drop
                                    max_drop_year = country_data[i]['year']
                                    max_drop_from = country_data[i-1]['year']
                            
                            if max_drop > 0:
                                print(f"\nLargest drop for {country_data[0]['country']}:")
                                print(f"From {max_drop_from} to {max_drop_year}: {max_drop:.3f} years decrease")
                            else:
                                print("No significant drops found (life expectancy consistently increased)")
                        else:
                            print("Insufficient data for year-to-year analysis")
                
                else:
                    print(f"No data available for year {year}")
                    
            except ValueError:
                print("Please enter a valid year number")
            except KeyboardInterrupt:
                print("\n\nProgram terminated by user.")
                break
        
        print("\nThank you for using the Life Expectancy Analyzer!")
        
    except FileNotFoundError:
        print("Error: Could not find the file 'life-expectancy.csv'")
        print("Please make sure the file is in the same directory as this program.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()