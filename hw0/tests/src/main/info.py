from src.main.db import get_all_accounts,get_account_by_session_token,get_account_by_username,find_in_db,sort_in_db,session_token_in_db

def show_info():
    print("Welcome to the App!")
    print("login: ./app 'login <username> <password>'")
    print("join: ./app 'join'")
    print("create: ./app 'create username=\"<value>\" password=\"<value>\" name=\"<value>\" status=\"<value>\"'")
    print("people: ./app 'people'")

def show_session_token_invalid():
    print("invalid request: invalid session token\nhome: ./app\n")

def show_info_with_session_token(session_token):
    account = get_account_by_session_token(session_token)
    if account:   
        print(
            f"Welcome back to the App, {account.name}!\n\n"
            f"\"{account.status}\"\n\n"
            f"edit: ./app 'session {account.session_token} edit'\n"
            f"update: ./app 'session {account.session_token} update (name=\"<value>\"|status=\"<value>\")+''\n"
            f"logout: ./app 'session {account.session_token} logout'\n"
            f"people: ./app '[session {account.session_token} ]people'\n"
        )
    else:
        show_session_token_invalid()


def show_info_with_account(account):
    print(
        f"Person\n"
        f"------\n"
        f"name: {account.name}\n"
        f"username: {account.username}\n"
        f"status: {account.status}\n"
        f"updated: {account.updated}\n"
        f"\n"
        f"edit: ./app 'session {account.session_token} edit'\n"
        f"update: ./app 'session {account.session_token} update (name=\"<value>\"|status=\"<value>\")+''\n"
        f"delete: ./app 'session {account.session_token} delete'\n"
        f"logout: ./app 'session {account.session_token} logout'\n"
        f"people: ./app '[session {account.session_token} ]people'\n"
        f"home: ./app ['session {account.session_token}']"
    )

def show_people():
    accounts = get_all_accounts()
    print("People\n------\n")
    if len(accounts)==0:
        print("No one is here...")
    else:
        for account in reversed(accounts):
            print(
                f"{account.name} @{account.username} (./app 'show {account.username}')\n"
                f"  {account.status}\n"
                f"  @ {account.updated}\n"
            )
    print("\nfind: ./app 'find <pattern>'\n")
    print("sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'\n")
    print("join: ./app 'join'\n")
    print("create: ./app 'create username=\"<value>\" password=\"<value>\" name=\"<value>\" status=\"<value>\"'\n")
    print("home: ./app\n")

def show_people_with_session_token(session_token):
    accounts = get_all_accounts()
    if session_token not in [account.session_token for account in accounts]:
        show_session_token_invalid()
    else:
        print("People\n------\n")
        for account in accounts:
            print(
                f"{account.name} @{account.username} (./app 'show {account.username}')\n"
                f"  {account.status}\n"
                f"  @ {account.updated}\n"
            )
            if session_token == account.session_token:
                print(f"  edit: ./app 'session {session_token} edit'\n")
    print("\nfind: ./app 'find <pattern>'\n")
    print("sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'\n")
    print(f"update: ./app 'session {session_token} update (name=\"<value>\"|status=\"<value>\")+''\n")
    print(f"home: ./app ['session {session_token}']")

def show_person(username):

    temp = username.split(" ")
    if len(temp)>1:
        if temp[1] == "people":
            username = temp[0]

    if not username:
        print("invalid request: missing username\nhome: ./app\n")
    else:
        account = get_account_by_username(username)
        if account:
            print(
                f"Person\n"
                f"------\n"
                f"name: {account.name}\n"
                f"username: {account.username}\n"
                f"status: {account.status}\n"
                f"updated: {account.updated}\n"
                f"\n"
                f"people: ./app 'people'\n"
                f"home: ./app"
            )
        else:
            print("not found\nhome: ./app\n")

def show_person_with_session_token(session_token, username):
    account = get_account_by_username(username)

    if not username:
        print("invalid request: missing username\nhome: ./app\n")
    elif not session_token_in_db(session_token):
        show_session_token_invalid()
    else:
        if account:
            print(
                f"Person\n"
                f"------\n"
                f"name: {account.name}\n"
                f"username: {account.username}\n"
                f"status: {account.status}\n"
                f"updated: {account.updated}\n"
                f"\n"
            )
            if session_token == account.session_token:
                print(
                    f"edit: ./app 'session {session_token} edit'\n"
                    f"update: ./app 'session {session_token} update (name=\"<value>\"|status=\"<value>\")+''\n"
                    f"delete: ./app 'session {session_token} delete'\n"
                )
            print(    
                f"people: ./app '[session {session_token} ]people'\n"
                f"home: ./app ['session {session_token}']"
                f"logout: ./app 'session {session_token} logout'\n"
            )
        else:
            print("not found\nhome: ./app\n")

def find_account(args):
    if ':' in args:
        field, value = args.split(':')
        if field in ['username', 'name', 'status', 'updated']:
            field,value = field.strip(),value.strip()
        else:
            field = 'any'
            value = args.strip()
    else:
        field = 'any'
        value = args.strip()
    results = find_in_db(field,value)
    if value=="":
            print("People (find all)")
    else:
        print(f'People (find "{value}" in {field})')
    if results:
        print('----------------------------')
        for username, name, status, updated in results:
            print(f'{name} @{username} (./app \'show {username}\')')
            print(f'  {status}')
            print(f'  @ {updated}')
    else:
        print("No one is here...")
        
    print('find: ./app \'find <pattern>\'')
    print('sort: ./app \'sort[ username|name|status|updated[ asc|desc]]\'')
    print('people: ./app \'people\'')
    print('join: ./app \'join\'')
    print('create: ./app \'create username="<value>" password="<value>" name="<value>" status="<value>"\'')
    print('home: ./app')

def find_account_with_session_token(session_token):
    print("People (find all)")
    account = get_account_by_session_token(session_token)
    if account:
        print(f'session {session_token}')
    else:
        show_session_token_invalid()


def sort_account(args):
    sort_field = 'updated'
    sort_order = 'desc'
    
    parts = args.split()
    if len(parts) == 1:
        sort_field = parts[0]
        if sort_field != 'updated':
            sort_order = 'asc'
    elif len(parts) == 2:
        sort_field = parts[0]
        sort_order = parts[1]
    
    valid_fields = ['username', 'name', 'status', 'updated']
    valid_orders = ['asc', 'desc']
    
    if sort_field not in valid_fields:
        print("not found")
        return False
    
    if sort_order not in valid_orders:
        print("not found")
        return
    
    results = sort_in_db(sort_field, sort_order)
    
    # Display sorted results
    if sort_field == 'updated':
        sort_order_str = 'oldest' if sort_order == 'asc' else 'newest'
    else:
        sort_order_str = 'a-z' if sort_order == 'asc' else 'z-a'
    print(f"People (sorted by {sort_field}, {sort_order_str})")
    print('----------------------------')
    for username, name, status, updated in results:
        print(f'{name} @{username} (./app \'show {username}\')')
        print(f'  {status}')
        print(f'  @ {updated}')
    
    # Provide further instructions
    print('find: ./app \'find <pattern>\'')
    print('sort: ./app \'sort[ username|name|status|updated[ asc|desc]]\'')
    print('people: ./app \'people\'')
    print('join: ./app \'join\'')
    print('create: ./app \'create username="<value>" password="<value>" name="<value>" status="<value>"\'')
    print('home: ./app')
