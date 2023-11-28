from odoo import models, fields, api

class RecursiveSerialSearch(models.Model):
    _name = 'recursive.serial.search'
    _description = "Recursive Search for Products with Serial Numbers based on a Component in the Bill of Materials (BoM)."

    component_id = fields.Many2one('product.product', string="Component", required=True)
    lot_ids = fields.One2many('stock.lot', compute="_compute_lot_ids", string="Serial Numbers")

    @api.depends('component_id')
    def _compute_lot_ids(self):
        for record in self:
            products_with_qty = self._get_products_from_component(record.component_id)
            lot_ids = self.env['stock.lot'].search([('product_id', 'in', list(products_with_qty.keys()))])

            for lot_id in lot_ids:
                lot_id.product_qty = products_with_qty.get(lot_id.product_id.id, 0)

            record.lot_ids = lot_ids

    def _get_products_from_component(self, component, quantity=1, products_with_qty=None):
        if products_with_qty is None:
            products_with_qty = {}

        product_id = component.id

        if product_id in products_with_qty:
            # If the product already exists, add the quantities
            products_with_qty[product_id] += quantity
        else:
            # If the product doesn't exist, set the quantity
            products_with_qty[product_id] = quantity

        bom_lines = self.env['mrp.bom.line'].search([('product_id', '=', product_id)])
        for bom_line in bom_lines:
            # Recursively call for sub-components with updated quantity
            sub_component = bom_line.bom_id.product_tmpl_id.product_variant_id
            self._get_products_from_component(sub_component, bom_line.product_qty * quantity, products_with_qty)

        return products_with_qty
