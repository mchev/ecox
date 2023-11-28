from odoo import models, fields, api

class RecursiveProductSearchWizard(models.TransientModel):
    _name = 'recursive.product.search.wizard'
    _description = "Wizard for searching components"

    component_id = fields.Many2one('product.product', string="Component", required=True)
    lot_lines = fields.One2many('ecox.line', 'recursive_product_search_id', string="Serial Numbers")

    @api.onchange('component_id')
    def _onchange_component_id(self):
        # Clear the lines before recomputing
        self.lot_lines = [(5, 0, 0)]

        line_obj = self.env['ecox.line']
        products = self._get_products_from_component(self.component_id)

        # Create new lines.
        for product in products:
            product_id, bom_line_id = product

            product = self.env['product.product'].browse(product_id)
            bom_line = self.env['mrp.bom.line'].browse(bom_line_id)
            lot_line = self.env['stock.lot'].search([('product_id', '=', product.id)], limit=1)

            self.lot_lines += line_obj.create({
                'recursive_product_search_id': self.id,
                'product_id': product_id,
                'lot_id': lot_line.id,
                'product_qty': bom_line.product_qty,
            })

    def _get_products_from_component(self, component, products=None):
        if products is None:
            products = set()

        bom_lines = self.env['mrp.bom.line'].search([('product_id', '=', component.id)])
        for bom_line in bom_lines:
            variant_id = bom_line.bom_id.product_tmpl_id.product_variant_id.id
            bom_line_id = bom_line.id
            if variant_id not in products:
                products.add((variant_id, bom_line_id))
                self._get_products_from_component(bom_line.bom_id.product_tmpl_id.product_variant_id, products)

        return products
