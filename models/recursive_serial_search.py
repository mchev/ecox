from odoo import models, fields, api

class RecursiveSerialSearch(models.Model):
    _name = 'recursive.serial.search'
    _description = "Recursive Search for Products with Serial Numbers based on a Component in the Bill of Materials (BoM)."

    component_id = fields.Many2one('product.product', string="Component", required=True)
    lot_ids = fields.One2many('stock.lot', compute="_compute_lot_ids", string="Serial Numbers")

    @api.depends('component_id')
    def _compute_lot_ids(self):
        for record in self:
            products = self._get_products_from_component(self.component_id)
            lot_ids = self.env['stock.lot'].search([('product_id', 'in', list(products))])
            record.lot_ids = lot_ids

    def _get_products_from_component(self, component, products=None):
        if products is None:
            products = set()

        bom_lines = self.env['mrp.bom.line'].search([('product_id', '=', component.id)])
        for bom_line in bom_lines:
            variant_id = bom_line.bom_id.product_tmpl_id.product_variant_id.id
            if variant_id not in products:
                products.add(variant_id)
                self._get_products_from_component(bom_line.bom_id.product_tmpl_id.product_variant_id, products)

        return products