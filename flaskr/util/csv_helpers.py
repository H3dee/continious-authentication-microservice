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


def print_csv_header_action(feature_file):
    feature_file.write("type_of_action,traveled_distance_pixel,elapsed_time,direction_of_movement,")
    feature_file.write("straightness,num_points,sum_of_angles,mean_curv,sd_curv,max_curv,min_curv,mean_omega,"
                       "sd_omega,max_omega,min_omega,")
    feature_file.write("largest_deviation,dist_end_to_end_line,num_critical_points,")
    feature_file.write("mean_vx,sd_vx,max_vx,min_vx,mean_vy,sd_vy,max_vy,min_vy,mean_v,sd_v,max_v,min_v,mean_a,sd_a,"
                       "max_a,min_a,mean_jerk,sd_jerk,max_jerk,min_jerk,a_beg_time,class,n_from,n_to")

    feature_file.write("\n")
    return
