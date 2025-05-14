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
    # order.sudo().email_sent = True
        # if not order.email_sent:

        #     # Publicar un mensaje en el chatter de la orden de venta
        #     order.sudo().message_post(
        #         body="Se ha enviado el correo de cotización.",
        #         subject="Correo de cotización enviado",
        #         message_type='notification',
        #     )

    # @http.route('/confirm/quote/upload', type='http', auth='public', csrf=False, website=True)
    # def confirm_quote_form(self, sale_order=None, **post):
    #     """ Muestra el formulario de subida """
    #     if not sale_order:
    #         return request.render("add_receipt_upload_web_site.error_template", {'error': 'Pedido no especificado'})

    #     order = request.env['sale.order'].sudo().search(
    #         [('name', '=', sale_order)], limit=1)
    #     if not order:
    #         return request.render("add_receipt_upload_web_site.error_template", {'error': 'Pedido no encontrado'})

    #     return request.render("add_receipt_upload_web_site.receipt_upload_template", {
    #         'order': order,
    #     })

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

    # @http.route('/confirm/quote/upload/submit', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    # def confirm_quote_upload_submit(self, sale_id=None, **post):
    #     file = request.httprequest.files.get('receipt')
    #     sale_order_id = post.get('sale_order_id')
    #     if not file or not sale_order_id:
    #         return request.render("add_receipt_upload_web_site.error_template", {'error': 'Datos faltantes'})

    #     if not order.exists():
    #         return request.render("add_receipt_upload_web_site.error_template", {'error': 'Pedido no encontrado'})

    #     image_bytes = file.read()
    #     attachment_data = {
    #         'filename': file.filename,
    #         'data': base64.b64encode(image_bytes),
    #     }

    #     # Confirmar la orden y enviar la cotización
    #     order.sudo().action_confirm_with_receipt(attachment=attachment_data)

    #     # Devolver la vista de éxito
    #     return request.render("add_receipt_upload_web_site.upload_success_template", {'order': order})

    # def confirm_quote_upload_submit(self, **post):
    #     file = request.httprequest.files.get('receipt')
    #     sale_order_id = post.get('sale_order_id')
    #     if not file or not sale_order_id:
    #         return request.render("add_receipt_upload_web_site.error_template", {'error': 'Datos faltantes'})

    #     print(f"""

    #           /confirm/quote/upload/submit
    #           {sale_order_id}

    #           """)
    #     order = request.env['sale.order'].sudo().search(
    #         [('id', '=', sale_order_id)], limit=1)
    #     # order = request.env['sale.order'].sudo().browse(
    #     #     int(sale_order_id))
    #     print(f"""

    #           /confirm/quote/upload/submit
    #           {order.id}
    #           {order.display_name}
    #           {order.partner_id.display_name}

    #           """)
    #     if not order.exists():
    #         return request.render("add_receipt_upload_web_site.error_template", {'error': 'Pedido no encontrado'})

    #     image_bytes = file.read()
    #     attachment_data = {
    #         'filename': file.filename,
    #         'data': base64.b64encode(image_bytes),
    #     }

    #     order.sudo().action_confirm_with_receipt(attachment=attachment_data)
    #     order.sudo().action_quotation_send()

    #     return request.render("add_receipt_upload_web_site.upload_success_template", {'order': order})
    # @http.route('/confirm/quote/upload/submit', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    # def confirm_quote_upload_submit(self, **post):
    #     file = request.httprequest.files.get('receipt')
    #     sale_order_name = post.get('sale_order')
    #     if not file or not sale_order_name:
    #         return request.redirect('/?error=datos_faltantes')

    #     order = request.env['sale.order'].sudo().search(
    #         [('name', '=', sale_order_name)], limit=1)
    #     if not order:
    #         return request.redirect('/?error=pedido_no_encontrado')

    #     image_bytes = file.read()
    #     attachment_data = {
    #         'filename': file.filename,
    #         'data': base64.b64encode(image_bytes),
    #     }

    #     order.sudo().action_confirm_with_receipt(attachment=attachment_data)
    #     order.sudo().action_quotation_send()

    #     return request.render("add_receipt_upload_web_site.upload_success_template", {'order': order})
