import json
from odoo import http
from odoo.http import request


class BookApi(http.Controller):

    @http.route('/http/patient/<int:patient_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def get_patient(self, patient_id):
        res = request.env['hms.patient'].sudo().search([('id', '=', patient_id)])
        return request.make_json_response({
            'name': res.f_name,
            'email': res.email,
            'age': res.age,
            'birth_date': res.b_date
        }, status=200)

    @http.route('/http/patient', methods=['Post'], type='http', auth='none', csrf=False)
    def add_patient(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['hms.patient'].sudo().create(vals)
        return request.make_json_response({
                'message': 'patient added successfully',
                'name': res.f_name,
                'email': res.email,
                'age': res.age,
            }, status=200)

    @http.route('/http/patient/<int:patient_id>', methods=['PUT'], type='http', auth='none', csrf=False)
    def update_patient(self,patient_id):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['hms.patient'].sudo().search([('id', '=', patient_id)])
        res.write(vals)
        return request.make_json_response({
                'message': 'patient updated successfully',
                'name': res.f_name,
                'email': res.email,
                'age': res.age,
            }, status=200)

    @http.route('/http/patient/delete/<int:patient_id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    def delete_patient(self, patient_id):
        res = request.env['hms.patient'].sudo().search([('id', '=', patient_id)])
        res.unlink()
        return request.make_json_response({
                'message': 'patient deleted successfully',
            }, status=200)
    