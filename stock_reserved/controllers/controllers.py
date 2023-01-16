# -*- coding: utf-8 -*-
# from odoo import http


# class StockReserved(http.Controller):
#     @http.route('/stock_reserved/stock_reserved/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_reserved/stock_reserved/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_reserved.listing', {
#             'root': '/stock_reserved/stock_reserved',
#             'objects': http.request.env['stock_reserved.stock_reserved'].search([]),
#         })

#     @http.route('/stock_reserved/stock_reserved/objects/<model("stock_reserved.stock_reserved"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_reserved.object', {
#             'object': obj
#         })
