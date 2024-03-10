from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
import re


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patients'
    _rec_name = 'f_name'

    f_name = fields.Char(string='First Name')
    l_name = fields.Char(string='Last Name')
    b_date = fields.Date(string='Birth Date')
    history = fields.Html()
    cr_ratio = fields.Float(string='CR Ratio', required=True)
    blood_type = fields.Selection([('a', 'A'),
                                   ('b', 'B+'),
                                   ('o', 'O+'),
                                   ('ab', 'AB')])
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='calc_age')
    department_ids = fields.Many2one('hms.department')
    doctor_ids = fields.Many2many('hms.doctor')
    department_capacity = fields.Integer(related='department_ids.capacity')
    states = fields.Selection([('undetermined', 'Undetermined'),
                               ('good', 'Good'),
                               ('fair', 'Fair'),
                               ('serious', 'Serious')])
    email = fields.Char(required=True)
    log_id = fields.One2many('hms.patient.log', 'patient_logs')

    @api.onchange('age')
    def _on_change_pcr(self):
        for record in self:
            if record.age < 30 and self.age != 0:
                record.pcr = True
                return {
                    'warning': {'title': "hello",
                                'message': "the pcr has checked"},
                }
            else:
                record.pcr = False

    @api.model
    def create(self, vals):
        if 'email' in vals:
            search = self.search([('email', '=', vals['email'])])
            if search:
                raise UserError('This email is existed')
            else:
                if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', vals['email']):
                    raise ValidationError("Wrong email format")
        return super().create(vals)

    @api.depends('b_date')
    def calc_age(self):
        for rec in self:
            if rec.b_date:
                rec.age = relativedelta(fields.Date.today(), rec.b_date).years
            else:
                rec.age = False

    def write(self, vals):
        if 'states' in vals:
            for patient in self:
                log_vals = {
                    'patient_logs': patient.id,
                    'description': f"State changed from {patient.states} to {vals['states']}"
                }
                patient.env['hms.patient.log'].create(log_vals)

        if 'email' in vals:
            search = self.search([('email', '=', vals['email'])])
            if search:
                raise UserError('This email is already in use.')
            elif not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', vals['email']):
                raise ValidationError("Invalid email format.")

        return super().write(vals)

    def action_add_log(self):
        action = self.env['ir.actions.actions']._for_xml_id('hms.log_wizard_action')
        action['context'] = {
            'default_patient_id': self.id,
        }
        return action

    def set_undetermined(self):
        for rec in self:
            rec.states = 'undetermined'

    def set_good(self):
        for rec in self:
            rec.states = 'good'

    def set_fair(self):
        for rec in self:
            rec.states = 'fair'

    def set_serious(self):
        for rec in self:
            rec.states = 'serious'


class Log(models.Model):
    _name = 'hms.patient.log'

    created_by = fields.Char(default=lambda self: self.env.user.name, readonly=True)
    created_date = fields.Date(default=datetime.today(), readonly=True)
    description = fields.Text()
    patient_logs = fields.Many2one('hms.patient')
