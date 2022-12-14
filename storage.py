from db import db

def get_list():
    sql = """SELECT item_name, information, category_name, in_storage
             FROM inventory inv 
             LEFT JOIN item_names n ON inv.item_type = n.name_id
             LEFT JOIN item_categories c ON inv.category = c.category_id 
             ORDER BY item_name;"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_loans(user_id):
    sql = """SELECT loan_id, item_name, information
             FROM loans l
             LEFT JOIN inventory inv ON l.object_id = inv.item_id 
             LEFT JOIN item_names i ON inv.item_type = i.name_id 
             WHERE user_id=:user_id;"""
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_all_loans():
    sql = """SELECT loan_id, username, item_name, information
             FROM loans l 
             LEFT JOIN inventory inv ON l.object_id = inv.item_id 
             LEFT JOIN item_names i ON inv.item_type = i.name_id 
             LEFT JOIN users u ON l.user_id = u.id 
             ORDER BY username;"""
    result = db.session.execute(sql)
    loans = result.fetchall()
    return loans

def get_available_items():
    sql = """SELECT item_id, item_name, information
             FROM inventory inv 
             LEFT JOIN item_names n ON inv.item_type = n.name_id 
             LEFT JOIN item_categories c ON inv.category = c.category_id 
             WHERE in_storage 
             ORDER BY item_name;"""
    result = db.session.execute(sql)
    return result.fetchall()

def new_loan(user_id, object_id):
    sql1 = "INSERT INTO loans (user_id, object_id) VALUES (:user_id, :object_id);"
    sql2 = "UPDATE inventory SET in_storage = FALSE WHERE item_id=:item_id;"
    db.session.execute(sql1, {"user_id":user_id, "object_id":object_id})
    db.session.execute(sql2, {"item_id":object_id})
    db.session.commit()

def item_return(loan_id):
    sql1 = "SELECT object_id FROM loans WHERE loan_id=:loan_id;"
    result = db.session.execute(sql1, {"loan_id":loan_id})
    object_id = result.fetchone()
    sql2 = "UPDATE inventory SET in_storage = TRUE WHERE item_id=:object_id;"
    db.session.execute(sql2, {"object_id":object_id[0]})
    sql3 = "DELETE FROM loans WHERE loan_id=:loan_id;"
    db.session.execute(sql3, {"loan_id":loan_id})
    db.session.commit()

def return_all():
    sql1 = "SELECT loan_id, object_id FROM loans;"
    loans = db.session.execute(sql1).fetchall()
    sql2 = "UPDATE inventory SET in_storage = TRUE WHERE item_id=:object_id;"
    sql3 = "DELETE FROM loans WHERE loan_id=:loan_id;"
    for loan in loans:
        db.session.execute(sql2, {"object_id":loan[1]})
        db.session.execute(sql3, {"loan_id":loan[0]})
    db.session.commit()
