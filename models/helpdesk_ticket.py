from odoo import models,fields,api


class HelpDeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Help Desk Ticket'

    name = fields.Char(string="Ticket Title", required=True)
    description = fields.Text(string="Description")
    state = fields.Selection(selection=[('new', 'New'), ('submitted','Submitted'), ('in_progress', 'In Progress'), ('done', 'Done'),
                                         ('canceled', 'Canceled')], tracking=True, String="Status",default='new')
    priority = fields.Selection(selection=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                                string="Priority", default='medium')
    category_id = fields.Many2one('helpdesk.category', string="Category")
    customer_id = fields.Many2one('res.partner', string="Customer", default=lambda self: self.env.user.partner_id,
                                  required=True)
    create_date = fields.Datetime(string="Creation Date", readonly=True, default=fields.Datetime.now)
    expected_resolution_date = fields.Datetime(string="Resolve within")
    phone_number = fields.Text(string="Phone Number")
    file = fields.Binary(string="Attachment")
    website_student = fields.Char(string='Name')

    def action_submit(self):
        self.state = 'submitted'

    def action_start_progress(self):
        for record in self:
            record.state = 'in_progress'

    def action_resolve(self):
        for record in self:
            record.state = 'done'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Solved',
                    'type': 'rainbow_man',
                }
            }

    def action_cancel_submission(self):
        for record in self:
            record.state = 'canceled'
