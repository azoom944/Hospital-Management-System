from odoo import fields, models


class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hms Departments'

    name = fields.Char(string='Department Name')
    capacity = fields.Integer(string='Department Capacity')
    is_opened = fields.Boolean()
    patients = fields.One2many('hms.patient', 'department_ids')
