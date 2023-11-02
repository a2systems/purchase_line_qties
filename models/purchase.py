from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date,datetime

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def btn_update_qties(self):
        self.ensure_one()
        if self.state not in ['done','purchase']:
            raise ValidationError(_('Order line in incorrect state'))
        vals = {
            'line_id': self.id,
            }
        wizard_id = self.env['purchase.line.qties.wizard'].create(vals)
        res = {
            'name': _('Update line qties wizard'),
            'res_model': 'purchase.line.qties.wizard',
            'view_mode': 'form',
            'res_id': wizard_id.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return res
