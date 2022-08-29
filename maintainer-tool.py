#
import os, sys
import subprocess as sp
import ldap as lp
import argparse

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="directory path to inspect from, default: src/pybind/mgr/", action="store_true", default="src/pybind/mgr/")
parser.add_argument("-t", "--time", help="start time to inspect the data from, default: 2022-01-01", action="store_true", default="2022-01-01")
parser.add_argument("-rh", "--RH", help="weather to filter RH employees, default: True", action="store_true", default=True)
parser.add_argument("-o", "--output", help="output file to store results in, default: False", action="store_true", default=False)
args = parser.parse_args()

dir_path = args.path
time = args.time
employee_only = args.RH
if args.output:
    stdoutOrigin=sys.stdout 
    sys.stdout = open("output.txt", "w")

# Open a file
dirs = os.listdir( dir_path )
output=""
print(f"You are inspecting repo under path {dir_path}")

#List the directories and their contributers
for d in sorted(os.listdir(dir_path)):
    if os.path.isdir(os.path.join(dir_path, d)) and d != 'tests':
        d += '/'
        output+='\n'+d +'\n'
        output += sp.getoutput(f'git blame -e {dir_path}{d}/module.py | cut -d\'(\' -f 2 | cut -d \'2\' -f 1 | grep \'redhat.com\' | sed \'s/[<>]//g\' | sort | uniq;')
       
 
for email in output.split('\n'):
    if '/' in email:
        print('==========\n'+email)
    if 'redhat.com' in email:
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
