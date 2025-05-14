from odoo import api, models, fields
import mimetypes


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    receipt_attachment_ids = fields.One2many(
        'ir.attachment', 'res_id',
        domain=[('res_model', '=', 'sale.order')],
        string='Recibos adjuntos'
    )
    email_sent = fields.Boolean(string="Correo enviado", default=False)

    def send_mail(self):
        self.ensure_one()

        template = self.env.ref(
            'add_receipt_upload_web_site.email_template_custom_quotation')

        if template:
            template.send_mail(self.id, force_send=False)
            self.email_sent = True

    def upload_receipt(self, attachment=None):
        """ Guarda el recibo si se pasa como adjunto """
        if attachment:
            data = self.env
            filename = attachment['filename']
            file_data = attachment['data']
            mimetype, _ = mimetypes.guess_type(filename)

            self.env['ir.attachment'].sudo().create({
                'name': filename,
                'type': 'binary',
                'datas': file_data,
                'res_model': 'sale.order',
                'res_id': self.id,
                'mimetype': mimetype or 'application/octet-stream',
            })
        if self.state != 'sale' and self.state != 'cancel':
            self.action_confirm()
