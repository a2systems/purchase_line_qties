from odoo import fields,models, api, _
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import date

_logger = logging.getLogger(__name__)

class PurchaseLineQtiesWizard(models.TransientModel):
    _name = 'purchase.line.qties.wizard'
    _description = 'purchase.line.qties.wizard'

    line_id = fields.Many2one('purchase.order.line','Line')
    order_id = fields.Many2one('purchase.order','Order',related='line_id.order_id')
    product_id = fields.Many2one('product.product','Producto',related='line_id.product_id')
    qty_received = fields.Float('Quantity Received',related='line_id.qty_received')
    new_qty_received = fields.Float('New Quantity Received')

    def btn_confirm(self):
        if self.new_qty_received < 0:
            raise ValidationError(_('New quantity received has to be greater than 0'))
        msg = 'Quantities for line %s changed from %s to %s'%(self.line_id.name,self.qty_received,self.new_qty_received)
        sql_statement = "UPDATE PURCHASE_ORDER_LINE SET QTY_RECEIVED = %s WHERE ID = %s"%(self.new_qty_received,self.line_id.id)
        self.env.cr.execute(sql_statement)
        self.env.cr.commit()
        self.order_id.message_post(body=msg)
