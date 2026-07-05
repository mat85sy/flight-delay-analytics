from sqlalchemy import create_engine, text

# Define the database URL
DATABASE_URL = "sqlite:///data/flights.sqlite3"

# Create the engine
engine = create_engine(DATABASE_URL)


def execute_query(query, params):
    """
    Execute an SQL query with the params provided in a dictionary,
    and returns a list of records (dictionary-like objects).
    If an exception was raised, print the error, and return an empty list.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.fetchall()
    except Exception as e:
        print("Query error:", e)
        return []


def get_flight_by_id(flight_id):
    """
    Searches for flight details using flight ID.
    If the flight was found, returns a list with a single record.
    """
    query = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.ID = :id"
    params = {'id': flight_id}
    return execute_query(query, params)


def get_flights_by_date(day, month, year):
    """
    Searches for flights by date.
    Returns a list of flights for the specified date.
    """
    query = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.day = :day AND flights.month = :month AND flights.year = :year"
    params = {'day': day, 'month': month, 'year': year}
    return execute_query(query, params)


def get_delayed_flights_by_airline(airline):
    """
    Searches for delayed flights by airline (20 minutes or more).
    Returns a list of delayed flights for the specified airline.
    """
    query = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE airlines.airline = :airline AND flights.DEPARTURE_DELAY >= 20"
    params = {'airline': airline}
    return execute_query(query, params)


def get_delayed_flights_by_airport(airport):
    """
    Searches for delayed flights from a specific airport (20 minutes or more).
    Returns a list of delayed flights departing from the specified airport.
    """
    query = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.origin_airport = :airport AND flights.DEPARTURE_DELAY >= 20"
    params = {'airport': airport}
    return execute_query(query, params)



def get_flights_by_airline(airline=None):
    """
    Get all flights for a specific airline or all airlines if no airline is specified.
    """
    if airline:
        query = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE airlines.airline = :airline"
        params = {'airline': airline}
    else:
        query = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id"
        params = {}
    
    return execute_query(query, params)