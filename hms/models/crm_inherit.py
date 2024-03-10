from odoo import models, fields,api
from odoo.exceptions import UserError,ValidationError


class CrmInherit(models.Model):
    _inherit = 'res.partner'
    _description = 'Crm Inherit'

    related_patient_id = fields.Many2one('hms.patient')

    @api.constrains('email')
    def check_mail(self):
        for rec in self:
            if rec.related_patient_id:
                mail = self.env['hms.patient'].search([('email', '=', rec.email)])
                if mail:
                    raise UserError('You cant link to patient using this email, plz change this email')

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError('You cant delete customer related with a patient' )
        return super().unlink()
