#
import os, sys
import subprocess as sp
import ldap as lp

stdoutOrigin=sys.stdout 
sys.stdout = open("inspect_log.txt", "w")

# Open a file
dir_path = str(sys.argv[1])
dirs = os.listdir( dir_path )
output=""
print("You are inspecting repo under path", dir_path)

#List the directories and their contributers
for d in sorted(os.listdir(dir_path)):
    if os.path.isdir(os.path.join(dir_path, d)) and d != 'tests':
        d += '/'
        output+='\n'+d +'\n'
        output += sp.getoutput(f'git blame -e src/pybind/mgr/{d}/module.py | cut -d\'(\' -f 2 | cut -d \'2\' -f 1 | grep \'redhat.com\' | sed \'s/[<>]//g\' | sort | uniq;')
       
 
for email in output.split('\n'):
    if '/' in email:
        print('==========\n'+email)
    if 'redhat.com' in email:
        print(email)
        try:
            # Open a connection to the server. LDAP url.
            connect = lp.initialize('ldaps://ldap.corp.redhat.com')
            print('connected..')
        except lp.LDAPError as e:
            print(e)

        try:
            #filters for ldap search
            base_dn = "dc=redhat,dc=com"
            search_scope = lp.SCOPE_SUBTREE
            retrieve_attributes = None
            search_filter = f"mail={email}"
            ldap_result_id = connect.search(base_dn, lp.SCOPE_SUBTREE, search_filter, retrieve_attributes)
        
            result_status, result_data = connect.result(ldap_result_id, 0)
            if result_data == []:
                print(email +' is not an active employee')
            else:
                print(email + " is an active employee")
           
        except lp.LDAPError as e:
            print(e)
