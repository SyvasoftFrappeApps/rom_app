import frappe
from frappe.model.document import Document
from datetime import datetime
import rom_app.scheduled_tasks
from frappe.utils import now
from frappe.utils import date_diff
from ... import utils


class ChefIndentByDept(Document):
    def validate(self):
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        print('date_difference ', date_difference)
        if (date_difference > 60):
            frappe.throw("You cannot save a record that is over 60 days old")

    def before_save(self):
        print('before save python')
        print('^^^^^^^^^^^^^^^^^^^')
        print(self)
        print('^^^^^^^^^^^^^^^^^^^')
        print(self.raw_materials)
        doc_date = self.date
        my_original_doc = self.get_doc_before_save()
        if my_original_doc is not None:
            intial_date = my_original_doc.date
            self.previous_date = intial_date
        else:
            self.previous_date = doc_date
            
        for item in self.raw_materials:
            print('------------------------------ - ')
            if (item.issu_qty_entry is None):
                return
            print('item.issu_qty_entry - ', item.issu_qty_entry)
            # print('item.issued_qty - ', item.issued_qty)
            if (item.issu_qty_entry == 0):
                print('==0')
                issu_qty_entry_minus = 0
            else:
                print('!=0')
                issu_qty_entry_minus = -1 * item.issu_qty_entry
            print('issu_qty_entry_minus ', issu_qty_entry_minus)
            item.issued_qty = issu_qty_entry_minus
            print('item.issued_qty ', item.issued_qty)
        

    def get_the_record_count(self, branch, user_name, date_obj):
        rec_count = frappe.db.count('Chef Indent By Dept', filters={
            'user_name': user_name,
            'branch': branch,
            'date': date_obj
        })
        return rec_count

    def listToString(s):
        str1 = " "
        return (str1.join(s))

    @frappe.whitelist()
    def get_raw_material(self, branch, department):
        print("inside python")
        sql = """
        SELECT rawmat.item, child.indent_unit, rawmat.name
        FROM `tabRaw Material For Indent` parent
        JOIN `tabRaw Material For Indent Child` child
        ON	parent.name = child.parent
        JOIN `tabRaw Material Only` rawmat
        ON	rawmat.name = child.raw_material
        WHERE parent.branch = '{}'
        AND parent.department = '{}';
        """
        sql = sql.format(branch, department)
        print(sql)
        item_data = frappe.db.sql(sql, as_dict=0)
        res_length = len(item_data)
        print(res_length)
        print(item_data)
        return item_data

    @frappe.whitelist()
    def get_raw_material_with_id(self, branch, department):
        print("inside python")
        sql = """
        SELECT child.raw_material, child.indent_unit, trmo.item,
        trmo.price, trmo.closing_stock
        FROM `tabRaw Material For Indent` parent
        JOIN `tabRaw Material For Indent Child` child
        ON	parent.name = child.parent
        JOIN `tabRaw Material Only` trmo
        ON child.raw_material  = trmo.name
        WHERE parent.branch = '{}'
        AND parent.department = '{}'
        ORDER BY child.idx ASC ;
        """
        sql = sql.format(branch, department)
        print(sql)
        item_data = frappe.db.sql(sql, as_dict=0)
        res_length = len(item_data)
        print(res_length)
        print(item_data)
        return item_data

    # @frappe.whitelist()
    # def test(self):
    #     print('item_data')
    #     return 'item_data'

    def on_update(self):
        print(' >> on_update << ')
        print(self)
        print("Formatted date and time:", now())
        user_email = frappe.session.user
        branch = utils.find_user_branch_based_on_email(user_email)
        print("on_update - branch:", branch)
        doc_date = self.date
        # rom_app.scheduled_tasks.inventory_summary(branch, doc_date)
        previous_date = self.previous_date
        date_format = "%Y-%m-%d"
        if isinstance(doc_date, str):
            doc_date = datetime.strptime(doc_date, date_format).date()
        if isinstance(previous_date, str):
            previous_date = datetime.strptime(previous_date, date_format).date()
        if doc_date > previous_date:
            doc_date = previous_date
        doc_date = doc_date.strftime("%Y-%m-%d")
        frappe.enqueue(
            rom_app.scheduled_tasks.inventory_summary,
            queue='long',
            p_branch=branch, p_date=doc_date)
        
    def after_delete(self):
        user_email = frappe.session.user
        branch = utils.find_user_branch_based_on_email(user_email)
        # print("on_update - branch:", branch)
        doc_date = self.date
        doc_date = doc_date.strftime("%Y-%m-%d")
        print("after delete - branch: docdate", branch, doc_date)
        print(' >> after_delete << <<<<<<<<<<<<<<<<<<< ')
        # rom_app.scheduled_tasks.inventory_summary(branch, doc_date)
        frappe.enqueue(
            rom_app.scheduled_tasks.inventory_summary,
            queue='long',
            p_branch=branch, p_date=doc_date)
