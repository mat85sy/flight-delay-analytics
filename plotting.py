import matplotlib.pyplot as plt
import pandas as pd
from flights_data import execute_query

def generate_delay_percentage_report():
    """
    Generate a bar chart showing the percentage of delayed flights by airline.
    """
    print("Generating delay percentage report...")
    
    # Get all airlines
    query = "SELECT DISTINCT airline FROM airlines"
    airline_results = execute_query(query, {})
    
    # Calculate delay percentage for each airline
    data = []
    for result in airline_results:
        airline_name = result._mapping['AIRLINE']
        
        # Get total flights for this airline
        query_total = """
        SELECT COUNT(*) as total 
        FROM flights f 
        JOIN airlines a ON f.airline = a.id 
        WHERE a.airline = :airline
        """
        total_result = execute_query(query_total, {'airline': airline_name})
        total_flights = total_result[0]._mapping['total'] if total_result else 0
        
        # Get delayed flights for this airline (20+ minutes)
        query_delayed = """
        SELECT COUNT(*) as delayed 
        FROM flights f 
        JOIN airlines a ON f.airline = a.id 
        WHERE a.airline = :airline AND f.DEPARTURE_DELAY >= 20
        """
        delayed_result = execute_query(query_delayed, {'airline': airline_name})
        delayed_flights = delayed_result[0]._mapping['delayed'] if delayed_result else 0
        
        # Calculate percentage
        if total_flights > 0:
            percentage = (delayed_flights / total_flights) * 100
        else:
            percentage = 0
            
        data.append({
            'Airline': airline_name,
            'Percentage': percentage
        })
    
    # Create DataFrame and sort
    df = pd.DataFrame(data)
    df = df.sort_values('Percentage', ascending=False)
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    bars = plt.bar(df['Airline'], df['Percentage'], color='steelblue')
    
    # Add labels and title
    plt.xlabel('Airline')
    plt.ylabel('Percentage of Delayed Flights')
    plt.title('Percentage of Delayed Flights by Airline')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('delay_percentage_by_airline.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Report generated successfully!")