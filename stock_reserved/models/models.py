# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_reserved(models.Model):
    _inherit = 'sale.order.line'

    is_available = fields.Boolean(string="Disponible", compute="get_available", store=True)
    available_stock = fields.Float(compute="get_free_qty", string="Disponible", store=True)

    @api.depends("available_stock", "product_uom_qty")
    def get_available(self):
        for record in self:
            if record.product_id.type == 'product':
                if record.product_uom_qty <= record.available_stock:
                    record.is_available = True
                else:
                    if record.id:
                        record.is_available = False
                    else:
                        record.is_available = True
            else:
                record.is_available = True

    @api.depends('product_id', 'state', 'product_uom_qty')
    def get_free_qty(self):
        for record in self:
            if record.product_id.type == 'product':
                wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
                    [('id', 'child_of', record.order_id.warehouse_id.view_location_id.id)],
                    ['id'],
                )]
                stock_quant = self.env['stock.quant'].search(
                    [('company_id', '=', record.order_id.company_id.id),
                     ('product_id', '=', record.product_id.id),
                     ('location_id', 'in', wh_location_ids)])
                if stock_quant:
                    record.available_stock = stock_quant.mapped('available_quantity')
                else:
                    record.available_stock = False
            else:
                record.available_stock = False


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for record in self:
            if record.order_line.filtered(lambda c: c.is_available is False):
                for line in record.order_line.filtered(lambda c: c.is_available is False):
                    if line.available_stock < line.product_uom_qty and line.product_id.type not in ('consu', 'service'):
                        msg_body = (
                                'No se cuenta con stock suficiente para cumplir con la demanda pactada del producto %s' %
                                line.product_id.name + ' Disponible %s' % line.available_stock)
                        raise Warning(msg_body)
            else:
                res = super(SaleOrder, self).action_confirm()
        return res
