from odoo import models,fields


class Addlog(models.TransientModel):
    _name = 'log.wizard'
    _description = 'Add Log Wizard'

    patient_id = fields.Many2one('hms.patient')
    log_id = fields.Many2one('hms.patient.log')
    log_description = fields.Char(required=True)

    def add_log_action(self):
            self.env['hms.patient.log'].create({
                "patient_logs": self.patient_id.id,
                "description": self.log_description
            })


