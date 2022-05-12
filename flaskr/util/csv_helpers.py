def sql_query_to_csv(path_of_file_to_write_in, query_output, headers):
    rows = query_output

    target_file = open(path_of_file_to_write_in, "w")

    for header in headers:
        target_file.write(header + ",")
    target_file.write("\n")

    for row in rows:
        for header in headers:
            target_file.write(str(row[header]) + ",")
        target_file.write("\n")

    target_file.close()
