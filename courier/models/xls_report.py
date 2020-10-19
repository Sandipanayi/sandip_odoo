from odoo import models

class CourierXlsx(models.AbstractModel):
    _name = 'report.courier.report_cou_id_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print("lllinees",lines)
        format1 = workbook.add_format({'font_size':14,'align':'vcenter','bold':True})
        format2 = workbook.add_format({'font_size':10,'align':'vcenter',})
        sheet = workbook.add_worksheet("courier_name")
        sheet.write(1, 1, "Name", format1)
        sheet.write(1, 2,lines.name,format2)
        sheet.write(1, 2, "From_id", format1)
        sheet.write(2, 3,lines.courier_from_id.id,format2)
