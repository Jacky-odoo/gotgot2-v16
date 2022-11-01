# # -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    vendor_picking_id = fields.Many2one('stock.picking', string='Picking vendor invoice', ondelete="restrict")



class StockMove(models.Model):
    _inherit = 'stock.move'

    is_locked = fields.Boolean(compute='_compute_is_locked', readonly=True)

    date_expected = fields.Datetime(
        'Expected Date', default=fields.Datetime.now, index=True, required=True,
        states={'done': [('readonly', True)]},
        help="Scheduled date for the processing of this move")
    has_move_lines = fields.Boolean(compute='_compute_has_move_lines')

    @api.depends('picking_id.is_locked')
    def _compute_is_locked(self):
        for move in self:
            if move.picking_id:
                move.is_locked = move.picking_id.is_locked
            else:
                move.is_locked = False
                
    @api.depends('move_line_ids')
    def _compute_has_move_lines(self):
        for move in self:
            move.has_move_lines = bool(move.move_line_ids)


class Picking(models.Model):
    _inherit = "stock.picking"


    vendor_invoice = fields.Char('Vendor Invoice')
    invoice_date = fields.Datetime('Invoice Date')
    invoice_generated = fields.Boolean(string="Invoice Generated")
    

    def action_generate_vendor_bill(self):
        context = dict(self._context) or {}
        context.update({'create': False, 'delete': False})        
        bill_exist = self.env['account.move'].search([('vendor_picking_id', '=', self.id)])
        if not bill_exist:
            move_line_vals = []
            for moves in self.move_ids_without_package:
                move_line_vals.append((0, 0, {
                                            'product_id': moves.product_id.id,
                                            'quantity': moves.quantity_done,
                                                }))
            bill_vals = {'type': 'in_invoice',
                        'vendor_picking_id': self.id,
                        'partner_id': self.partner_id.id,
                        'invoice_line_ids': move_line_vals}
            bill_id = self.env['account.move'].create(bill_vals)
            self.invoice_generated = True
        else :
            bill_id = bill_exist

        return {'name': _('Vendor Bill'),
                'view_mode': 'form',
                'res_model': 'account.move',
                'views': [(self.env.ref('account.view_move_form').id, 'form')],
                'domain': [('vendor_picking_id', '=', self.id)],
                'res_id': bill_id.id,
                'type': 'ir.actions.act_window',
                'context': context
                }

    def action_view_vendor_bill(self):
        context = dict(self._context) or {}
        context.update({'create': False, 'delete': False})        
        bill_exist = self.env['account.move'].search([('vendor_picking_id', '=', self.id)])        
        if bill_exist:
            return {'name': _('Vendor Bill'),
                'view_mode': 'form',
                'res_model': 'account.move',
                'views': [(self.env.ref('account.view_move_form').id, 'form')],
                'domain': [('vendor_picking_id', '=', self.id)],
                'res_id': bill_exist.id,
                'type': 'ir.actions.act_window',
                'context': context
                }

    def put_in_pack(self):
        self.ensure_one()
        if self.state not in ('done', 'cancel'):
            picking_move_lines = self.move_line_ids
            if (
                not self.picking_type_id.show_reserved
                and not self.env.context.get('barcode_view')
            ):
                picking_move_lines = self.move_line_nosuggest_ids

            move_line_ids = picking_move_lines.filtered(lambda ml:
                float_compare(ml.qty_done, 0.0, precision_rounding=ml.product_uom_id.rounding) > 0
                and not ml.result_package_id
            )
            if not move_line_ids:
                move_line_ids = picking_move_lines.filtered(lambda ml: float_compare(ml.product_uom_qty, 0.0,
                                     precision_rounding=ml.product_uom_id.rounding) > 0 and float_compare(ml.qty_done, 0.0,
                                     precision_rounding=ml.product_uom_id.rounding) == 0)
            if move_line_ids:
                res = self._pre_put_in_pack_hook(move_line_ids)
                if not res:
                    res = self._put_in_pack(move_line_ids)
                return res
            else:
                raise UserError(_("Please add 'Done' qantitites to the picking to create a new pack."))
