import sqlite3


# @todo add logger
def get_skills_description(db_file):
    """
    Connects to ESCO database and retrieves skills label, alternative label, hidden label and description
    :param db_file: database file location
    :return: list with description
    """
    print(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    statement = 'SELECT description FROM skills'
    cursor.execute(statement)
    records = cursor.fetchall()
    skills_desc = []
    for row in records:
        skills_desc.append([row[0]])
    conn.close()

    return skills_desc


def get_skills_preferred_label(db_file):
    """
    Connects to ESCO database and retrieves skills preferred labels
    :param db_file: database file location
    :return: list with labels
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    statement = "SELECT  preferredLabel FROM skills;"
    cursor.execute(statement)
    records = cursor.fetchall()
    skills_labels = []
    for row in records:
        labels = "{0}".format(row[0]).splitlines()
        skills_labels.append(labels)
    conn.close()

    return skills_labels


def get_skills_merged_labels(db_file):
    """
    Connects to ESCO database and erges skill's preferredLabel and altLabels
    :param db_file: database file location
    :return: list with merged labels
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        statement = "SELECT preferredLabel || CHAR(10) || altLabels  as labels FROM skills;"
        cursor.execute(statement)
        records = cursor.fetchall()
        skills_labels = []
        for row in records:
            labels = "{0}".format(str(row[0]).strip())
            skills_labels.append(labels)
        conn.close()
        return skills_labels
    except sqlite3.Error as e:
        print(e)
    return None


def get_skills_record(db_file, rowid):
    """
    Connects to ESCO database and retrieves skills records for a given rowid
    :param rowid:
    :param db_file: database file location
    :return: list with description
    """
    rowid = str(rowid + 1)  # we offset 1 to rowid because models in the embedding start from 0, in sqlite start from 1
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    statement = 'SELECT  * FROM skills WHERE rowid = ' + rowid + ';'
    cursor.execute(statement)
    skills = cursor.fetchall()
    conn.close()
    return skills


def get_skills_record_conn(conn, rowid):
    """
    Connects to ESCO database and retrieves skills records for a given rowid
    :param rowid:
    :param conn: database cursorn
    :return: list with description
    """
    rowid = str(rowid + 1)  # we offset 1 to rowid because models in the embedding start from 0, in sqlite start from 1
    cursor = conn.cursor()

    statement = 'SELECT  * FROM skills WHERE rowid = ' + rowid + ';'
    cursor.execute(statement)
    skills = cursor.fetchall()

    return skills


def get_desc_from_skillname(cursor, skill):
    """
    Connects to ESCO database and retrieves description from skill's name, notice only one record maximun is retrieved
    :param cursor: database cursor
    :param skill: skill name
    :return: description string
    """

    statement = 'SELECT description FROM skills WHERE preferredLabel = \"' + skill + '\" COLLATE NOCASE LIMIT 1;'
    cursor.execute(statement)
    record = cursor.fetchone()
    if record is None:
        return -1
    result = ", ".join(record)

    return result


def get_id_from_skillname(cursor, skill):
    """
    Connects to ESCO database and retrieves the ID from skill's name, notice only one record maximun is retrieved
    :param cursor: database cursor
    :param skill: skill name
    :return: description string
    """

    statement = 'SELECT ROWID FROM skills WHERE preferredLabel = \"' + skill + '\" COLLATE NOCASE LIMIT 1;'
    cursor.execute(statement)
    record = cursor.fetchone()
    if record is None:
        return -1
    skill_id = int(record[0])
    return skill_id


