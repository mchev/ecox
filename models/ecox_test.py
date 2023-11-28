from odoo import models, fields, api

class EcoxTestWizard(models.TransientModel):
    _name = 'ecox.test.wizard'
    _description = "Wizard for searching components"

    component_id = fields.Many2one('product.product', string="Component", required=True)
    lot_lines = fields.One2many('ecox.test.line', 'ecox_test_id', string="Serial Numbers")
    
    @api.onchange('component_id')
    def _onchange_component_id(self):
        line_obj = self.env['ecox.test.line']
        
        products = self._get_products_from_component(self.component_id)

        # clear the lines before recomputing
        self.lot_lines = [(5,)]
        
        # create new lines.
        for product in products:
            product_id, bom_line_id = product

            product = self.env['product.product'].browse(product_id)
            bom_line = self.env['mrp.bom.line'].browse(bom_line_id)
            lot_line = self.env['stock.lot'].search([('product_id', '=', product.id)], limit=1)
            
            self.lot_lines += line_obj.create({
                'ecox_test_id': self.id,
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
            if variant_id not in [product[0] for product in products]:
                products.add((variant_id, bom_line_id))
                self._get_products_from_component(bom_line.bom_id.product_tmpl_id.product_variant_id, products)

        return products