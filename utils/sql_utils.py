from cs50 import SQL

db = SQL("sqlite:///db.db")

def sql(table, column, id):
    result = db.execute(f"SELECT {column} FROM {table} WHERE id = ?", id)

    # Check if there is at least one result
    if result:
        return result[0][column]  
    return None 

def insert_or_update_report(business_id, date, metric, number):
    """Insert a new report or update the existing one if the combination exists."""
    
    # Attempt to update the existing report
    rows_updated = db.execute('''
        UPDATE reports
        SET number = ?
        WHERE business_id = ? AND date = ? AND metric = ?
    ''', number, business_id, date, metric)
    
    # If no rows were updated, insert a new report
    if rows_updated == 0:
        db.execute('''
            INSERT INTO reports (business_id, date, metric, number)
            VALUES (?, ?, ?, ?)
        ''', business_id, date, metric, number)