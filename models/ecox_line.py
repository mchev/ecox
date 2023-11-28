from odoo import models, fields

class EcoxLine(models.TransientModel):
    _name = 'ecox.line'
    _description = "Line model for ecox views"

    recursive_product_search_id = fields.Many2one('recursive.product.search.wizard', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    lot_id = fields.Many2one('stock.lot', string="Serial number")
    product_qty = fields.Float(string="Product Quantity")

    def __str__(self):
        return f'{self.product_id.display_name} - {self.lot_id.name} - {self.product_qty}'