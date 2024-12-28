from odoo.http import Controller, request, route
import base64


class WebFormController(Controller):
    @route('/helpdesk_thanks', auth='public', website=True)
    def helpdesk_request_web_form(self, **kwargs):
        helpdesk = request.env['helpdesk.ticket'].sudo().search([])
        return request.render('custom_helpdesk.helpdesk_thanks_web_form_template', {'helpdesk': helpdesk})

    @route('/create_helpdesk_request', auth='public', website=True)
    def create_helpdesk_request(self, **post):

        category = request.env['helpdesk.category'].search([])
        print("category: ", category)
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
        uploaded_file = post.get('file')  # Get the uploaded file
        file_content = uploaded_file.read() if uploaded_file else None

        ticket = request.env['helpdesk.ticket'].sudo().create({
            'website_student': post.get('website_student'),
            'phone_number': post.get('phone_number'),
            'category_id': int(post.get('category_id')),
            'name': post.get('name'),
            'priority': post.get('priority'),
            'state': 'submitted',
            'file': base64.b64encode(file_content) if file_content else None,
            'is_web_form': True,
        })
        # Trigger recomputation
        if ticket.category_id:
            ticket.category_id._compute_ticket_counts()

        return request.redirect('/helpdesk_thanks')




