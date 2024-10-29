from odoo.http import Controller, request, route


class WebFormController(Controller):
    @route('/helpdesk_thanks', auth='public', website=True)
    def helpdesk_request_web_form(self, **kwargs):
        helpdesk = request.env['helpdesk.ticket'].sudo().search([])
        return request.render('custom_helpdesk.helpdesk_thanks_web_form_template', {'helpdesk': helpdesk})

    @route('/create_helpdesk_request', auth='public', website=True)
    def create_helpdesk_request(self, **post):

        category = request.env['helpdesk.category'].search([])
        priority_field = request.env['helpdesk.ticket'].fields_get(['priority'])['priority']
        priority_options = priority_field.get('selection', [])
        values = {
            'priority_options': priority_options,
            'category': category,
        }
        return request.render('custom_helpdesk.web_form_template', values)

    @route('/helpdesk_request/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def web_form_submit(self, **post):
        request.env['helpdesk.ticket'].sudo().create({
            'website_student': post.get('website_student'),
            'phone_number': post.get('phone_number'),
            'category_id': post.get('category_id'),
            'name': post.get('name'),
            'priority': post.get('priority'),
        })
        return request.redirect('/helpdesk_thanks')



