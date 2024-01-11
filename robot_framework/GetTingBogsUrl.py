def TingBogsURL():
    import pyodbc
    import numpy as np
    from GetBFENR import GetBFENumber
    CaseInfo = GetBFENumber()
    CaseUuid = CaseInfo[0]
    BFENumber = CaseInfo[1]

    # Define your connection string
    conn_str = (
        "Driver={SQL Server};"
        "Server=srvsql29;"
        "Database=LOIS;"
        "Trusted_Connection=yes;"  # since Integrated Security is True
    )

    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Define the variable to replace 'Ejendomsnummer'
    bfe_nr_value = BFENumber  # Replace with the actual value you want to use

    # Define the SQL query with a placeholder for the variable
    sql_query = """
    SELECT TOP (10)
        [LFE_nr],
        [adresse],
        [BFEnr],
        [TlyAttestUrl]
    FROM [LOIS].[ETL].[EjendomSoegningGeoview]
    WHERE BFEnr LIKE ?
    """

    # Execute the query with the variable
    cursor.execute(sql_query, bfe_nr_value)

    # Fetch the data
    data = cursor.fetchall()

    # Convert the data to a NumPy array (if needed)
    numpy_array = np.array(data)

    # Close the database connection
    conn.close()

    # Now you can use numpy_array for further processing with NumPy
    return numpy_array