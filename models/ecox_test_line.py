from odoo import models, fields

class EcoxTestLine(models.TransientModel):
    _name = 'ecox.test.line'
    _description = "Line model for 'ecox.test' wizard"

    ecox_test_id = fields.Many2one('ecox.test.wizard', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    lot_id = fields.Many2one('stock.lot', string="Serial number")
    product_qty = fields.Float(string="Product Quantity")

    def __str__(self):
        return f'{self.product_id.display_name} - {self.lot_id.name} - {self.product_qty}'