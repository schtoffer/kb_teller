from cs50 import SQL

db = SQL("sqlite:///kb_teller.db")

def sql(table, column, id):
    result = db.execute(f"SELECT {column} FROM {table} WHERE id = ?", id)

    # Check if there is at least one result
    if result:
        return result[0][column]  
    return None  