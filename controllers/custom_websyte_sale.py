from odoo import http
from odoo.http import request
import base64


class CustomWebsiteSale(http.Controller):

    @http.route('/confirm/quote/upload', type='http', auth='user', website=True, csrf=False)
    def confirm_quote_form(self, **post):
        user_partner = request.env.user.partner_id
        order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', user_partner.id),
        ], limit=1)

        if not order:
            return request.render("add_receipt_upload_web_site.error_template", {'error': 'No hay cotizaciones para este usuario'})

        order.action_confirm()
        order.send_mail()

        return request.render('add_receipt_upload_web_site.success_message_template', {'order': order})

    @http.route('/confirm/quote/upload/submit', type='http', auth='public', website=True, csrf=False)
    def render_upload_form(self, sale_id=None, **post):
        if not sale_id:
            return request.render("add_receipt_upload_web_site.error_template", {
                'error': 'Faltan datos de la orden de venta.'
            })

        user_partner = request.env.user.partner_id

        order = request.env['sale.order'].sudo().search(
            [
                ('id', '=', sale_id),
                ('partner_id', '=', user_partner.id),
            ], limit=1)

        if not order.exists():
            return request.render("add_receipt_upload_web_site.error_template", {
                'error': 'No se encontró la orden de venta.'
            })

        return request.render("add_receipt_upload_web_site.receipt_upload_template", {
            'order': order
        })

    @http.route('/confirm/quote/upload/success', type='http', auth='public', website=True, csrf=False)
    def receipt_success(self, sale_id=None, **post):
        if not sale_id:
            return request.render("add_receipt_upload_web_site.error_template", {
                'error': 'Falta el ID de la orden de venta.'
            })

        order = request.env['sale.order'].sudo().search(
            [('id', '=', sale_id)], limit=1)

        file = request.httprequest.files.get('receipt')
        if not file:
            return request.render("add_receipt_upload_web_site.error_template", {'error': 'Datos faltantes'})

        if not order.exists():
            return request.render("add_receipt_upload_web_site.error_template", {'error': 'Pedido no encontrado'})

        image_bytes = file.read()
        attachment_data = {
            'filename': file.filename,
            'data': base64.b64encode(image_bytes),
        }

        # Confirmar la orden y enviar la cotización
        order.sudo().upload_receipt(attachment=attachment_data)

        return request.redirect('/')
