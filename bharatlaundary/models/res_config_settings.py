from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    otp_api_url = fields.Char(string='OTP API URL', config_parameter='bharatlaundary.otp_api_url')
    otp_api_key = fields.Char(string='OTP API Key', config_parameter='bharatlaundary.otp_api_key')
    otp_client_id = fields.Char(string='OTP Client ID', config_parameter='bharatlaundary.otp_client_id')
    otp_sender_id = fields.Char(string='OTP Sender ID', config_parameter='bharatlaundary.otp_sender_id')
    dlt_template_id = fields.Char(string='DLT Template ID', config_parameter='bharatlaundary.dlt_template_id')
    otp_message_template = fields.Text(string='OTP Message Template', config_parameter='bharatlaundary.otp_message_template')
    android_app_hash = fields.Char(string='Android App Hash', config_parameter='bharatlaundary.android_app_hash')
    test_mobile_number = fields.Char(string='Test Mobile Number', config_parameter='bharatlaundary.test_mobile_number')

    def action_test_sms_otp(self):
        # Logic to send test SMS could be added here later
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Test SMS',
                'message': 'Test SMS action triggered for %s' % self.test_mobile_number,
                'sticky': False,
            }
        }
