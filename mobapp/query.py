
############### RESIDENT TABLE ##############################################################
query_add_resident      = 'INSERT INTO resident VALUES(%s, %s ,%s ,%s )'
query_remove_reident    = "DELETE FROM resident WHERE id= %s"
query_check_resident    = "SELECT * FROM resident WHERE id = %s AND password = %s"
query_get_room          = "SELECT room FROM resident WHERE id = %s"
query_get_resident_name = "SELECT name FROM resident WHERE id = %s "
query_get_all_residents = 'SELECT * FROM resident'
query_validate_resident_access  = "SELECT * FROM resident WHERE id = %s "
query_get_resident_id   = "SELECT id FROM resident WHERE room = %s"

############### VISITOR TABLE ################################################################
query_signup_visitor    = "INSERT INTO visitor VALUES(%s, %s, %s)"
query_remove_visitor    = "DELETE FROM visitor WHERE id= %s"
query_check_user_exists = "SELECT * FROM visitor WHERE id = %s "
query_check_visitor     = "SELECT * FROM visitor WHERE id = %s AND password = %s"
query_get_visitor_name  = "SELECT name FROM visitor WHERE id = %s "
query_get_all_visitors  =  "SELECT * FROM visitor"


############### ACCESS TABLE #################################################################
query_add_access         = "INSERT INTO access(room,id) VALUES(%s, %s)"
query_remove_access      = "DELETE FROM access WHERE ind= %s"
query_remove_access_by_resident = "DELETE FROM access WHERE id= %s and room= %s"
query_get_access         = 'SELECT id FROM access WHERE room = %s'
query_get_visitor_access = 'SELECT room FROM access WHERE id = %s'
query_validate_access   = "SELECT * FROM access WHERE room = %s AND id = %s"
query_join_access_visitors = 'SELECT visitor.id,name,room,ind FROM visitor INNER JOIN access ON visitor.id = access.id'
############### ADMIN TABLE ##################################################################
query_check_admin       = "SELECT * FROM admin WHERE user = %s AND password = %s"

############### BLACKLIST TABLE ##############################################################
query_add_to_blacklist  = "INSERT INTO blacklist VALUES(%s,%s,%s)"
query_from_blacklist    = "DELETE FROM blacklist WHERE id= %s"
query_get_all_blacklist = "SELECT * FROM blacklist"
query_check_blacklist   = "SELECT * FROM blacklist WHERE id= %s"

############### ACCESS LOGS TABLE ##############################################################

query_get_all_logs  = "SELECT * FROM access_logs "
query_get_room_logs = "SELECT * FROM access_logs WHERE room= %s"
query_get_id_logs   = "SELECT * FROM access_logs WHERE id= %s"
query_get_date_logs  = "SELECT * FROM access_logs WHERE date= %s"
query_insert_logs    = "INSERT INTO access_logs VALUES(%s,%s,%s,%s)"