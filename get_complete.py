from sqlite3 import connect

# Added ability to filter by course or for sub assignments by parent assignment


def get_completed_assignments(course_id: int = None) -> list:
    con = connect("storage.db")

    query = ["SELECT * FROM assignments WHERE completed = TRUE"]

    if course_id is not None:
        query.append(f"AND course_id = ?")

    # Unpack results in to assignment class
    results = con.execute("".join(query), (course_id,)).fetchall()
    con.close()
    return results


def get_completed_sub_assignments(assignment_id: int = None, course_id: int = None) -> list:
    con = connect("storage.db")

    query = ["SELECT * FROM subassignments WHERE completed = TRUE"]

    if assignment_id is not None:
        query.append(" AND assignment_id = ?")

    if course_id is not None:
        query.append(" AND course_id = ?")

    # Unpack results in to sub_assignment class
    results = con.execute("".join(query), (assignment_id, course_id)).fetchall()
    con.close()
    return results
