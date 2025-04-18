import frappe
import yaml
import json
import socket


def execute(filters=None):
    # print("=========================")
    # print(yaml.dump(filters))
    data, columns = [], []
    columns = get_columns()
    cs_data = get_data(filters)
    # branch date raw_material quantity price unit closing_quantity
    data = []
    for d in cs_data:
        row = frappe._dict({
            'trans_type': d.trans_type,
            'name': d.name,
            'date': d.date,
            'branch': d.branch,
            'user_name': d.user_name,
            'raw_material': d.raw_material,
            'unit': d.unit,
            'qty': d.qty,
            'price': d.price,
            'amount': d.amount,
            'link': d.link,
            'rm_group': d.rm_group,
            'vendor_name': d.vendor_name
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'trans_type',
            'label': 'Trans Type',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'HTML',
        },
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'branch',
            'label': 'Branch',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'user_name',
            'label': 'User Name',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'raw_material',
            'label': 'Raw Material',
            'fieldtype': 'Data',
            'width': 350
        },
        {
            'fieldname': 'unit',
            'label': 'Unit',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'qty',
            'label': 'Quantity',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'price',
            'label': 'Price',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'amount',
            'label': 'Amount',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'rm_group',
            'label': 'RM Group',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'vendor_name',
            'label': 'Vendor',
            'fieldtype': 'Data',
        }
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    # print("-------- get data ------------")
    # print(conditions)
    sql_se = build_sql_se(conditions)
    sql_indent = build_sql_indent(conditions)
    sql_waste = build_sql_waste(conditions)
    # sql_invcount = build_sql_invcount(conditions)
    # full_sql = find_transtype_only_sql(conditions, sql_se, sql_indent, sql_waste, sql_invcount)
    full_sql = find_transtype_only_sql(conditions, sql_se, sql_indent, sql_waste)
    # print("-------- full sql ------------")
    # print(full_sql)
    data = frappe.db.sql(full_sql, as_dict=True)
    data_with_anchor = formate_link_column_to_anchor_link(data)
    # print('data_with_anchor')
    # print(data_with_anchor)
    return data_with_anchor


def find_transtype_only_sql(conditions, sql_se, sql_indent, sql_waste):
    # print('find_transtype_only_sql')

    if "trans_type_filter" in conditions:
        filter_val = conditions['trans_type_filter']
        if filter_val == 'SE':
            return sql_se
        elif filter_val == 'Indent':
            return sql_indent
        elif filter_val == 'Waste':
            return sql_waste
        # elif filter_val == 'InvCount':
        #     return sql_invcount
    # full_sql = f"{sql_se}  UNION  {sql_indent}  UNION  {sql_waste}  UNION  {sql_invcount}"
    full_sql = f"{sql_se}  UNION  {sql_indent}  UNION  {sql_waste}"
    return full_sql


def build_sql_se(conditions):
    sql = """
    SELECT "Stock" as trans_type,
    par.name, par.date, par.branch,  par.user_name,
    raw.item as raw_material, chi.unit, chi.ord_qty as qty,
    chi.unit_price AS price, chi.amount,
    rmgrp.group_name  as rm_group,
    ven.template_type_name as vendor_name
    FROM `tabStock Entry` par
    LEFT JOIN `tabStock Entry Child` chi ON chi.parent = par.name
    LEFT JOIN `tabRaw Material Only` raw ON chi.raw_material = raw.name
    LEFT JOIN `tabRaw Material Group` rmgrp ON raw.rm_group = rmgrp.name
    LEFT JOIN tabVendor ven ON par.vendor = ven.name
    """
    full_sql = get_where_filter(sql, conditions)
    full_sql = get_where_filter_for_vendor(full_sql, conditions)
    return full_sql


def build_sql_indent(conditions):
    sql = """
    SELECT "Indent" as trans_type,
    par.`name`, par.`date`, 	par.branch,	par.user_name,
    raw.item as raw_material, chi.unit, chi.issued_qty as qty,
    chi.price, chi.amount,
    rmgrp.group_name  as rm_group,
    '' as vendor_name
    FROM `tabChef Indent By Dept` par
    LEFT JOIN `tabChef Indent By Dept Child` chi on par.name = chi.parent
    LEFT JOIN `tabRaw Material Only` raw ON chi.raw_material = raw.name
    LEFT JOIN `tabRaw Material Group` rmgrp ON raw.rm_group = rmgrp.name
    """
    full_sql = get_where_filter(sql, conditions)
    return full_sql


def build_sql_waste(conditions):
    sql = """
    SELECT  "Waste" as trans_type,
    par.name, par.date, par.branch, par.user_name,
    raw.item as raw_material, chi.unit, chi.wastage_qty as qty,
    chi.unit_price as price , chi.amount,
    rmgrp.group_name  as rm_group,
    ''  as vendor_name
    FROM `tabInventory Wastage` par
    LEFT JOIN `tabInventory Wastage Child` chi ON chi.parent = par.name
    LEFT JOIN `tabRaw Material Only` raw ON chi.raw_material = raw.name
    LEFT JOIN `tabRaw Material Group` rmgrp ON raw.rm_group = rmgrp.name

    """
    full_sql = get_where_filter(sql, conditions)
    return full_sql


def get_where_filter(sql, conditions):
    where_cond = f" WHERE par.`date` between '{conditions['from_date_filter']}' AND '{conditions['to_date_filter']}' "
    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND par.branch = '{conditions['branch_filter']}' "
    if "raw_material_filter" in conditions:
        where_cond = where_cond + f" AND chi.raw_material = '{conditions['raw_material_filter']}' "
    if "rmgroup_filter" in conditions:
        where_cond = where_cond + f" AND raw.rm_group = '{conditions['rmgroup_filter']}' "
    if "raw_material_like_filter" in conditions:
        where_cond = where_cond + f" AND raw.item LIKE '%{conditions['raw_material_like_filter']}%' "

    sql = f"{sql}  {where_cond}"
    return sql


def get_where_filter_for_vendor(sql, conditions):
    vendor_filter_cond = ''
    if "vendor_filter" in conditions:
        vendor_filter_cond = f" AND par.vendor = '{conditions['vendor_filter']}' "
    sql = f"{sql}  {vendor_filter_cond}"
    return sql


def formate_link_column_to_anchor_link(data):
    # print('format_link_column_to_anchor_link')
    domain_url = get_domain_name_of_the_site()

    for d in data:
        # print(d)
        # d.update({})
        trans_type = d.trans_type
        name = d.name
        # print(trans_type, name)
        formatted_url = formate_the_url(domain_url, trans_type, name)
        # print(formatted_url)
        d.name = formatted_url

    return data


def get_conditions(filters):
    conditions = {}
    if (type(filters) is str):
        filters = json.loads(filters)

    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value
    return conditions


def formate_the_url(domain_name, trans_type, trans_id):
    part_url = get_url_path_based_on_trans_type(trans_type)
    # farmate_part_url_with_id = f"{domain_name}/app/{part_url}/{trans_id}"
    farmate_part_url_with_id = f"/app/{part_url}/{trans_id}"
    anchor = f"<a href='{farmate_part_url_with_id}' target='_blank'>{trans_id}</a>"
    # print(anchor)
    return anchor


def get_url_path_based_on_trans_type(trans_type):
    if trans_type == 'Stock':
        return 'stock-entry'
    elif trans_type == 'Indent':
        return 'chef-indent-by-dept'
    elif trans_type == 'Waste':
        return 'inventory-wastage'
    # elif trans_type == 'InvCount':
    #     return 'inventory-counting'


def get_domain_name_of_the_site():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    # print("Your Computer Name is:" + hostname)
    # print("Your Computer IP Address is:" + IPAddr)
    domain_url = frappe.db.get_value('Rom Settings',
                                     {'settings_name': 'domain_name'},
                                     ['settings_value'])
    # print('domain_url ---> ', domain_url)
    return domain_url

# http://rom_site:8000/app/purchase-order/47
# http://rom_site:8000/app/chef-indent-by-dept/19
# http://rom_site:8000/app/inventory-wastage/8
# http://rom_site:8000/app/inventory-counting/5
