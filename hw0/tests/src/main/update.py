from datetime import datetime
import re

from src.main.info import show_info_with_account,show_session_token_invalid
from src.main.db import get_account_by_session_token, update_account_to_db

def update_account(session_token,args):
    account = get_account_by_session_token(session_token)
    if account:
        if "=" in args:
            change_status,change_name = False,False
            update_data = re.findall(r'(\w+)=["\']([^"\']*)["\']', args)
            update_data = {key: value for key, value in update_data}

            if "status" in update_data:
                if len(update_data["status"]) <1:
                        print("failed to update: status is too short\n")
                elif len(update_data["status"]) >100:
                    print("failed to update: status is too long\n")                        
                else:
                    change_status = account.update_status(update_data["status"])

            if "name" in update_data:               
                if len(update_data["name"]) <3:
                    print("failed to update: name is too short\n")
                elif len(update_data["name"]) >20:
                    print("failed to update: name is too long\n")
                else:
                    change_name = account.update_name(update_data["name"])

            update_account_to_db(account)

            if change_status and change_name:
                print("[name and status updated]\n")
            elif change_status:
                print("[status updated]\n")
            elif change_name:
                print("[name updated]\n")
            else:
                print("failed to update: missing name and status\n")

            show_info_with_account(account)
        else :
            print("failed to update: missing name and status\n")
    else:
        show_session_token_invalid()

def edit(session_token):
    account = get_account_by_session_token(session_token)
    if account:
        print("Edit Person\n-----------")
        print("leave blank to keep [current value]\n")
        new_name= input(f"name [{account.name}]: ")
        new_status = input(f"status [{account.status}]: ")

        if new_name and new_status and new_name!= account.name and new_status!=account.status:
            account.update_name(new_name)
            account.update_status(new_status)
            update_account_to_db(account)
            print("[name and status updated]\n")
            print("===========")
        elif new_name and new_name!= account.name:
            account.update_name(new_name)
            update_account_to_db(account)
            print("[name updated]\n")
            print("===========")
        elif new_status and new_status!=account.status:
            account.update_status(new_status)
            update_account_to_db(account)
            print("[status updated]\n")
            print("===========")

        show_info_with_account(account)
    else:
        show_session_token_invalid()


