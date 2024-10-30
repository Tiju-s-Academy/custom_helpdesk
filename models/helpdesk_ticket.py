from odoo import models,fields,api


class HelpDeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Help Desk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Ticket Title", required=True)
    description = fields.Text(string="Description")
    state = fields.Selection(selection=[('new', 'New'), ('submitted','Submitted'), ('in_progress', 'In Progress'), ('done', 'Done'),
                                         ('canceled', 'Canceled')], tracking=True, String="Status",default='new',index=True)
    priority = fields.Selection(selection=[
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Urgent')],
    string="Priority",
    default='1')
    category_id = fields.Many2one('helpdesk.category', string="Category")
    customer_id = fields.Many2one('res.partner', string="Customer", default=lambda self: self.env.user.partner_id,
                                  required=True,readonly=True)
    create_date = fields.Date(string="Submission Date", readonly=True, default=fields.Date.today)
    expected_resolution_date = fields.Datetime(string="solve within")
    phone_number = fields.Text(string="Phone Number")
    file = fields.Binary(string="Attachment", store=True)
    website_student = fields.Char(string='Name')

    def action_submit(self):
        self.state = 'submitted'
        if self.category_id.team_id.member_ids:
            for user in self.category_id.team_id.member_ids:
                self.activity_schedule(
                    'custom_helpdesk.mail_activity_type_helpdesk_ticket',  # Custom activity type
                    user_id=user.id,
                    note=f'Please Check Ticket: {self.name}'
                )

    def action_start_progress(self):
        for record in self:
            record.state = 'in_progress'

    def action_resolve(self):
        for record in self:
            record.state = 'done'
            activity_ids = self.activity_ids
            if activity_ids:
                activity_ids.unlink()
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
