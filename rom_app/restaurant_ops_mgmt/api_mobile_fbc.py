import frappe
from datetime import datetime
import json
from . import api


@frappe.whitelist()
def get_fb_closing_checklist_child_mobile(branch_param):
    print('get_fb_closing_checklist_child_mobile =======', branch_param)
    print("-------- get data ------------")
    current_date = datetime.today().date()
    build_sql = """
    SELECT
        coc.name as parent_name,
        coc.date,
        coc.user_name,
        coc.branch,
        cocc.name as child_name,
        cocc.audit,
        cocc.question
    FROM
        `tabFB Closing Checklist` coc
        JOIN `tabFB Closing Checklist Child` cocc
    ON
        coc.name = cocc.parent
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data


@frappe.whitelist()
def update_fb_closing_checklist_child_mobile(form_values):
    print('update_fb_closing_checklist_child_mobile =======', form_values)
    json_object = json.loads(form_values)
    print(type(json_object))
    field_parent_name = json_object["field_parent_name"]
    print(field_parent_name)
    for x in json_object:
        print(x, " -> ", json_object[x])

#   User
    field_user = json_object["field_user"]
    field_user = split_by_colon(field_user)
    print(field_user)
#   Branch
    field_branch = json_object["field_branch"]
    field_branch = split_by_colon(field_branch)
    print(field_branch)
#   Date
    field_current_date = json_object["field_current_date"]
    field_current_date = split_by_colon(field_current_date)
    print(field_current_date)
#   Parent Id
    field_parent_name = json_object["field_parent_name"]
    field_parent_name = split_by_colon(field_parent_name)
    print(field_parent_name)

    # remove non row values from dict
    json_object.pop('field_user', None)
    json_object.pop('field_branch', None)
    json_object.pop('field_current_date', None)
    json_object.pop('field_parent_name', None)

    for x in json_object:
        print(x, " <-> ", json_object[x])

    parent_doc = frappe.get_doc("FB Closing Checklist", field_parent_name)
    print(parent_doc)
    for q in parent_doc.questions:
        disp = f"name {q.name}  = qaudit  {q.audit} = qquestion  {q.question}"
        print(disp)
        child_name = q.name
        print('child_name', child_name)
        value_from_user = json_object[str(child_name)]
        print('value_from_user', value_from_user)
        if (value_from_user == 1):
            q.audit = 1
        else:
            q.audit = 0
        q.save()
    parent_doc.db_update()
    frappe.db.commit()


@frappe.whitelist()
def fb_closing_check_today_record_exits_otherwise_create_one(branch,
                                                             current_date,
                                                             email_id,
                                                             user_name):
    res = fb_closing_check_today_record_exist(branch, user_name, current_date)
    if (res is False):
        fb_closing_insert_today_records(branch, current_date,
                                        email_id, user_name)
        return "record created successfully"
    return "record already exist"


def fb_closing_check_today_record_exist(branch, user_name, current_date):
    print('fb_closing_check_today_record_exist')
    # current_date = datetime.today().date()
    rec_count = frappe.db.count("FB Closing Checklist", filters={
            'user_name': user_name,
            'branch': branch,
            'date': current_date
        })

    print('*** rec_count')
    print(rec_count)
    if (rec_count > 0):
        print(" *** record_exists")
        return True

    print(" *** record_does_not_exists")
    return False


def fb_closing_insert_today_records(branch, current_date,
                                    email_id, user_name):
    print('fb_closing_insert_today_records')
    print('branch-', branch)
    print('current_date-', current_date)
    print('email_id-', email_id)
    print('user_name-', user_name)
    print("^^^^^^^^^^^^^^^^^")
    parent = frappe.new_doc('FB Closing Checklist')
    parent.branch = branch
    parent.date = current_date
    parent.user_name = user_name
    parent.save(ignore_permissions=True)

    parent_new = frappe.get_last_doc('FB Closing Checklist',
                                     filters={"branch": branch,
                                              "user_name": user_name,
                                              "date": current_date
                                              })
    print(parent_new)
    print(parent_new.name)
    # Create child entries for the parent
    q_template = api.get_fb_closing_checklist_child(branch)
    print('q_template')
    print(q_template)
    print('====== q_template item =============')
    for item in q_template:
        print(item)
        template_question = item[2]
        child = frappe.get_doc({
            'doctype': 'FB Closing Checklist Child',
            'parent': parent_new.name,
            'parentfield': 'questions',
            'parenttype': 'FB Closing Checklist',
            'audit': 0,
            'question': template_question,
        })
        child.insert(ignore_permissions=True)


def get_fb_closing_checklist_template_child_mobile(branch_param):
    print('get_fb_closing_checklist_template_child_mobile ====', branch_param)
    print("-------- get data ------------")
    current_date = datetime.today().date()
    build_sql = """
    SELECT
        coc.name as parent_name,
        coc.date,
        coc.user_name,
        coc.branch,
        cocc.name as child_name,
        cocc.audit,
        cocc.question
    FROM
        `tabFB Closing Checklist` coc
        JOIN `tabFB Closing Checklist Child` cocc
    ON
        coc.name = cocc.parent
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data


def split_by_colon(full_data):
    all_data = full_data.split(':')
    actual_value = all_data[1]
    actual_value = actual_value.strip()
    return actual_value